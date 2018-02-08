#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
tiger_door.py , Built on Wing 101 IDE for Python 2.7
James Watson, 2018 February , Template Version: 2018-01-08
Implement and simulate the Tiger Door POMDP Problem

Dependencies: numpy
"""
__progname__ = "Tiger Door"
__version__  = "2018.02.06"

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

# ~~~ Problem Statement ~~~


# ~~~ Problem Setup ~~~
ACTIONS = set( range(3) ) # { 0: Listen , 1: Open Left , 2: Open Right }
STATES  = set( range(2) ) # { S0: Tiger Left , S1: Tiger Right }
REWARD  = {}
for state in STATES:
    for action in ACTIONS:
        if action == 0:
            r =   -1
        elif state + 1 == action:
            r = -100
        else:
            r =   10
        REWARD[ ( state , action ) ] = r
    

# ~~ Belief ~~
# Belief state: Probability of S0 vs S1 being true underlying state
belief = {}
for s in STATES:
    belief[ s ] = 1.0 / len( STATES ) # Initial belief state: p(S0) = p(S1) = 0.5

# ~~ Policy ~~
# Policy \pi is a map from Belief [ 0 , 1 ] to Action { 0: Listen , 1: Open Left , 2: Open Right }


class DoorPair:
    """ A pair of doors that either has a tiger in the Right or Left Door , But this cannot be observed directly """
    
    def __init__( self , tiger = "L" ):
        """ Create a door and store the tiger information """
        self.tiger = tiger
        
    def door_with_tiger( self ):
        """ Return the door that has the tiger """
        return self.tiger
    
def take_observation( door , observationModel ):
    """ Return an observation that simulates listening 'door' , given an 'observationModel' """
    pass

def reward_for_action( belief , action ):
    """ The expected reward is the reward for acting in a state times the expectation of being in that state, like Expectimax. """
    # r( b , a ) = \sum_{s}( b[s] * r( s , a ) )
    reward_ba = 0.0
    for s in STATES:
        reward_ba += belief[s] * REWARD[ ( s , action ) ]
    return reward_ba

# === Main Application =====================================================================================================================

# = Program Vars =





# _ End Vars _

if __name__ == "__main__":
    print __prog_signature__()
    termArgs = sys.argv[1:] # Terminal arguments , if they exist
    
    print "Belief:" , belief
    

# ___ End Main _____________________________________________________________________________________________________________________________


# === Spare Parts ==========================================================================================================================



# ___ End Spare ____________________________________________________________________________________________________________________________