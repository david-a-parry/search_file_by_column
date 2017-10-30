#!/usr/bin/env python3
import sys
import os
import pickle
import argparse
import mmh3
from collections import namedtuple 

Node = namedtuple('Node', ['pos', 'next'])

def get_parser():
    '''Get ArgumentParser'''
    parser = argparse.ArgumentParser(
            description='''Index and retrieve file entries by column.''',)

    parser.add_argument('infile', metavar='FILE', help=''' Input filename''')
    parser.add_argument('column', metavar='COL', type=int, help=
                        ''' Column of file to search/index. Default=1 '''),
    parser.add_argument('-s', '--string', help=''' String to search for'''),
    parser.add_argument('-z', '--index_size', default=2**24,
                        help=''' Size of index. Default = 2^24'''),
    return parser

def build_idx(infile, index_file, column=1, size=2**24, ):
    sys.stderr.write("Indexing {}\n".format(infile))
    idx = [ None ] * size
    with open(infile, 'r') as f:
        while True:
            pos = f.tell()
            line = f.readline()
            if not line: break
            cols = line.split()
            i = mmh3.hash(cols[column-1]) % size
            if idx[i] is None:
                idx[i] = pos
            else:
                idx[i] = Node(pos, idx[i])
    pfh = open(index_file, 'wb')
    pickle.dump(idx, pfh)
    pfh.close()
    return idx

def search(string, idx, f, column):
    i = mmh3.hash(string) % len(idx)
    entry = idx[i]
    hits = []
    while entry is not None:
        pos = entry.pos if isinstance(entry, Node) else entry
        f.seek(pos)
        line = f.readline().rstrip()
        col = line.split()[column-1]
        if col == string:
            hits.append(line)
        entry = entry.next if isinstance(entry, Node) else None
    hits.reverse()
    return hits

def search_file(infile, column, string=None, index_size=2**24):
    index_file = str.format("{}.{}.sbcidx".format(infile, column))
    if os.path.exists(index_file):
        if os.path.getmtime(index_file) < os.path.getmtime(infile):
            sys.stderr.write("WARNING: Index file {} is older than input {}.\n"
                             .format(index_file, infile))
        pfh = open(index_file, 'rb')
        idx = pickle.load(pfh)
        pfh.close()
    else:
        idx = build_idx(infile, index_file, column, index_size)
    if string is not None:
        with open(infile, 'r') as f:
            found = (search(string, idx, f, column))
            if not found:
                sys.stderr.write("No matches found\n")
            else:
                for x in found: print(x)
                sys.stderr.write("{:,} matches found\n".format(len(found)))

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    search_file(**vars(args))

