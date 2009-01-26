#!/usr/bin/env python

from optparse import OptionParser
import os, sys, string, pprint
from cStringIO import StringIO
import urllib2, urllib, subprocess

optparser = OptionParser("usage: %prog [-p] file1 file2 file3\n\nPass files to me and I'll post them to http://gist.github.com")
optparser.set_defaults(gistread="")
optparser.add_option( "-p", "--private",
        action="store_true", dest="private",
        help="The private secret." )
optparser.add_option( "-r", "--read",
        action="store", dest="gistread", type="string",
        help="The Gist to read.." )


(opts, filenames) = optparser.parse_args()


def copy(content):
    system = sys.platform
    if system == 'darwin':
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.stdin.write(content)
        p.stdin.close()
        retcode = p.wait()
    elif system == 'linux':
        p = subprocess.Popen(['xclip'], stdin=subprocess.PIPE)
        p.stdin.write(content)
        p.stdin.close()
        retcode = p.wait()
        
        

def write(filenames):
    out = {}
    counter = 1

    for i in filenames:
        if os.path.isfile(i):
            info = os.path.splitext(i)
            f = open(i)
            fileStr = StringIO(f.read()).getvalue()
            ext_key = "file_ext[gistfile%s]" % counter
            name_key = "file_name[gistfile%s]" % counter
            content_key = "file_contents[gistfile%s]" % counter
            out[ext_key] = info[1]
            out[name_key] = i
            out[content_key] = fileStr
            counter = counter + 1
        
    if opts.private:
        out['private'] = 'on'

    out['login'] = os.popen('git config --global github.user').read().strip()
    out['token'] = os.popen('git config --global github.token').read().strip()


    pp = pprint.PrettyPrinter(indent=4)

    url = 'http://gist.github.com/gists'
    data = urllib.urlencode(out)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)

    url = response.geturl()
    copy(url)
    print url


def read(id):
    url = "http://gist.github.com/%s.txt" % id;
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    
    data = response.read()
    copy(data)
    print data


if opts.gistread:
    read(opts.gistread)
    sys.exit(1)
    


if len(filenames) == 0:
    print "No args given.."
    sys.exit(1)

write(filenames)
