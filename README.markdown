Gist: The Python 3.0 Script
===========================

Works great with Gist: The Website!

This is the Python 3.0 version of this script, derived from the Ruby and
Python 2 versions.

Usage
-----

	# create a gist from one or more files
	./gist.py [-p] file [file2 file3...]
	
	# create a gist from stdin, giving if a filename
	cal | ./gist.py -i cal.txt
	
	# clone the repostiories of one or more gists
	./gist.py -c id [id2 id3...]
	
	# display the text contents of a gist
	./gist.py -r id

Installation
------------

You need to set the GitHub config options to use this properly.
[Instructions are available
](http://github.com/guides/local-github-config) in the GitHub guides.

	curl http://github.com/JeremyBanks/gist/raw/master/3.0/gist.py > gist
	chmod 755 gist
	sudo mv gist /usr/local/bin/gist

Before you decide to install this, a word of caution: This is currently
under rapid development, and code only trivially tested before being
pushed here. Functionality may change or be broken at any time.

TODO
----

* Support for reading private Gists
* Use official API wherever possible
* Allow private cloning of Gists
  * Add flags to force using the public or private clone URLs
  * Detect if you are cloning one of your own Gists and default to using
    the private URL if so
* Allow `stdin` files to have types without names

Repositories and Authors
------------------------

* [Ruby version](http://github.com/defunkt/gist/) by
  [Chris Wanstrath](http://github.com/defunkt) (defunkt)
* [Python 2 version](http://github.com/davglass/gist/) by
  [Dav Glass](http://github.com/davglass)
* [Python 3.0 version](http://github.com/JeremyBanks/gist/) by
  [Jeremy Banks](http://github.com/jeremybanks)

License
-------

	Copyright © 2008, 2009 Chris Wanstrath, Dav Glass and Jeremy Banks
	
	Permission is hereby granted, free of charge, to any person obtaining
	a copy of this software and associated documentation files (the
	"Software"), to deal in the Software without restriction, including
	without limitation the rights to use, copy, modify, merge, publish,
	distribute, sublicense, and/or sell copies of the Software, and to
	permit persons to whom the Software is furnished to do so, subject to
	the following conditions:
	
	The above copyright notice and this permission notice shall be
	included in all copies or substantial portions of the Software.
	
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
	IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
	CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
	TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
	SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
