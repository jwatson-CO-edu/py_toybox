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

# == Init ==================================================================================================================================

# ~~ Imports ~~
# ~ Standard ~
import time , os
from math import cos , sin , acos , asin , tan , atan2 , radians , degrees , hypot , pi
from random import choice
# ~ Special ~
import numpy as np
from marchhare.Vector import vec_random_range
# ~ Local ~

# ~~ Aliases & Shortcuts ~~
import __builtin__ # URL , Add global built-ins to be used by all scripts in the environment: https://stackoverflow.com/a/4698550
__builtin__.endl = os.linesep # Line separator
__builtin__.infty = float('inf') # Infinity
__builtin__.EPSILON = 1e-8 # A very small number below the precision we care about

# == End Init ==============================================================================================================================

"""
~~~~~~ Problem Statement ~~~~~~
1. Given a set of available outputs, how might an agent create a set of actions that are appropriate for the task?
    * Might these actions be parameterized?
    * Might these parameters be matched to learned features?

~~~~~~ DEVELOPMENT PLAN ~~~~~~
[Y] 1. Slider Bug Environment - COMPLETE
    |Y| Light position as a function of time , f(t) - COMPLETE , tested
    |Y| Light intensity as a function of light position - COMPLETE , tested
    |Y| Step function , Light intensity evolution over time - COMPLETE , tested
    |Y| Transition model for BugAgent
[Y] 2. Bug - COMPLETE
    |Y| Fixed sensors , X2 - COMPLETE
    |Y| Available outputs , { LEFT , RGHT , IDLE } - COMPLETE
    |Y| Sense - COMPLETE
[ ] 3. Q-Learning
    | | Standard Q-learning with human-prepared output actions
    | | Random Q-Learning with decaying output actions
[ ] 4. Re-read VSM idea notes
[ ] 5. Neural transitions
[ ] 6. Bug Dynamics
    | | Bug { momentum , acceleration , and damping } 
    
"""

"""
~~~~~~ NOTES ~~~~~~

FIXME: WHAT IS THE SIMPLEST WAY TO EXPRESS THIS PROBLEM? ARE MODES ABSOLUTELY NECESSARY TO EXPRESS IT? - NO , left, right, and idle can be
       expressed as a single value that represents the desired speed in a line

* What is an Action?: It is a set of outputs corresponding to every degree of freedom, each output consisting of a mode and a parameter
                      ( zero / no-op allowed )
                      
      DOF_1              , ... , DOF_n               
    [ ( Mode X , param ) , ... , ( Mode X , param ) ]
    

    
* Do all actions give positive value? No
* Are all actions relevant to the problem? No
* What is the search space?: All actions
    - What is the dimensionality of all actions: Number of DOFs times number of configurations that those DOFs can assume

* Variable Q-Learning
    - Assemble actions on the fly , starting with a random assortment of actions
    - Do the best with the tools you have first
    - Try to invent new tools second
    - This might take even longer than regular Q-learning
"""

class OutputSpec:
    """ One DOF output for an agent , consists of an action and a parameter """
    
    def __init__( self , modeSet , outputRange ):
        """ Represents one action-parameter pair """
        if isinstance( DOFset , ( list , tuple ) ):
            self.actions = tuple( actionSet )
        else:
            raise ValueError( "OutputSpec.__init__: 'actionSet' must be an iterable, got " + str( outputRange ) )
        if not isinstance( outputRange , ( list , tuple ) ) or len( outputRange ) != 2 or outputRange[0] > outputRange[1]:
            raise ValueError( "OutputSpec.__init__: 'outputRange' must be an iterable of two elements defining a range, got " + str( outputRange ) )
        else:
            self.paramRange = tuple( outputRange )
        
    def check_output( self , action , output ):
        """ Check that the given output is valid """
        if action in self.actions and output >= self.paramRange[0] and output <= self.paramRange[1]:
            return True
        else:
            return False
        
    def rand_output( self ):
        """ Get a random output actionlet """
        return ( choice( self.actions ) , vec_random_range( 1 , *self.paramRange )  )
        
class Action( object ):
    """ Represents the complete action state for the agent """
    
    def __init__( self ):
        self.selector = []
        self.outputs  = []

# == Utility Functions ==

def clamp( val , lims ):
    """ Return a version of val that is clamped to the range [ lims[0] , lims[1] ] , inclusive """
    if val < lims[0]:
        return lims[0]
    if val > lims[1]:
        return lims[1]
    return val

# == End Utility ==

