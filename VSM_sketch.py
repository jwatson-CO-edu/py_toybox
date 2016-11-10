#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-09-05

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
VSM_sketch.py , Built on Spyder for Python 2.7
James Watson, 2016 October
Quick sketch of the Variable State Machine, A flexible decision process for AI
"""

# == Init Environment =================================================add_node========================================================= 140 char ==
import sys, os.path
SOURCEDIR = os.path.dirname(os.path.abspath(__file__)) # URL, dir containing source file: http://stackoverflow.com/a/7783326

def first_valid_dir(dirList):
    """ Return the first valid directory in 'dirList', otherwise return False if no valid directories exist in the list """
    rtnDir = False
    for drctry in dirList:
        if os.path.exists( drctry ):
			rtnDir = drctry 
			break
    return rtnDir
        
def add_first_valid_dir_to_path(dirList):
    """ Add the first valid directory in 'dirList' to the system path """
    # In lieu of actually installing the library, just keep a list of all the places it could be in each environment
    validDir = first_valid_dir(dirList)
    print __file__ , "is attempting to load a path ...",
    if validDir:
        if validDir in sys.path:
            print "Already in sys.path:", validDir
        else:
            sys.path.append( validDir )
            print 'Loaded:', str(validDir)
    else:
        raise ImportError("None of the specified directories were loaded") # Assume that not having this loaded is a bad thing
# List all the places where the research environment could be
add_first_valid_dir_to_path( [ '/media/jwatson/FILEPILE/ME-6225_Motion-Planning/Assembly_Planner/ResearchEnv' , 
                               '/home/jwatson/regrasp_planning/src/researchenv',
                               '/media/jwatson/FILEPILE/Python/ResearchEnv',
                               'F:\Python\ResearchEnv',
                               'E:\Python\ResearchEnv',
                               '/media/mawglin/FILEPILE/Python/ResearchEnv' ] )

# ~~ Libraries ~~
# ~ Standard Libraries ~
# ~ Special Libraries ~
# ~ Local Libraries ~
from ResearchEnv import * # Load the custom environment, this also loads UCBerkeleyUtil
from ResearchUtils.Graph_Lite import *

# == End Init ================================================================================================================== 140 char ==

# "Graph.py" has become really heavy. It's time to get back to the bare bones of what works

"""
There are internal states
There are external states
There are features of the external states
There are actions
"""

class Topic(object):
    """ A message board for holding sequential states """
    
    def __init__( self ):
        """ Set up the data Queue and list of callbacks """
        self.data = Queue()
        self.state = None
	
    def publish( self , msg ):
        """ Push message to the Queue """
        self.data.push( msg )
	
    def pop( self ):
        """ Pop message from the Queue and send to all callbacks """
        if not self.data.is_empty():
            self.state = self.data.pop()
	
    def changed( self ):
        """ Return true if there is data waiting in the Queue, otherwise return False """
        return self.data.is_empty()


class VSM_State( Node ):
    """ Graph node for a VSM network """
    
    def __init__( self ):
        super( VSM_Node , self ).__init__()
        
    def get_action( self , agent ):
        """ EMPTY: Get the action for this state """
        return None

    def next_state( self , agent ):
        """ EMPTY: Choose a next state for the agent """
        return None

# <0> Implement the simplest robot, go north

class VSM_Agent(TaggedObject):
    """ A single agent in a shared-VSM swarm """
    
    def __init__( self , initState = None ):
        self.state = initState # Current state pointer
        self.nextState = None #  Next state assigned by the VSM
        
    def tick( self ):
        """ Calc actions for this timestep """
        return self.state.get_action( self )


if __name__ == "__main__":
    
    # Set up a simple grid world
    tinyWorld = GridGraph( 3 , 3 )
    for node in tinyWorld.nodes: print node.alias , 
    print
    
    