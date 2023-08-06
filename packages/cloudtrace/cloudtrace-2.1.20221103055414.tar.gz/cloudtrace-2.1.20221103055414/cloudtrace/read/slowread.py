import json
import os.path
import sys
import traceback
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from collections import defaultdict, namedtuple, OrderedDict
from datetime import timedelta
from multiprocessing import Pool
from subprocess import Popen, PIPE
from sys import stderr
from typing import List, Dict
from socket import IPPROTO_ICMP, IPPROTO_UDP

from file2 import fopen
from pb_amarder import Progress

# {"type": "trace", "version": "0.1", "userid": 0, "method": "udp-paris", "src": "172.31.25.243", "dst": "99.198.241.1", "sport": 6179, "dport": 30000, "stop_reason": "GAPLIMIT", "stop_data": 0, "start": {"sec": 1666208958, "usec": 841377, "ftime": "fake"}, "hop_count": 5, "attempts": 1, "hoplimit": 32, "firsthop": 1, "wait": 15, "wait_probe": 0, "tos": 0, "probe_size": 64}

_fix = True
verbose = False
_timeout = 10

TraceInfo = namedtuple('TraceInfo', ['src', 'dst', 'proto'])

def remove_old(ts, times, reqs, timeout):
    sec = ts['ts_sec']
    todel = []
    for tinfo, tx in times.items():
        if sec - tx > timeout:
        # if (timedelta(milliseconds=ts) - timedelta(milliseconds=tx)).total_seconds() >= 10:
            todel.append(tinfo)
        else:
            break
    # print(f'Removing {len(todel):,d}', file=stderr)
    for tinfo in todel:
        del times[tinfo]
        del reqs[tinfo]
    return todel

def write_traces(towrite: List[TraceInfo], traces, extra_info: Dict[TraceInfo, Dict[str, int]], outfile, timeout):
    for tinfo in towrite:
        dst = tinfo.dst
        hops = traces.pop(tinfo, None)
        extra = extra_info.pop(tinfo)
        if hops:
            hops = sorted(hops, key=lambda x: x['probe_ttl'])
            hops, stop_reason = truncate_hops(hops, dst)
            if len(hops) > 0:
                hop = hops[0]
                tx = hop['tx']
                if tinfo.proto == IPPROTO_ICMP:
                    method = 'icmp-echo-paris'
                elif tinfo.proto == IPPROTO_UDP:
                    method = 'udp-paris'
                else:
                    continue
                # start = dict(sec=tx['sec'], usec=tx['usec'], ftime='fake')
                start = f'{{"sec": {tx["sec"]}, "usec": {tx["usec"]}, "ftime": "fake"}}'
                truncate_hops(hops, dst)
                output = f'{{"type": "trace", "version": "0.1", "userid": 0, "method": "{method}", "src": "{tinfo.src}", "dst": "{tinfo.dst}", '
                if tinfo.proto == IPPROTO_ICMP:
                    output += f'"icmp_sum": {extra["icmp_sum"]}, '
                elif tinfo.proto == IPPROTO_UDP:
                    output += f'"sport": {extra["sport"]}, "dport": {extra["dport"]}, '
                output += (f'"stop_reason": "{stop_reason}", "stop_data": 0, "start": {start}, "hop_count": {len(hops)}, '
                           f'"attempts": 1, "hoplimit": 32, "firsthop": 1, "wait": {timeout}, "wait_probe": 0, "tos": 0, "probe_size": 64, '
                           f'"hops": {json.dumps(hops)}}}\n')
                outfile.write(output)
                # trace = dict(
                #     type='trace', version='0.1', userid=0,
                #     method=method,
                #     src=tinfo.src, dst=dst,
                #     icmp_sum=47652,
                #     stop_reason=stop_reason, stop_data=0,
                #     start=start, hop_count=len(hops), attempts=1, hoplimit=32, firsthop=1,
                #     wait=10, wait_probe=0, tos=0, probe_size=64, hops=hops
                # )
                # outfile.write(json.dumps(trace) + '\n')

