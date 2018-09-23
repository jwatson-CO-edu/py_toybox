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
[ ] Use Viterbi to recover sequence , Build up theory using increasingly complex algos
    [Y] Forward Algorithm - COMPLETE , Consistently > 80% accurate!
    [ ] Backward Algorithm
    [ ] Forward-Backward Algorithm
    [ ] Viterbi Algorithm , Recover Sequence
    
[ ] Use Particle filter to recover sequence ( HMM_02_Intro.py )
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
from marchhare.marchhare import sep , enumerate_reverse , prepend
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

P_1T_0T = 0.7 # ------- The probability it rains         today given that it rained       yesterday
P_1T_0F = 0.3 # ------- The probability it rains         today given that it did not rain yesterday
P_1F_0T = 1 - P_1T_0T # The probability it does not rain today given that it rained       yesterday
P_1F_0F = 1 - P_1T_0F # The probability it does not rain today given that it did not rain yesterday

#       r  = F  | r  = T
T = [ [ P_1F_0F , P_1F_0T ] , # r' = F
      [ P_1T_0F , P_1T_0T ] ] # r' = T

# P( r' | r  ) = T[r'][r ]

# ~~ Sensor Model ~~

P_uT_rT = 0.9 # ------- The probability an umbrella is seen     given rain    
P_uT_rF = 0.2 # ------- The probability an umbrella is seen     given no rain 
P_uF_rT = 1 - P_uT_rT # The probability an umbrella is not seen given rain    
P_uF_rF = 1 - P_uT_rF # The probability an umbrella is not seen given no rain 

#       r = F   | r = T
Z = [ [ P_uF_rF , P_uF_rT ] , # u = F
      [ P_uT_rF , P_uT_rT ] ] # u = T
# P( u | r ) = Z[u][r]

ALLSTATES = [ False , True ]; # Possible States: { Not Raining , Raining }
ALLOBSERV = [ False , True ]; # Possible Observations: { No Umbrella , Umbrella }

# _ End Vars _

# = Program Functions =

def generate_state_sequence( T , N , initState = None ):
    """ Generate a sequence of 'N' sequential states in {True,False} according to the given transition model """
    # NOTE: This function assumes that 'N' >= 1
    if initState == None:
        initState = flip_weighted( 0.5 )
    rtnSeq = [ initState ]
    for i in xrange( N - 1 ):
        rtnSeq.append( flip_weighted( T[ True ][ rtnSeq[-1] ] ) )
    return rtnSeq

def generate_observ_sequence( stateSeq , Z ):
    """ Generate a sequence of noisy observations given a sequence of ground-truth states """
    rtnSeq = []
    for state in stateSeq:
        rtnSeq.append( flip_weighted( Z[ True ][ state ] ) )
    return rtnSeq

def argmax_dict( pDict ):
    """ Return the dictionary key with the greatest value """
    # NOTE: *Strongly* consider 'marchhare.marchhare.Counter' if it fits your use case!
    # NOTE: This function assumes that 'pDict' has at least one key-val pair
    # NOTE: This function assumes that all values in 'pDict' can be compared with inequalities
    # NOTE: If there are multiple keys with the max value, this function will return the last one encountered by the iterator. 
    #       Python does not guarantee order in dictionaries
    maxKey = pDict.keys()[0]
    maxVal = pDict.values()[0]
    for key , val in pDict.iteritems():
        if val >= maxVal:
            maxKey = key
            maxVal = val
    return maxKey

def seq_accuracy( nfrSeq , truSeq ):
    """ Calculate the accuracy of state inferences """
    # NOTE: This function assumes thate 'truSeq' and 'nfrSeq' are of equal length
    correctCount = 0
    seqLen = len( truSeq )
    for i in xrange( seqLen ):
        if truSeq[i] == nfrSeq[i]:
            correctCount += 1
    return correctCount / seqLen

