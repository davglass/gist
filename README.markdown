Gist: The Script
================

Works great with Gist: The Website.

Ported this script to Python.. Also supports passing multiple files



Installation
------------

    You need to set the GitHub config options to use this properly:
    Go here: https://github.com/account
    Click the "Global Git Config" link, follow instructions

    curl http://github.com/davglass/gist/raw/master/gist.py?raw=true > gist
    chmod 755 gist
    sudo mv gist /usr/local/bin/gist



Usage
------------
    
    #Creates a new Gist
    gist file.txt file2.js file3.html

    #Pull the Gist #12345
    gist -r 12345

    #Clone the Gist #12345
    gist -r 12345 -c


TODO
------------

 * Add directory support
