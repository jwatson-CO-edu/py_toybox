#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

__progname__ = "FSM_Example.py"
__version__  = "2018.11" 
__desc__     = "An example Finite State Machine , https://www.python-course.eu/finite_state_machine.php"
"""
James Watson , Template Version: 2018-05-14
Built on Wing 101 IDE for Python 2.7

Dependencies: numpy
"""


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

# ~~ Constants , Shortcuts , Aliases ~~
EPSILON = 1e-7
infty   = 1e309 # URL: http://stackoverflow.com/questions/1628026/python-infinity-any-caveats#comment31860436_1628026
endl    = os.linesep

# ~~ Script Signature ~~
def __prog_signature__(): return __progname__ + " , Version " + __version__ # Return a string representing program name and verions

# ___ End Init _____________________________________________________________________________________________________________________________


# === Main Application =====================================================================================================================

# = Program Classes =

"""  
~~~ Finite State Machine ~~~

~~ State ~~
name : __ Uppercase string identifying the state
handler : Function that runs every update when the machine is in this state

~~ State Handler ~~
( newState , cargo ) = handler( cargo )
~ Inputs ~
    cargo : Input to the state, Handler uses this to determine the next state
~ Outputs ~ 
    newState : The next state
    cargo : __ Data generated in this state to be used in the next
    
~~ Transitions ~~
The next state is set by the current state

"""

class StateMachine:
    """ Simplest Finite State Machine (FSM) """
    # Author: Bernd Klein , https://www.python-course.eu/finite_state_machine.php
    
    def __init__( self ):
        """ Establish data structures that will be used by the FSM """
        self.handlers   = {} # -- Update functions associated with each state
        self.startState = None #- Initial state
        self.endStates  = [] # -- List of end state names
        self.state      = None #- Current state , Set by previous handler ( Current state is stored here, so not storing current handler )
        self.active     = False # Flag for whether the FSM is running

    def add_state( self , name , handler , end_state = False ):
        """ Add a state to the FSM and enforce name formatting , Add to end state list if designated """
        name = name.upper()
        self.handlers[ name ] = handler
        # If the user has designated this as an end state, then add to end states
        if end_state:
            self.endStates.append( name )

    def set_start( self , name ):
        """ Set the initial state of the FSM """
        self.startState = name.upper()

    def init_bgn_end_cond( self ):
        """ Check the beginning and ending conditions and init state """
        # NOTE: This function should be run before the first time 'update' is run
        # Attempt to set the current update function.  If it fails, assume that the user did not set up the FSM correctly
        try:
            # Check for the update function associated with the starting state
            handler = self.handlers[ self.startState ]
            self.active = True
        except:
            # If there was no function with this name 'startState', Then ask the user to set a start state
            raise InitializationError( "must call .set_start() before .run()" )
        # Warn the user if there were no end states 
        if not self.endStates:
            raise  InitializationError( "At least one state must be an end_state" )        

    def run( self , cargo ):
        """ Execute FSM , Given input 'cargo' """
        # NOTE: No external event loop , This function assumes that the FSM should run autonomously until an end condition is reached
        # Check and set begin and end states , Init
        self.init_bgn_end_cond()
        handler = self.handlers[ self.startState ]
    
        # Run until exit
        while True:
            # 1. Run this state's update function
            ( newState , cargo ) = handler( cargo )
            # 2. Determine if an ending state was reached as a result of this state. If so, report and exit loop
            if newState.upper() in self.endStates:
                print "reached" , newState , "which is an end state"
                break 
            # else an exit state was not reached, set the handler for the next state
            else:
                handler = self.handlers[ newState.upper() ]   
                
    def update( self , cargo ):
        """ Set and run the handler for this state , Set the next state """
        # NOTE: This function assumes an event loop paradigm, and that 'update' will be called by client code
        # NOTE: This function assumes that input data 'cargo' is provided by client code
        
        # 1. Fetch the update function for the current state
        handler = self.handlers[ self.state ]
        # 2. Run this state's update function
        ( newState , cargo ) = handler( cargo )        
        
        # FIXME: START HERE , WRITE AN UPDATE ASSUMING CLIENT CODE DRIVES LOOP AND PROVIDES INPUT DATE
        
        return { 'state': self.state , 'output': cargo }

# _ End Classes _ 

# = Program Functions =

def start_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word == "Python":
        newState = "Python_state"
    else:
        newState = "error_state"
    return (newState, txt)

def python_state_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word == "is":
        newState = "is_state"
    else:
        newState = "error_state"
    return (newState, txt)

def is_state_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word == "not":
        newState = "not_state"
    elif word in positive_adjectives:
        newState = "pos_state"
    elif word in negative_adjectives:
        newState = "neg_state"
    else:
        newState = "error_state"
    return (newState, txt)

def not_state_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word in positive_adjectives:
        newState = "neg_state"
    elif word in negative_adjectives:
        newState = "pos_state"
    else:
        newState = "error_state"
    return (newState, txt)

def neg_state(txt):
    print("Hallo")
    return ("neg_state", "")

# _ End Func _

# = Program Vars =

positive_adjectives = ["great","super", "fun", "entertaining", "easy"]
negative_adjectives = ["boring", "difficult", "ugly", "bad"]

# _ End Vars _

if __name__ == "__main__":
    print __prog_signature__()
    termArgs = sys.argv[1:] # Terminal arguments , if they exist
    
    m = StateMachine()
    m.add_state( "Start"        , start_transitions        )
    m.add_state( "Python_state" , python_state_transitions )
    m.add_state( "is_state"     , is_state_transitions     )
    m.add_state( "not_state"    , not_state_transitions    )
    m.add_state( "neg_state"    , None , end_state = 1     )
    m.add_state( "pos_state"    , None , end_state = 1     )
    m.add_state( "error_state"  , None , end_state = 1     )
    m.set_start( "Start" )
    m.run( "Python is great" )
    m.run( "Python is difficult" )
    m.run( "Perl is ugly" )    

# ___ End Main _____________________________________________________________________________________________________________________________


# === Spare Parts ==========================================================================================================================



# ___ End Spare ____________________________________________________________________________________________________________________________
