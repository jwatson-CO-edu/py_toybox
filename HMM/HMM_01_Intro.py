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
    [ ] Forward Algorithm
    [ ] Forward-Backward Algorithm
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

# ~~ Transition Model ~~

T = { True:  0.7 , # The probability it rains today given that it rained yesterday
      False: 0.3 } # The probability it rains today given that it did not rain yesterday

# ~~ Sensor Model ~~

P_uT_rT = 0.9 # ------- The probability an umbrella is seen     given rain    
P_uT_rF = 0.2 # ------- The probability an umbrella is seen     given no rain 
P_uF_rT = 1 - P_uT_rT # The probability an umbrella is not seen given rain    
P_uF_rF = 1 - P_uT_rF # The probability an umbrella is not seen given no rain 

#       r = F   | r = T
Z = [ [ P_uF_rF , P_uF_rT ] , # u = F
      [ P_uT_rF , P_uT_rT ] ] # u = T
# P( u | r ) = Z[u][r]

ALLSTATES = [ True , False ]; # Possible States: { Raining , Not Raining }
ALLOBSERV = [ True , False ]; # Possible Observations: { Umbrella , No Umbrella }

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

# CS 6300 HW#08 Problem 2 is very helpful for forward algo
def Forward_Algorithm( Zseq ):
    """ Recover the state sequence from the observation sequence using the Forward Algorithm """
    rainDist = { True: 0.5 , False: 0.5 } # Begin with an even distribution of rainy and nonrainy days
    for i , observ_i in enumerate( Zseq ):
        
        # 1. Determine the probability of rain_1 = T at Time 1 given the evidence of an observation 1 at Time 1
        """ In order to do this, we need to build expressions for the probability of Rain given evidence and probability of Not Rain given
        evidence, solve for \alpha, and evaluate the expression """        
        # P(  state | observ ) = ( \alpha ) * P( observ |  state ) * P(  state )
        alphP_rT_Oi = Z[ observ_i ][ True ]  * rainDist[ True ]
        # P( -state | observ ) = ( \alpha ) * P( observ | -state ) * P( -state )
        alphP_rF_Oi = Z[ observ_i ][ False ] * rainDist[ False ]    
        alpha = 1.0 / ( alphP_rT_Oi + alphP_rF_Oi )
        
        P_rT_Oi = alpha * alphP_rT_Oi
        P_rF_Oi = alpha * alphP_rF_Oi
        
        # 1. Determine the overall probability of Rain , P(r)
        """ The probability of rain_1 = T at Time 1 is the sum of the (transition probabilities from all possible Time 0 states to rain_1 = T) 
        times (the associated probabilities of the states at Time 0). At Time 0 the probability of states has some initial distribution. """        
        rainProbTot = 0
        for prevState in ALLSTATES:
            rainProbTot += T[ prevState ] * rainDist[ prevState ] # Matches the initial distribution at time 1
        
        
        # FIXME : START HERE
        
        # A. The probability of observation, given Rain
        
        # FIXME : DOCUMENT EXPRESSION
        # B. The Probability of observation, given Not-Rain
        # FIXME : DOCUMENT EXPRESSION
        

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