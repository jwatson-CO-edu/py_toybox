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
            # if specification[jointNum + 1]['type'] == 'rotary':
            if specification[jointNum]['type'] == 'rotary':
                rotations.append( Rotation([0,0,1],0) )
            elif specification[jointNum]['type'] == None:
                pass
            else:
                # raise ValueError("robot_from_DH: Joint type " + specification[jointNum + 1]['type'] + " is not supported")
                raise ValueError("robot_from_DH: Joint type " + specification[jointNum]['type'] + " is not supported")
            # if specification[jointNum]['alpha'] != 0:
            if jointNum > 0 and specification[jointNum - 1]['alpha'] != 0:
                # rotations.append( Vector.Quaternion.k_rot_to_Quat( [1,0,0] , transform['alpha'] ) )
                rotations.append( Vector.Quaternion.k_rot_to_Quat( [1,0,0] , specification[jointNum - 1]['alpha'] ) )
            # if (jointNum < len(specification) - 1):
            #if (jointNum > 0):
            
            
            
            if jointNum > 0:
                origin = [ specification[jointNum - 1]['a'] , 0.0 , specification[jointNum - 1]['d'] ] # Origin is at the end of the last link
                # origin = [ specification[jointNum]['a'] , 0.0 , specification[jointNum]['d'] ] # Origin is at the end of the last link
            else:
                origin = [0.0 , 0.0 , 0.0]
            segments = []
            # if specification[jointNum + 1]['d'] != 0.0:
            if specification[jointNum]['d'] != 0.0:
                # segments.append( Vector.Segment( [ [ 0.0 , 0.0 , 0.0 ] , [ 0.0 , 0.0 , specification[jointNum + 1]['d'] ] ] ) )
                segments.append( Vector.Segment( [ [ 0.0 , 0.0 , 0.0 ] , [ 0.0 , 0.0 , specification[jointNum]['d'] ] ] ) )
            # if specification[jointNum + 1]['a'] != 0.0:
            if specification[jointNum]['a'] != 0.0:
                # segments.append( Vector.Segment( [ [ 0.0 , 0.0 , specification[jointNum + 1]['d'] ] , 
                segments.append( Vector.Segment( [ [ 0.0 , 0.0 , specification[jointNum]['d'] ] , 
                                                   # [ specification[jointNum + 1]['a'] , 0.0 , specification[jointNum + 1]['d'] ] ] ) )
                                                   [ specification[jointNum]['a'] , 0.0 , specification[jointNum]['d'] ] ] ) )
#            else:
#                origin = [ 0.0 , 0.0 , 0.0 ]
#                segments = [] # Nothing to paint, only locating the origin of the robot
            
            currLink = Vector.LinkFrame( origin , rotations , *segments ) # build a link frame from the above specifications
            if jointNum > 0: # If this is not the first link, then this link is a subframe of the last link
                linkRefs[-1].attach_sub( currLink )
            
            linkRefs.append( currLink ) 
            if len(linkRefs) == 6: break # TODO: ITERATIVE TROUBLESHOOTING            
            
        return linkRefs # Assume the last frame is the effector frame
    # TODO: Implement support for other DH parameter formulations
    else:
        raise ValueError( "robot_from_DH: The formulation \"" + formulation + "\" is not recognized!" )

robotChain = robot_from_DH( KUKADH )
for link in robotChain:
    print link.__class__, len(link.subFrames), len(link.objs)
    # Chain appears to be populated!

# TODO:
#    [X] Compare the above specification to the first successful implementation
#    [X] Compare the above specification to the class specification
#    [ ] Produce a series of properly connected LinkFrames from the above specification - Needs testing
#    { } Display axes at the appropriate places for the Hollerbach formulation



#EffectorFrame = Vector.Frame( Span2[:] , # There's no real need for this to be a LinkFrame
#                              Rotation([0,1,0],0) )
#               
## Link2.subFrames.append( Link3 )
#Link2.attach_sub( EffectorFrame )  
              
def jnt_refs_serial_chain( rootLink ):
    """ Return a list of references to Rotations that correspond to each of the links of the manipulator """
    # NOTE: This function assumes that each frame has only one subframe
    jntRefs = [] # [ rootLink.orientation ]
    currLink = rootLink
    
    while len(currLink.subFrames) > 0:
        print "At link:", currLink
        print "This link has",len(currLink.subFrames),"subframes"
        
        # jntRefs.append( currLink.orientation ) # TODO: Find out if this attaches the reference or a copy
        jntRefs.append( currLink ) # TODO: Find out if this attaches the reference or a copy
        currLink = currLink.subFrames[0]
    return jntRefs

foo = LinkFrameApp() # init the app object
##
attach_geometry( robotChain[0] , foo.canvas ) # attach all the segments to the canvas
color_all( robotChain[0] , 'white' )
attach_transform( robotChain[0] , chain_R3_scrn )
##
for segment in foo.staticSegments:
    segment.transform = chain_R3_scrn

def segment_update_function( linkChain ):
    """ Set all the joint angles in 'linkChain' to those specified in 'angleList' """
    def segment_update( angleList ):
        for jntDex in range(1, len(linkChain)-1): # The first frame is from the lab to the robot
            linkChain[jntDex].set_theta( angleList[jntDex-1] )
    return segment_update
    
foo.calcFunc = segment_update_function( robotChain )
foo.simFrame = robotChain[0]
##    
foo.rootWin.after(100,foo.run)  
foo.rootWin.mainloop()
    
# == Abandoned Code ==



# == End Abandoned ==