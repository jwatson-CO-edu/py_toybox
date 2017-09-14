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
# from marchhare.Vector import vec_random_range # Not in the CARGO environment!
# ~ Local ~

# ~~ Aliases & Shortcuts ~~
import __builtin__ # URL , Add global built-ins to be used by all scripts in the environment: https://stackoverflow.com/a/4698550
__builtin__.endl = os.linesep # Line separator
__builtin__.infty = float('inf') # Infinity
__builtin__.EPSILON = 1e-8 # A very small number below the precision we care about

# == End Init ==============================================================================================================================

"""
~~~~~~ NOTES ~~~~~~

* What is an Action?: It is a set of efforts, each corresponding to a degree of freedom of the agent ( zero / no-op allowed )
    - Can be used to represent on / off == 1 / 0
    - Can be used to represent direction of DOF -N , +N
    - IDLE == 0
                      
      DOF_1    , ... , DOF_n               
    [ Effort_1 , ... , Effort_n ]
     
* Do all actions give positive value? No
* Are all actions relevant to the problem? No
* What is the search space?: All actions
    - What is the dimensionality of all actions: Number of DOFs times number of efforts that the DOF can output ( may be continuous )

* Variable Q-Learning
    - Assemble actions on the fly , starting with a random assortment of actions
    - Do the best with the tools you have first
    - Try to invent new tools second
    - This might take even longer than regular Q-learning
    
* Variable Action
    - Is it possible for the machine to choose between discrete efforts and situation-dependent , parametric efforts?  How to do this?
    - Does it make sense to give actions unique names?
    
* Variable State
    - How to arrive at the internal states that I specified by hand?
    - What is the advantage of having the machine invent internal states for itself?
"""


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
[ ] 3. Simple learning algo with human-prepared output actions
    |Y| Define an action
    |Y| Create a set of actions , Course
    |Y| Look at Q-Learning and SARSA and decide which one to use ( The ONLINE one ) - COMPLETE , Either of these can be online / offline , 
        Choosing SARSA first because it is simpler
    | | Implement Learning
    | | Compare SARSA and Q-Learning
    | | Create a set of actions , Fine
    | | See if this results in improvement , How much longer does it take to train?
    | | Learning on random actions with decay
[ ] 4. Re-read VSM idea notes
[ ] 5. Neural transitions
[ ] 6. Bug Dynamics
    | | Bug { momentum , acceleration , and damping } 
    
"""



# == Utility Functions ==

def clamp_val( val , lims ): # >>> MH
    """ Return a version of val that is clamped to the range [ lims[0] , lims[1] ] , inclusive """
    if val < lims[0]:
        return lims[0]
    if val > lims[1]:
        return lims[1]
    return val

def vec_random_range( dim , limLo , limHi ): # <<< MH
    """ Return a vector in which each element takes on a random value between 'limLo' and 'limHi' with a uniform distribution """
    rtnVec = []
    randVec = vec_random( dim )
    span = abs( limHi - limLo )
    for elem in randVec:
        rtnVec.append( elem * span + limLo )
    return rtnVec

def vec_random_limits( dim , limits ): # <<< MH
    """ Return a vector in which each element takes on a random value between 'limits[i][0]' and 'limits[i][1]' with a uniform distribution """
    rtnVec = []
    randVec = vec_random( dim )
    for i , elem in enumerate( randVec ):
        span = abs( limits[i][1] - limits[i][0] )
        rtnVec.append( elem * span + limits[i][0] )
    return rtnVec

def vec_check_limits( vec , limits ): # <<< MH
    """ Return True of 'vec' [x_0 ... x_N] falls within 'limits' ( ( x0min , x0max ) ... ( xNmin , xNmax ) ) , otherwise false """
    for i , lim in enumerate(limits):
        if vec[i] < lim[0]:
            return False
        elif vec[i] > lim[1]:
            return False
    return True

# == End Utility ==


class ActionSpec( object ):
    """ Contains the constraints and requirements for an agent action in the problem """
    
    def __init__( self , dimension , dimLims ):
        """ Create a specification with the given dimensionality and limits """
        if len( dimLims ) != dimension:
            raise ValueError( "ActionSpec.__init__: Limits did not mention the given dimensionality!" )
        self.dims = dimension
        self.lims = dimLims
                
    def check_action( self , action ):
        """ Return 'True' if 'action' has the correct dimensionality and limits """
        if isinstance( action , ( list , tuple ) ):
            if len( action ) == self.dims:
                return vec_check_limits( action , self.lims )
            else:
                return False
        else:
            return False
        
    def gen_rand_action( self ):
        """ Generate a random action that meets the specification """
        return vec_random_limits( self.dims , self.lims )
        
    
class Action:
    """ Container , Represents the completely defined action for the agent """
    
    def __init__( self , efforts = [] ):
        self.efforts  = efforts
        

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


# ~~ Bug Model Parameters ~~
_BUGSPEED   = 0.5 # Distance that the bug moves , per step
# _BUGACTIONS = [ "LEFT" , "RGHT" , "IDLE" ] # Actions available to the bug
_BUGACTIONS = [ [ -_BUGSPEED ] , [  _BUGSPEED ] , [ 0.0 ] ] # Actions available to the bug


class BugAgent( object ):
    """ Agent with two sensors that can slide right or slide left """
    
    def __init__( self , world , x ):
        self.env = world
        self.state = x
        self.internal = None
        self.sensorOffsets = [ -0.5 ,  0.5 ]
        self.sensors = []
        self.action = _BUGACTIONS[2]
        for sensDex , offset in enumerate( self.sensorOffsets ):
            self.sensors.append( Sensor( self.state + self.sensorOffsets[ sensDex ] , 
                                         self.env.get_intensity_at ) )
            
    def observe( self ):
        """ Populate sensors with observations """
        for sensDex , sensor in enumerate( self.sensors ):
            sensor.observation = sensor.observe( self.state + self.sensorOffsets[ sensDex ] )
        print [ sensor.observation for sensor in self.sensors ]
        self.interpret()
    
    def interpret( self ):
        """ Translate the sensor readings into an internal state """ # 
        if self.sensors[0].observation > self.sensors[1].observation:
            self.internal = 0 # self.action = _BUGACTIONS[0]
        elif self.sensors[0].observation < self.sensors[1].observation:
            self.internal = 1 # self.action = _BUGACTIONS[1]
        else:
            self.internal = 2 # self.action = _BUGACTIONS[2]
    
    def act( self ):
        """ Make decision based on the data """
        self.action = _BUGACTIONS[ self.internal ]
    
    def tick( self ):
        """ Observe and act """
        self.observe() # Retrieve data from the world
        self.act() # Act on the data


def transition_model( env , agent , state , action ):
    """ Get s' = T(s,a) """
    name = agent.__class__.__name__
    if name == "BugAgent":
        if len( action ) == 1:
            return clamp_val( state + action[0] , env.slideLimits ) 
        else:
            raise ValueError( "transition_model: " + str( action ) + " was of the wrong dimensionality for " + str( name ) + "!" )
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
        # 3. Update agents , Apply transitions resulting from actions
        self.agent.tick()
        print "Agent Action  :" , self.agent.action
        self.agent.state = transition_model( self , self.agent , self.agent.state , self.agent.action )
        # 4. Assign Value
        # 5. Agent learning

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
    
        plt.plot( lightPos , linewidth = 2.0 )
        plt.plot( agentPos , linewidth = 2.0 )
        
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