#!/usr/bin/env python

import gzip
import sys
import yaml
import os

# will add objecty shit up in here

config = yaml.load(open('config/config.yaml'))

dump_dir = config['paths']['dumps']

files = os.listdir(dump_dir)
files.sort()

fd = os.path.join(dump_dir, files[-1])
fn = os.listdir(fd)[0]
fp = os.path.join(fd, fn)

f = gzip.open(fp, 'rb')

d = {}
s = ""
try:
    byte = f.read(1)
    while byte != "":
        s += byte
        if byte == "\x00":
            b = s.split("=")
            try:
                if not b[1] == "\x00":
                    d[b[0]] = b[1]
            except IndexError:
                pass

            s = ""
        byte = f.read(1)
finally:
    f.close()

wide = 0
for key in d:
    if len(key) > wide:
        wide = len(key)

frmt = "%%%ds:	%%s" % wide
for key in d:
    print frmt % (key, d[key])
