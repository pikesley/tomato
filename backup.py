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

# get today's date in ISO-ish format (this has always seemed way too complex to
# me, I think I must be doing it wrong)
datestamp = time.strftime("%Y-%m-%d",
                            datetime.fromtimestamp(time.time()).timetuple())

# load up our config
config = yaml.load(open('config/config.yaml'))

# construct the base URL of the tomato router
baseurl = "https://%s:%s@%s" % (
                                config['host']['user'],
                                config['host']['password'],
                                config['host']['name'])

print "Retrieving data from %s..." % config['host']['name'],

# grab the HTML as a list of lines
lines = urllib.urlopen("%s/admin-config.asp" % baseurl).readlines()
print "done"

# we want to extract lines that match these patterns (and capture the (.*)
# bits)
regexes = {
    'version': re.compile(".*<div class='version'>Version (.*)</div>.*"),
    'mac': re.compile(".*et0macaddr: '..:..:..:(.*)',.*"),
    'httpd_id': re.compile(".*http_id: '(.*)',.*")}

# we will store stuff in here
data = {}

print "Extracting data...",

# so line by line
for line in lines:

# try to match each regex
    for regex in regexes:
        m = regexes[regex].match(line)

# if we got a match
        if m:

# we store the matched group into the data dict under the key from the regex
# dict. we do the 'split/join' thing to remove the ':'s from the MAC address
            data[regex] = "".join(m.group(1).split(':'))
print "done"

print "Downloading config file...",

# construct the config filename
filename = "tomato_v%s_m%s.cfg" % (data['version'], data['mac'])

# and the URL from which we can retrieve it
url = "%s/cfg/%s?_http_id=%s" % (baseurl, filename, data['httpd_id'])

# we will dump it to this dir
outdir = os.path.join(config['paths']['dumps'], datestamp)

# the dir needs to exist (python really needs something 'mkdir -p'-ish)
try:
    os.makedirs(outdir)
except OSError:
    pass

# this shall be our dump file (it comes as a .gz)
outfile = os.path.join(
                        outdir,
                        "%s.%s.cfg.gz" % (config['host']['name'], datestamp))

# actually download the file
u = urllib.urlretrieve(url, outfile)
print "done"