def truncate_hops(hops, dst):
    seen = set()
    prev = None
    for i, hop in enumerate(hops):
        if hop['addr'] == dst:
            return hops[:i+1], 'COMPLETED'
        elif hop['icmp_type'] == 3:
            return hops[:i+1], 'UNREACH'
        addr = hop['addr']
        if addr in seen:
            return hops[:i+1], 'LOOP'
        if prev is not None:
            seen.add(prev)
        prev = addr
    return hops, 'GAPLIMIT'

def read_pcap(infile, outfile, timeout):
    reqs = defaultdict(dict)
    times = OrderedDict()
    traces = defaultdict(list)
    extra_info = {}
    noinfo = 0
    skipped = 0
    wrongtype = 0
    malformed = 0
    start = None
    lines = 0
    pb = Progress(message='Converting pcap to json', increment=100000, callback=lambda: f'Skipped {skipped:,d} NoInfo {noinfo:,d} WrongType {wrongtype:,d} Malformed {malformed:,d}')
    for line in pb.iterator(infile):
        try:
            j = json.loads(line)
            ts = j['timestamp']
            if start is None:
                start = ts
            ip = j['ip']
            proto = ip['ip_proto']
            src = ip['ip_src']
            dst = ip['ip_dst']
            ttl = ip['ip_ttl']
            if proto == IPPROTO_ICMP:
                icmp = j['icmp']
                icmp_type = icmp['icmp_type']
                if icmp_type == 8:
                    tinfo = TraceInfo(src, dst, proto)
                    reqs[tinfo][ttl] = dict(ts_sec=ts['ts_sec'], ts_usec=ts['ts_usec'], src=src, dst=dst, size=ip['ip_len'])
                    extra_info[tinfo] = dict(icmp_sum=icmp['icmp_check'])
                    times[tinfo] = ts['ts_sec']
                else:
                    if icmp_type == 3 or icmp_type == 11:
                        qip = icmp['ip']
                        odst = qip['ip_dst']
                        qproto = qip['ip_proto']
                        if qproto == IPPROTO_ICMP:
                            try:
                                qicmp = icmp['icmp']
                            except KeyError:
                                noinfo += 1
                                continue
                            ottl = qicmp['icmp_seq']
                        elif qproto == IPPROTO_UDP:
                            try:
                                qudp = icmp['udp']
                            except KeyError:
                                noinfo += 1
                                continue
                            ottl = qudp['udp_check']
                        else:
                            wrongtype += 1
                            continue
                        tinfo = TraceInfo(dst, odst, qproto)
                        extra = dict(icmp_q_ttl=qip['ip_ttl'], icmp_q_ipl=qip['ip_len'], icmp_q_tos=qip['ip_tos'])
                    elif icmp_type == 0:
                        ottl = icmp['icmp_seq']
                        odst = src
                        tinfo = TraceInfo(dst, odst, 1)
                        extra = None
                    else:
                        wrongtype += 1
                        continue
                    try:
                        req = reqs[tinfo][ottl]
                    except KeyError:
                        skipped += 1
                        continue
                    tx = timedelta(seconds=req['ts_sec'], microseconds=req['ts_usec'])
                    rx = timedelta(seconds=ts['ts_sec'], microseconds=ts['ts_usec'])
                    rtt = round((rx - tx).total_seconds() * 1000, 3)
                    hop = dict(
                        addr=src, probe_ttl=ottl, probe_id=1, probe_size=req['size'],
                        tx={'sec': req['ts_sec'], 'usec': req['ts_usec']}, rtt=rtt,
                        reply_ttl=ttl, reply_tos=ip['ip_tos'], reply_ipid=ip['ip_id'], reply_size=ip['ip_len'],
                        icmp_type=icmp_type, icmp_code=icmp['icmp_code']
                    )
                    if extra is not None:
                        hop.update(extra)
                    traces[tinfo].append(hop)
            elif proto == IPPROTO_UDP:
                udp = j['udp']
                tinfo = TraceInfo(src, dst, proto)
                reqs[tinfo][ttl] = dict(ts_sec=ts['ts_sec'], ts_usec=ts['ts_usec'], src=src, dst=dst, size=ip['ip_len'])
                extra_info[tinfo] = dict(sport=udp['udp_src'], dport=udp['udp_dst'])
                times[tinfo] = ts['ts_sec']
            lines += 1
            if lines >= 100000:
                todel = remove_old(ts, times, reqs, timeout)
                write_traces(todel, traces, extra_info, outfile, timeout)
                lines = 0
                # removed.update(todel)
        except KeyError:
            # print()
            print(line)
            traceback.print_exc()
            # raise
            malformed += 1
            # raise
        except:
            print()
            print(line)
            raise
    # todel = remove_old(float('inf'), times, reqs)
    write_traces(list(traces.keys()), traces, extra_info, outfile, timeout)