class Sensor:
    """ A device for obtaining certain information from the environment """
    
    def __init__( self , state = None , observFunc = None ):
        self.state = state
        self.observation = None
        if observFunc:
            self.observe = observFunc
        else:
            self.observe = self.dummy_observe
            
    def dummy_observe( self , state ):
        """ Dummy observation function , does nothing """
        return 0
    
    def set_state( self , x ):
        self.state = x


class BugAgent( object ):
    """ Agent with two sensors that can slide right or slide left """
    
    def __init__( self , world , x ):
        self.env = world
        self.state = x
        self.sensorOffsets = [ -0.5 ,  0.5 ]
        self.sensors = []
        self.action = "IDLE"
        for sensDex , offset in enumerate( self.sensorOffsets ):
            self.sensors.append( Sensor( self.state + self.sensorOffsets[ sensDex ] , 
                                         self.env.get_intensity_at ) )
            
    def observe( self ):
        """ Populate sensors with observations """
        for sensDex , sensor in enumerate( self.sensors ):
            sensor.observation = sensor.observe( self.state + self.sensorOffsets[ sensDex ] )
        print [ sensor.observation for sensor in self.sensors ]
    
    def act( self ):
        """ Make decision based on the data """
        if self.sensors[0].observation > self.sensors[1].observation:
            self.action = "LEFT"
        elif self.sensors[0].observation < self.sensors[1].observation:
            self.action = "RGHT"
        else:
            self.action = "IDLE"
    
    def tick( self ):
        """ Observe and act """
        self.observe() # Retrieve data from the world
        self.act() # Act on the data

# ~~ Bug Model Parameters ~~
_BUGACTIONS = [ "LEFT" , "RGHT" , "IDLE" ] # Actions available to the bug
_BUGSPEED   = 0.5 # Distance that the bug moves , per step

bugOutSpec = OutputSpec( _BUGACTIONS , [ -_BUGSPEED ,  _BUGSPEED ] )



def transition_model( env , agent , state , action ):
    """ Get s' = T(s,a) """
    name = agent.__class__.__name__
    if name == "BugAgent":
        if action in _BUGACTIONS:
            s_prime = state
            if action == "LEFT":
                s_prime = clamp( state - _BUGSPEED , env.slideLimits ) 
            elif action == "RGHT":
                s_prime = clamp( state + _BUGSPEED , env.slideLimits )
            elif action == "IDLE":
                pass
            return s_prime
        else:
            raise ValueError( "transition_model: " + str( action ) + " is not an action recognized by the transition model!" )
    else:
        raise ValueError( "transition_model: " + str( name ) + " is not a class recognized by the transition model!" )

class SliderBugEnv( object ):
    """ Slider Bug Environment - For testing an agent with only two actions available """
    
    def __init__( self ):
        self.agent       = None # ------------------------------- Reference to the agent that lives in the slider environment , world must exist first
        self.slideSide   = 10 # --------------------------------- One-sided range of each slider
        self.slideLimits = [ -self.slideSide , self.slideSide ] # Limits of both the light and the bug sliders
        self.lightPos    = 0.0 # -------------------------------- Current position of the light
        self.lightMax    = 100 # -------------------------------- Maximum intensity of the light
        self.t           = 0.0 # -------------------------------- Current time
        self.ticLen      = 0.05 # ------------------------------- Amount of time to elapse each step
        self.litePosFunc = self.lightFunc_sin # ----------------- Position of the light as a function of the current time
        self.liteIntFunc = self.liteI_invSqr # ------------------ Intensity of the light at the specified postion , given the current light pos
        
    def lightFunc_sin( self , t ):
        """ Light position as a sine function of 't' , Default """
        return self.slideSide * sin( t )
    
    def liteI_invSqr( self , x , x_Light ):
        """ Get the light intensity at position 'x' givent the light position 'x_Light' """
        return min( self.lightMax , self.lightMax / abs( x - x_Light )**2 ) # Divide the max intensity by the square of the distance between point and light pos
        
    def get_intensity_at( self , x ):
        """ Get the light intensity at state 'x' , given the present state of the light """
        return self.liteIntFunc( x , self.lightPos )
    
    def tick( self ):
        """ Run one simulation step """
        # 1. Advance time
        self.t += self.ticLen 
        # 2. Update environment
        self.lightPos = self.litePosFunc( self.t )
        print "Light position: {0:6.2f}".format( self.lightPos ) , "  ,  Light intensity at 0 pos: {0:6.2f}".format( 
                self.liteIntFunc( 0 , self.lightPos )
        ) , 
        # 3. Update agents
        self.agent.tick()
        print "Agent Action  :" , self.agent.action
        self.agent.state = transition_model( self , self.agent , self.agent.state , self.agent.action )


