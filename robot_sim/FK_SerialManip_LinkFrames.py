#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-06-25

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
FK_SerialManip_LinkFrames.py , Built on Spyder for Python 2.7
James Watson, 2016 August
Testing representation of reference frames in the simplest implementation possible
"""

# == Init Environment ==================================================================================================
import sys, os.path
SOURCEDIR = os.path.dirname(os.path.abspath(__file__)) # URL, dir containing source file: http://stackoverflow.com/a/7783326

def add_first_valid_dir_to_path(dirList):
    """ Add the first valid directory in 'dirList' to the system path """
    # In lieu of actually installing the library, just keep a list of all the places it could be in each environment
    loadedOne = False
    for drctry in dirList:
        if os.path.exists( drctry ):
            if drctry not in sys.path:
                sys.path.append( drctry )
                print 'Loaded:', str(drctry)
            else:
                print "Already in sys.path:", str(drctry)
            loadedOne = True
            break
    if not loadedOne:
        print "None of the specified directories were loaded", dirList
        
# List all the places where the research environment could be
add_first_valid_dir_to_path( [ '/media/jwatson/FILEPILE/Python/ResearchEnv',
                               '/home/jwatson/regrasp_planning/researchenv',
                               'F:\Python\ResearchEnv',
                               'E:\Python\ResearchEnv',
                               '/media/mawglin/FILEPILE/Python/ResearchEnv'] )

from ResearchEnv import * # Load the custom environment
from ResearchUtils import Vector # Geometry # Not importing all becuase of collisions with Vector.Frame and Tkinter.Frame
from robotAnim import * # Cheap Iso
from ResearchUtils.DebugLog import *

# == End Init ==========================================================================================================

set_dbg_lvl(1) # Debugging creation of robot from DH params

# DH Parameters and Joint Limits for the KUKA R6 R900
KUKADH = [ # This is the Hollerbach formulation
    {'alpha':   0.0, 'd':   0.0, 'a':    0.0, 'theta': None, 'type': None    }, # The -1 --> 0 transformation must be specified!
    {'alpha':  pi/2, 'd': 400.0, 'a':  -25.0, 'theta': None, 'type': 'rotary'},
    {'alpha':   0.0, 'd':   0.0, 'a': -455.0, 'theta': None, 'type': 'rotary'},
    {'alpha':  pi/2, 'd':   0.0, 'a':  -35.0, 'theta': None, 'type': 'rotary'},
    {'alpha': -pi/2, 'd': 420.0, 'a':    0.0, 'theta': None, 'type': 'rotary'},
    {'alpha':  pi/2, 'd':   0.0, 'a':    0.0, 'theta': None, 'type': 'rotary'},
    {'alpha':   0.0, 'd':  80.0, 'a':    0.0, 'theta': None, 'type': 'rotary'}
]

JNTLIM = [ # Joint Limits
    ( radians( 170) , radians(-170) ) ,
    ( radians(  45) , radians(-190) ) ,
    ( radians( 156) , radians(-120) ) ,
    ( radians( 185) , radians(-185) ) ,
    ( radians( 120) , radians(-120) ) ,
    ( radians( 350) , radians(-350) )
]

def robot_from_DH( specification , formulation='Hollerbach' ):
    """ Return a "stick-model" robot according to the DH parameters given in the 'specification' """
    linkRefs = [] # Chain of links that comprise the robot
    if formulation == 'Hollerbach':
        # NOTE: This differs slightly from the class formulation in that the -1 --> 0 transformation must be specified
        for jointNum , transform in enumerate(specification):
            dbgLog(1 , "Creating Link" , jointNum)
            rotations = []
            if specification[jointNum]['type'] == 'rotary':
                rotations.append( Rotation([0,0,1],0) )
            elif specification[jointNum]['type'] == None:
                pass
            else:
                raise ValueError("robot_from_DH: Joint type " + specification[jointNum]['type'] + " is not supported")
            if jointNum > 0 and specification[jointNum - 1]['alpha'] != 0:
                rotations.append( Vector.Quaternion.k_rot_to_Quat( [1,0,0] , specification[jointNum - 1]['alpha'] ) )
            
            if jointNum > 0:
                origin = [ specification[jointNum - 1]['a'] , 0.0 , specification[jointNum - 1]['d'] ] # [:] # Origin is at the end of the last link
            else:
                origin = [0.0 , 0.0 , 0.0]
                
            segments = []

            if specification[jointNum]['d'] != 0.0:
                segments.append( Vector.Segment( [ [ 0.0 , 0.0 , 0.0 ] , [ 0.0 , 0.0 , specification[jointNum]['d'] ] ] ) )
            if specification[jointNum]['a'] != 0.0:
                segments.append( Vector.Segment( [ [ 0.0 , 0.0 , specification[jointNum]['d'] ] , 
                                                   [ specification[jointNum]['a'] , 0.0 , specification[jointNum]['d'] ] ] ) )
            
            dbgLog(1, "Link",jointNum )
            dbgLog(1, "\tOrigin:",origin )
            dbgLog(1, "\tRotations",*[str(rot) for rot in rotations] )
            dbgLog(1, "\tSegments",*[str(seg) for seg in segments] )
            
            currLink = Vector.LinkFrame( origin , rotations , *segments ) # build a link frame from the above specifications
            
            if jointNum > 0: # If this is not the first link, then this link is a subframe of the last link
                linkRefs[-1].attach_sub( currLink )
                # pass
            
            linkRefs.append( currLink )

        # Attach coordinate axes to each Frame            
        for jointNum , transform in enumerate(specification):
            if jointNum > 0:
                axes = Vector.Axes( Vector.Pose( [ transform['a'] , 0.0 , transform['d'] ], Vector.Quaternion.no_turn_quat() ) , 75 )
                linkRefs[jointNum].attach_sub( axes )

#        axes = Vector.Axes( Vector.Pose( [ -25 , 0.0 , 400] , Vector.Quaternion.no_turn_quat() ) , 100 )
#        linkRefs[1].attach_sub( axes )
            
    # TODO: Implement support for other DH parameter formulations
    else:
        raise ValueError( "robot_from_DH: The formulation \"" + formulation + "\" is not recognized!" )
        
    return linkRefs # Assume the last frame is the effector frame        
        
robotChain = robot_from_DH( KUKADH ) # Generate the robot from the DH parameters

def add_tool_frame( chain ):
    """ Append a tool frame with tool axes to the end of the robot chain """
    toolFrame = Vector.Axes( Vector.Pose( [0,0,0] , Vector.Quaternion.no_turn_quat()  ) , 75 )
    chain[-1].attach_sub( toolFrame )
    chain.append( toolFrame )
    
add_tool_frame( robotChain )
print len(robotChain)
print Vector.Axes.count

for link in robotChain:
    print link.__class__, len(link.subFrames), len(link.objs)
    # Chain appears to be populated!

#    [X] Compare the above specification to the first successful implementation
#    [X] Compare the above specification to the class specification
#    [X] Produce a series of properly connected LinkFrames from the above specification - Needs testing
#    {X} Display axes at the appropriate places for the Hollerbach formulation
#    [X] Figure out why the tool frame axes do not move


foo = LinkFrameApp() # init the app object
##
attach_geometry( robotChain[0] , foo.canvas ) # attach all the segments to the canvas
color_all( robotChain[0] , 'white' ) # Color all the links white
attach_transform( robotChain[0] , chain_R3_scrn ) # Assign the Cheap Iso projection to all drawable objects
##
for segment in foo.staticSegments: # Assign the Cheap Iso projection to the world axes
    segment.transform = chain_R3_scrn

def segment_update_function( linkChain ):
    """ Set all the joint angles in 'linkChain' to those specified in 'angleList' """
    def segment_update( angleList ):
        for jntDex in range(1, len(linkChain)-1): # The first frame is from the lab to the robot
            linkChain[jntDex].set_theta( angleList[jntDex-1] )
    return segment_update
    
foo.calcFunc = segment_update_function( robotChain )
foo.simFrame = robotChain[0]
foo.rootWin.after(100,foo.run)  
foo.rootWin.mainloop()
   
   
# == Abandoned Code ==



# == End Abandoned ==
