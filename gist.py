#!/usr/bin/env python
# encoding: utf-8
import sys
import urllib
import optparse
import subprocess	

GIST_URL = "http://gist.github.com/{0}.txt"

def main(*args):
	import gist
	
	print(GIST_URL.format("HAM"))

if __name__ == "__main__": sys.exit(main(*sys.argv[1:]))
