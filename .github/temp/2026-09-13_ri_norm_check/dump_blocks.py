"""Dump L-block / G-record (E, RI, DRI) from an ENSDF dataset file.

Usage: python dump_blocks.py FILE [EMAX]
"""
import sys

def main():
    path = sys.argv[1]
    emax = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
    cur = None
    curE = None
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for i, raw in enumerate(fh, 1):
            line = raw.rstrip('\n').rstrip('\r')
            if len(line) < 10:
                continue
            typ = line[7]
            if typ == 'L' and line[6] == ' ':
                e = line[9:19].strip()
                try:
                    curE = float(e)
                except ValueError:
                    curE = None
                cur = e
                if curE is not None and curE <= emax:
                    print('L %6d  E=%-11s J=%-16s XREF=%s' % (i, e, line[22:39].strip(), line[39:80].strip()))
            elif typ == 'G' and line[6] == ' ' and curE is not None and curE <= emax:
                print('  G %6d  E=%-11s RI=%-8s DRI=%-3s M=%-9s MR=%-8s C=%r Q=%r' % (
                    i, line[9:19].strip(), line[22:29].strip(), line[29:31].strip(),
                    line[32:41].strip(), line[41:49].strip(), line[76:77], line[79:80]))

main()
