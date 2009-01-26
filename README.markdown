Gist: The Script
================

Works great with Gist: The Website.

Ported this script to Python.. Also supports passing multiple files



Installation
------------

    You need to set the GitHub config options to use this properly:
    http://github.com/guides/local-github-config

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


Vim shortcut Key
------------

Add these lines to your .vimrc file and you have a new shortcut: Shift + F9 will write the file and create a Gist from it


    " Make a Gist of this file..
    map <S-F9> :w<CR> :!gist %<CR>



TODO
------------

 * Add directory support
