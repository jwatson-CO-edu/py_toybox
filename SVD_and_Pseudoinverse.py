#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
FILENAME.py , Built on Wing 101 IDE for Python 2.7
James Watson, YYYY MONTHNAME , Template Version: 2018-01-08
A ONE LINE DESCRIPTION OF THE FILE
URL: https://www.johndcook.com/blog/2018/05/05/svd/

Dependencies: numpy
"""
__progname__ = "PROGRAM NAME"
__version__  = "YYYY.MM.DD"
"""  
~~~ Developmnent Plan ~~~
[ ] Generate points in a parallelepiped
[ ] Investigate SVD of points
[ ] Investigate Pseudoinverse of points
"""

# === Init Environment =====================================================================================================================
import sys, os.path
SOURCEDIR = os.path.dirname( os.path.abspath( __file__ ) ) # URL, dir containing source file: http://stackoverflow.com/a/7783326

# ~~~ Imports ~~~
# ~~ Standard ~~
from math import pi , sqrt
# ~~ Special ~~
import numpy as np
# ~~ Local ~~

# ~~ Constants , Shortcuts , Aliases ~~
EPSILON = 1e-7
infty   = 1e309 # URL: http://stackoverflow.com/questions/1628026/python-infinity-any-caveats#comment31860436_1628026
endl    = os.linesep

# ~~ Script Signature ~~
def __prog_signature__(): return __progname__ + " , Version " + __version__ # Return a string representing program name and verions

# ___ End Init _____________________________________________________________________________________________________________________________


# === Main Application =====================================================================================================================

# = Program Functions =

def sample_in_hyperparallelepiped( N , corner , magBases ):
    """ Sample 'N' uniformly-distributed points in the 'hyperparallelepiped' with 'corner' and bases 'magBases' """
    # NOTE: 'magBases' also specifies the maximum extent beyond the corner for each dimension
    # NOTE: It is possible for the number of bases to differ from the number of dimensions
    
    # FIXME : START HERE!
    
    # 1. Enforce consisistent dimensionality
    # 2. For each i
    # 3. Start at corner
    # 4. For each dimension basis
    # 5. Sample along

# _ End Func _


# = Program Vars =



# _ End Vars _

if __name__ == "__main__":
    print __prog_signature__()
    termArgs = sys.argv[1:] # Terminal arguments , if they exist
    

# ___ End Main _____________________________________________________________________________________________________________________________


# === Spare Parts ==========================================================================================================================



# ___ End Spare ____________________________________________________________________________________________________________________________