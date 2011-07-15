#!/usr/bin/env python

import gzip
import sys
import yaml
import os

# will add objecty shit up in here

class TomatoConfig(dict):
    def __init__(self, path):
        self['path'] = path
        self.populate()

    def populate(self):
        f = gzip.open(self['path'])
        s = ""
        try:
            byte = f.read(1)
            while byte != "":
                s += byte
                if byte == "\x00":
                    b = s.split("=")
                    try:
                        if not b[1] == "\x00":
                            self[b[0]] = b[1]
                    except IndexError:
                        pass

                    s = ""
                byte = f.read(1)
        finally:
            f.close()

    def get(self, key):
        try:
            return self[key]
        except KeyError:
            return None

    def __repr__(self):
        s = ""
        wide = 0
        for key in self:
            if len(key) > wide:
                wide = len(key)

        frmt = "%%%ds:	%%s" % wide
        for key in self:
            s += frmt % (key, self[key])
            s += "\n"

        return s

if __name__ == '__main__':
    config = yaml.load(open('config/config.yaml'))
    dump_dir = config['paths']['dumps']
    files = os.listdir(dump_dir)
    files.sort()
    fd = os.path.join(dump_dir, files[-1])
    fn = os.listdir(fd)[0]
    fp = os.path.join(fd, fn)

    tc = TomatoConfig(fp)
    print tc


