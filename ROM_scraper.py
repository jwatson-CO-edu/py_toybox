#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__progname__ = "PROGRAM_NAME.py"
__version__  = "YYYY.MM"
__desc__     = "A_ONE_LINE_DESCRIPTION_OF_THE_FILE"
"""
James Watson , Template Version: 2018-05-14
Built on Wing 101 IDE for Python 3.6

Dependencies: numpy
"""


"""  
~~~ Developmnent Plan ~~~
[ ] Port DFS to MARCHHARE3
[ ] ITEM2
"""

# === Init Environment =====================================================================================================================
# ~~~ Prepare Paths ~~~
import sys, os.path
SOURCEDIR = os.path.dirname( os.path.abspath( __file__ ) ) # URL, dir containing source file: http://stackoverflow.com/a/7783326
PARENTDIR = os.path.dirname( SOURCEDIR )
# ~~ Path Utilities ~~
def prepend_dir_to_path( pathName ): sys.path.insert( 0 , pathName ) # Might need this to fetch a lib in a parent directory

# ~~~ Imports ~~~
# ~~ Standard ~~
from math import pi , sqrt
import urllib.request
import re
# ~~ Special ~~
import numpy as np
from bs4 import BeautifulSoup
    
# ~~ Local ~~

# ~~ Constants , Shortcuts , Aliases ~~
EPSILON = 1e-7
infty   = 1e309 # URL: http://stackoverflow.com/questions/1628026/python-infinity-any-caveats#comment31860436_1628026
endl    = os.linesep

# ~~ Script Signature ~~
def __prog_signature__(): return __progname__ + " , Version " + __version__ # Return a string representing program name and verions

# ___ End Init _____________________________________________________________________________________________________________________________


# === Main Application =====================================================================================================================

# ~~ Program Constants ~~


# == Program Functions ==



# __ End Func __


# == Program Classes ==



# __ End Class __


# == Program Vars ==
ROMURL  = "https://yomiko.bytex64.net/media/games/NES/"
_PARENT = "../"

# __ End Vars __


if __name__ == "__main__":
    print( __prog_signature__() )
    termArgs = sys.argv[1:] # Terminal arguments , if they exist
        
    html_page = urllib.request.urlopen( ROMURL )
    soup = BeautifulSoup( html_page , 'html.parser' )
    for link in soup.find_all("a"):
        print( link.get('href') )

# ___ End Main _____________________________________________________________________________________________________________________________


# === Spare Parts ==========================================================================================================================



# ___ End Spare ____________________________________________________________________________________________________________________________