# == Main ==================================================================================================================================

if __name__ == "__main__":
    
    LightEnv = SliderBugEnv()
    LightEnv.agent = BugAgent( LightEnv , 0.0 )
    
    lightPos = []
    agentPos = []
    
    for i in xrange( 100 ):
        LightEnv.tick()
        lightPos.append( LightEnv.lightPos )
        agentPos.append( LightEnv.agent.state )
        
    if 1:
        import matplotlib.pyplot as plt
    
        plt.plot( lightPos )
        plt.plot( agentPos )
        
        plt.show()

# == End Main ==============================================================================================================================



# === Spare Parts ==========================================================================================================================

#"""
# == NOTES ==
#There are internal statestransition_determ
#There are external states
#There are features of the external states
#There are actions
#
# == LOG ==
#2016-11-24: For now, not asking Node or Graph to keep track of all the objects that it contains, keep model simple like 6225 until collisions
#            become important, or the the environment has to otherwise broadcast information to the agent. Then it might be useful to add agents
#            to nodes.
#            * COUNTERPOINT: Why not just have agents keep track of their state, and always ask the world for information about states and 
#                            transitions. Would that make things more efficient if only occupied states were calculated? This would also 
#                            eliminate the need to manage the double container<-->contained pointers of Node<-->Agent
#"""
#
#class Topic(object):
#    """ A message board for holding sequential states """
#    
#    def __init__( self ):
#        """ Set up the data Queue and list of callbacks """
#        self.data = Queue()
#        self.state = None
#	
#    def publish( self , msg ):
#        """ Push message to the Queue """
#        self.data.push( msg )
#	
#    def pop( self ):
#        """ Pop message from the Queue and send to all callbacks """
#        if not self.data.is_empty():
#            self.state = self.data.pop()
#	
#    def changed( self ):
#        """ Return true if there is data waiting in the Queue, otherwise return False """
#        return self.data.is_empty()
#
#
#class VSM_Graph(Graph):
#    """ Holds the VSM , Intermediary between the decision graph and the problem simulator """
#
#    def __init__( self , simulator = None , pRootNode = None ):
#        """ Create a VSM graph with connections to the problem simulator """
#        Graph.__init__( self , rootNode = pRootNode )
#        self.probSim = simulator # Simulator of state transitions for the problem
#        
#    def simulate_sa( self , state , action ):
#        """ Ask the simulator for the result of a state-action pair """
#        return self.probSim.transition( state , action )
#        
# 
## TODO: Figure out if there is some kind of DSL needed to construct arbitrary actions       
#
#class VSM_State( Node ):
#    """ Graph node for a VSM network """
#    
#    def __init__( self , graph = None ):
#        super( VSM_State , self ).__init__( pGraph = graph )
#        
#    def get_action( self , agent ):
#        """ EMPTY: Get the action for this state """
#        return None
#
#    def next_state( self , agent , action ):
#        """ EMPTY: Choose a next state for the agent """
#        return None
#
## <0> Implement the simplest robot, go north
#
#class VSM_Agent(TaggedObject):
#    """ A single agent in a shared-VSM swarm """
#    
#    def __init__( self , initState = None ):
#        self.state = initState # Current state pointer
#        self.nextState = None #  Next state assigned by the VSM
#        
#    def tick( self ):
#        """ Calc actions for this timestep """
#        return self.state.get_action( self )
#
#
#if __name__ == "__main__":
#    
#    # Set up a simple grid world
#    tinyWorld = GridGraph( 3 , 3 )
#    for node in tinyWorld.nodes: print node.alias , 
#    print
#    
#    
#    ant = VSM_Agent(  )
#    
#    decisionG = Graph()
#    world = GridGraph( 3 , 3 ) # Create a 3x3 grid world , von Neumann neighborhood
#    temp = VSM_State( decisionG )
#    temp.connect_to( temp , pDir=True )
#    temp.get_action = lambda agent: 'NT'
#    temp.next_state = lambda agent , state: temp
#    decisionG.add_node( temp )
#    print temp.get_action( ant )
#    for i in xrange(4):
#        print temp.next_state( ant , 'NT' )
#        print world.transition_determ( ( 1 , 1 ) , temp.get_action( ant ) )
    
# === End Spare ============================================================================================================================