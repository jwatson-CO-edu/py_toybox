#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
HMM_01_Intro.py , Built on Wing 101 IDE for Python 2.7
James Watson, 2018 May , Template Version: 2018-05-10
Investigate Hidden Markov Models with a toy problem

Dependencies: numpy
"""
__progname__ = "HMM Investigation"
__version__  = "2018.05"
"""  
~~~ Developmnent Plan ~~~
[Y] Generate a sequence of states and observations - COMPLETE , Simple problem with 2 states and 2 observations
[ ] Use Viterbi to recover sequence
[ ] Use Particle filter to recover sequence
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
from marchhare.MathKit import flip_weighted


# ~~ Constants , Shortcuts , Aliases ~~
EPSILON = 1e-7
infty   = 1e309 # URL: http://stackoverflow.com/questions/1628026/python-infinity-any-caveats#comment31860436_1628026
endl    = os.linesep

# ~~ Script Signature ~~
def __prog_signature__(): return __progname__ + " , Version " + __version__ # Return a string representing program name and verions


# ___ End Init _____________________________________________________________________________________________________________________________


# === Main Application =====================================================================================================================

"""
Example:
    * Security Guard resides in an underground facility
    * Wants to determine the probability of rain given whether the Director brings an umbrella
"""

# = Program Vars =

T = { True:  0.7 , # The probability it rains today given that it rained yesterday
      False: 0.3 } # The probability it rains today given that it did not rain yesterday

Z = { True:  0.9 , # The probability an umbrella is seen today given rain today
      False: 0.2 } # The probability an umbrella is seen today given no rain today

# _ End Vars _

# = Program Functions =

def generate_state_sequence( T , N , initState = None ):
    """ Generate a sequence of 'N' sequential states in {True,False} according to the given transition model """
    if initState == None:
        initState = flip_weighted( 0.5 )
    rtnSeq = [ initState ]
    for i in xrange( N ):
        rtnSeq.append( flip_weighted( T[ rtnSeq[-1] ] ) )
    return rtnSeq

def generate_observ_sequence( stateSeq , Z ):
    """ Generate a sequence of noisy observations given a sequence of ground-truth states """
    rtnSeq = []
    for state in stateSeq:
        rtnSeq.append( flip_weighted( Z[ state ] ) )
    return rtnSeq

# _ End Func _



if __name__ == "__main__":
    print __prog_signature__()
    termArgs = sys.argv[1:] # Terminal arguments , if they exist
    
    groundTruth  = generate_state_sequence( T , 10 )
    observations = generate_observ_sequence( groundTruth , Z )
    
    Xdist = { True: 0.5 , False: 0.5 } # Begin with an even distribution of rainy and nonrainy days
    
    print "Truth:" , groundTruth
    print "Obsrv:" , observations

# ___ End Main _____________________________________________________________________________________________________________________________


# === Spare Parts ==========================================================================================================================



# ___ End Spare ____________________________________________________________________________________________________________________________