# CS 6300 HW#08 Problem 2 is very helpful for forward algo
def Forward_Algorithm( Zseq ):
    """ Recover the state sequence from the observation sequence using the Forward Algorithm """
    rtnSeq = []
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
        
        PgivenOi = { True: P_rT_Oi , False: P_rF_Oi }
        
        # 2. Determine the overall probability of Rain , P(r)
        """ The probability of rain_1 = T at Time 1 is the sum of the (transition probabilities from all possible Time 0 states to rain_1 = T) 
        times (the associated probabilities of the states at Time 0). At Time 0 the probability of states has some initial distribution. """        
        # If there is a previous state to look at
        rainDist = { True: 0.0 , False: 0.0 } # Reset the distribution to 0
        for nextState in ALLSTATES:
            for currState in ALLSTATES:
                # P( next ) = P( next | state ) * P( state | observ )
                rainDist[ nextState ] += T[ nextState ][ currState ] * PgivenOi[ currState ]
        
        # 3. Infer the state for this timestep
        rtnSeq.append( ( argmax_dict( rainDist ) , ( PgivenOi[ True ] , PgivenOi[ True ] ) ) )
    return rtnSeq
        
# CS 6300 Lecture #20 HMM-1 very useful for this algo
def Backward_Algorithm( Zseq ):
    """ At each timestep, determine probability that the observation was emitted from each state """
    rtnSeq = []
    beta_T = 1
    beta_t = { False: [] , # Probability that Not-Raining was responsible for the observation at t
               True:  [] } # Probability that Raining     was responsible for the observation at t
    
    # 1. Build the beta_t(i) sequences, per state, per timestep
    for k in ALLSTATES:
        prepend( beta_t[ k ] , 1 )
    for t , z_t in enumerate_reverse( Zseq ):
        for i in ALLSTATES: # For every next state
            # 2. INIT beta_t[ i ] summation
            beta_ti = 0
            # beta_t[ i ] = Probability of the follow-on sequence of observations { z_{t+1} ... z_{T} } given the state x_t = i at time t
            for j in ALLSTATES: # Sum over possible next states
                # beta_t[ i ] = \sum_{j=1}^{N}(  beta_{t+1}[ j ] * P( x_{t+1} = i | x_{t} = j ) * P( z_t | x_t = j ) )
                beta_ti                       += beta_t[ j ][0]  * T[ i ][ j ]                  * Z[ z_t ][ j ]
            prepend( beta_t[ i ] , beta_ti )
      
    # return beta_t
    # beta_t[ i ] = Probability of the follow-on sequence of observations { z_{t+1} ... z_{T} } given the state x_t = i at time t
                
    # 2. Determine the most likely state at t by comparing beta_t(i)
    
    # FIXME : START HERE
    
    # 3. Determine the likelihood of the observation at time t

# _ End Func _



if __name__ == "__main__":
    print __prog_signature__()
    termArgs = sys.argv[1:] # Terminal arguments , if they exist
    
    groundTruth  = generate_state_sequence( T , 10 )
    observations = generate_observ_sequence( groundTruth , Z )
    fwdInferencs = Forward_Algorithm( observations )
    
    Xdist = { True: 0.5 , False: 0.5 } # Begin with an even distribution of rainy and nonrainy days
    
    print "Truth:" , groundTruth
    print "Obsrv:" , observations
    inferredStates = [ infer[0] for infer in fwdInferencs ]
    print "Forwd:" ,  inferredStates
    print "Accur:" , seq_accuracy( inferredStates , groundTruth )
    
    beta_t = Backward_Algorithm( observations )
    print ["{0:0.5f}".format(i) for i in beta_t[ False ]]  , len( beta_t[ False ] ) , sum( beta_t[ False ][:-1] ) 
    print ["{0:0.5f}".format(i) for i in beta_t[ True  ]] , len( beta_t[ True  ] ) , sum( beta_t[ True  ][:-1] ) 

# ___ End Main _____________________________________________________________________________________________________________________________


# === Spare Parts ==========================================================================================================================



# ___ End Spare ____________________________________________________________________________________________________________________________