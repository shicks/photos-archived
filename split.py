#!/usr/bin/python

# Splits photos into groups
# Reads filenames from stdin

import math
import sys
import os

MIN_SIZE = 5
MIN_WINDOW = 6 * 3600

def diff(x, n):
    return [a-b for a,b in zip(x[n:], x[:-n])]

files = {}
misformed = []
lines = sys.stdin.readlines()
for line in lines:
    line = line[:-1] # chop off the newline
    try:
        t = int(line.split('/')[-1][:10])
        if t not in files:
            files[t] = []
        files[t].append(line)
    except ValueError:
        misformed.append(line)

ts = files.keys()
ts.sort()

chunks = []

while len(ts) > 10:
    dt = diff(ts, 10)
    target = min(range(len(dt)), key=lambda i:dt[i])
    dt0 = max(2 * dt[target] / MIN_SIZE, MIN_WINDOW)
    start = target
    end = target + MIN_SIZE
    print "Chunk: %d, dt0=%d, start=%d/%d, end=%d/%d" % (dt[target], dt0, start, ts[start], end-1, ts[end - 1])
    while start > 0 and ts[start] - ts[start-1] < dt0:
        start -= 1
    while end < len(ts) and ts[end] - ts[end - 1] < dt0:
        end += 1
    print "  Expanded: start=%d/%d, end=%d/%d                              DELTA=%d" % (start, ts[start], end-1, ts[end - 1], ts[end-1]-ts[start])
    chunk = ts[start:end]
    chunks.append(chunk)
    #print chunk
    ts = ts[:start] + ts[end:]

if ts:
    chunks.append(ts)
    #print ts

chunks.sort(key=lambda c:c[0])
for chunk in chunks:
    d = 'chunk-%d-%d' % (chunk[0], chunk[-1])
    os.mkdir(d)
    for t in chunk:
        for f in files[t]:
            os.symlink('../%s' % f, '%s/%s' % (d, f.split('/')[-1]))
try:
    os.mkdir('chunk-misformed')
except OSError:
    pass # okay - already exists
for f in misformed:
    os.symlink('../%s' % f, 'chunk-misformed/%s' % f.split('/')[-1])
