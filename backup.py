#!/usr/bin/env python
# coding: latin-1
# method stolen from Gregg Hansen's excellent script: http://beekl.es/5w

# import a bunch of stuff (you may need to 'apt-get install python-yaml' or
# similar)
import urllib
import yaml
import sys
import os
import re
import time
from datetime import datetime

###############################################################################


class Tomato(dict):
    """Class representing a Tomato device"""
    def __init__(self, name):
        self['name'] = name

# do some configuration
        self.config = yaml.load(open('config/config.yaml'))
        self.update(self.config['hosts'][self['name']])

# do these things
        self.set_date()
        self.set_paths()
        self.set_regexes()
        self.extract_data()

###############################################################################

    def set_date(self):
        """Set the date stamp for the dump file"""

# this has always seemed horrendously complicated to me. I think I'm doing it
# wrong
        self['datestamp'] = time.strftime("%Y-%m-%d",
                            datetime.fromtimestamp(time.time()).timetuple())

###############################################################################

    def set_regexes(self):
        """Set up the regexes to match bits of the HTML from the admin page"""

# pack them into this dict
        self['regexes'] = {}

# they're actually defined in the config file
        for key in self.config['regexes']:
            self['regexes'][key] = re.compile(self.config['regexes'][key])

###############################################################################

    def extract_data(self):
        """Pull the interesting bits out of the admin page HTML"""

# read the page into a list of strings
        lines = urllib.urlopen(
            "%s/admin-config.asp" % self['baseurl']).readlines()

# for each line
        for line in lines:

# try each regex
            for regex in self['regexes']:
                m = self['regexes'][regex].match(line)

# if we got a match
                if m:

# set the captured value in ourself under the key from the regexes hash
# the split/join thing is to remove the ':'s from the MAV address
                    self[regex] = "".join(m.group(1).split(':'))

###############################################################################

    def set_paths(self):
        """Set some paths we'll use later"""

# construct the base URL of the Tomato
        self['baseurl'] = "https://%s:%s@%s" % (
                                self['user'],
                                self['password'],
                                self['name'])

# we'll send our dump to this dir
        self['outdir'] = os.path.join(
                                self.config['paths']['dumps'],
                                self['datestamp'])

# the dir needs to exist (python needs something 'mkdir -p'-ish)
        try:
            os.makedirs(self['outdir'])
        except OSError:
            pass

# the path for the actual dump file
        self['outfile'] = os.path.join(
                        self['outdir'],
                        "%s.%s.cfg.gz" % (self['name'], self['datestamp']))

###############################################################################

    def download(self):
        """Actually download the config"""

# the filename (on the Tomato)
        self['filename'] = "tomato_v%s_m%s.cfg" % (
                                                self['version'], self['mac'])

# the URL for the file
        self['url'] = "%s/cfg/%s?_http_id=%s" % (
                                self['baseurl'],
                                self['filename'],
                                self['httpd_id'])

# grab the file and dump it
        urllib.urlretrieve(self['url'], self['outfile'])

###############################################################################

# if we're called on the command line
if __name__ == '__main__':

# grab all entries from the 'hosts' stanza in the config file
    toms = yaml.load(open('config/config.yaml'))['hosts']

# for each one
    for tom in toms:

# make a tomato
        t = Tomato(tom)

# do the download
        t.download()
