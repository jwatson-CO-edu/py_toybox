#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
HMM_01_Intro.py , Built on Wing 101 IDE for Python 2.7
James Watson, YYYY MONTHNAME , Template Version: 2018-05-10
A ONE LINE DESCRIPTION OF THE FILE

Dependencies: numpy
"""
__progname__ = "PROGRAM NAME"
__version__  = "YYYY.MM.DD"
"""  
~~~ Developmnent Plan ~~~
[ ] ITEM1
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
# ~~ Special ~~
import numpy as np
# ~~ Local ~~
prepend_dir_to_path( PARENTDIR ) # Add local MARCHHARE to path
from marchhare.marchhare import sep


# ~~ Constants , Shortcuts , Aliases ~~
EPSILON = 1e-7
infty   = 1e309 # URL: http://stackoverflow.com/questions/1628026/python-infinity-any-caveats#comment31860436_1628026
endl    = os.linesep

# ~~ Script Signature ~~
def __prog_signature__(): return __progname__ + " , Version " + __version__ # Return a string representing program name and verions


# ___ End Init _____________________________________________________________________________________________________________________________


# === Main Application =====================================================================================================================

# = Program Functions =



# _ End Func _

# = Program Vars =



# _ End Vars _

if __name__ == "__main__":
    print __prog_signature__()
    termArgs = sys.argv[1:] # Terminal arguments , if they exist

# ___ End Main _____________________________________________________________________________________________________________________________


# === Spare Parts ==========================================================================================================================



# ___ End Spare ____________________________________________________________________________________________________________________________