def convert(infile, outfile, timeout, fix=True):
    sidefile = (infile.rpartition('.')[0] if infile.endswith('.gz') or infile.endswith('.bz2') else infile) + '.sidecar'
    if os.path.exists(sidefile):
        with open(sidefile) as f:
            header = f.readline()
            footer = f.readline()
    else:
        header = '{"type":"cycle-start", "list_name":"default", "id":0, "hostname":"fake", "start_time":0}\n'
        footer = '{"type":"cycle-stop", "list_name":"default", "id":0, "hostname":"fake", "stop_time":0}\n'
    if fix:
        pref = f"pcapfix2 -o - {infile}"
    elif infile.endswith('gz'):
        pref = f'gzip -dc {infile}'
    elif infile.endswith('bz2'):
        pref = f'bzip2 -df {infile}'
    else:
        pref = f'cat {infile}'
    cmd = f"{pref} | pcap2json -o - -"
    print(cmd)
    p = Popen(cmd, shell=True, universal_newlines=True, stdout=PIPE)
    fout = fopen(outfile, 'wt') if outfile != '-' else sys.stdout
    try:
        # with fopen(outfile, 'wt') as fout:
        # print(header)
        fout.write(header)
        read_pcap(p.stdout, fout, timeout)
        fout.write(footer)
    finally:
        if outfile == '-':
            fout.close()
    #     p.terminate()
    #     p.communicate()

def convert_wrapper(args):
    infile, outfile = args
    convert(infile, outfile, _timeout, fix=_fix)

def pattern(infile, gzip=False, bzip2=False):
    if infile.endswith('.bz2'):
        outfile = infile[:-4]
    elif infile.endswith('.gz'):
        outfile = infile[:-3]
    else:
        outfile = infile
    outfile = '{}.json'.format(outfile)
    if gzip:
        outfile += '.gz'
    elif bzip2:
        outfile += '.bz2'
    return outfile

def main():
    global _fix, verbose, _timeout
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-r', '--raw', action='store_true')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-o', '--outfiles', nargs='+')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-z', '--gzip', action='store_true')
    group.add_argument('-b', '--bzip2', action='store_true')
    parser.add_argument('-p', '--processes', default=1, type=int)
    parser.add_argument('-i', '--infiles', nargs='+')
    parser.add_argument('-I', '--file')
    parser.add_argument('-t', '--timeout', type=int, default=_timeout)
    args = parser.parse_args()

    _fix = not args.raw
    print('Fixing pcap file: {}'.format(_fix))
    verbose = args.verbose

    _timeout = args.timeout

    infiles = args.infiles if args.infiles is not None else []
    if args.file:
        with open(args.file, 'rt') as f:
            for filename in f:
                infiles.append(filename.strip())

    if args.outfiles:
        if len(args.outfiles) != len(infiles):
            print('Outfiles must match number of infiles.')
            exit(1)
        outfiles = args.outfiles
    else:
        outfiles = []
        for infile in infiles:
            outfile = pattern(infile, gzip=args.gzip, bzip2=args.bzip2)
            outfiles.append(outfile)

    processes = min(args.processes, len(infiles))

    pb = Progress(len(infiles), message=f'Creating traceroutes with {processes} process')
    if processes == 1:
        for infile, outfile in pb.iterator(zip(infiles, outfiles)):
            convert(infile, outfile, _timeout, fix=_fix)
    else:
        Progress.set_output(False)
        with Pool(processes) as pool:
            for _ in pb.iterator(pool.imap_unordered(convert_wrapper, zip(infiles, outfiles))):
                pass
        Progress.set_output(True)

if __name__ == '__main__':
    main()