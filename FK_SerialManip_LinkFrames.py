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
        print "None of the specified directories were loaded"
# List all the places where the research environment could be
add_first_valid_dir_to_path( [ '/media/jwatson/FILEPILE/Python/ResearchEnv',
                               '/home/jwatson/regrasp_planning/researchenv',
                               'F:\Python\ResearchEnv',
                               '/media/mawglin/FILEPILE/Python/ResearchEnv'] )

from ResearchEnv import * # Load the custom environment
from ResearchUtils import Vector # Geometry # Not importing all becuase of collisions with Vector.Frame and Tkinter.Frame
from robotAnim import * # Cheap Iso

# == End Init ==========================================================================================================

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

JNTLIM = [
    ( radians(170) , radians(-170) ),
    ( radians( 45) , radians(-190) ),
    ( radians(156) , radians(-120) ),
    ( radians(185) , radians(-185) ),
    ( radians(120) , radians(-120) ),
    ( radians(350) , radians(-350) )
]

def robot_from_DH( specification , formulation='Hollerbach' ):
    """ Return a "stick-model" robot according to the DH parameters given in the 'specification' """
    if formulation == 'Hollerbach':
        # NOTE: This differs slightly from the class formulation in that the -1 --> 0 transformation must be specified
        for jointNum , transform in enumerate(specification):
            rotations = [ Rotation([0,1,0],0) ]
            # FIXME: START HERE!
            currLink = LinkFrame( [ transform['a'] , 0.0 , transform['d'] ] , 
                                  [ Rotation( [0,0,1] , 0 ) ], 
                                  Segment( [ [0.0 , 0.0 , 0.0] , Span1[:] ] ) )
    else:
        raise ValueError( "robot_from_DH: The formulation \"" + formulation +"\" is not recognized!" )

# TODO:
#    [ ] Compare the above specification to the first successful implementation
#    [ ] Compare the above specification to the class specification
#    [ ] Produce a series of properly connected LinkFrames from the above specification
#    [ ] Place axes at the appropriate places for the Hollerbach formulation

Span1 = [ 100 ,   0 , 100 ] # extent of link 1 in its own frame
Span2 = [ 100 ,   0 ,   0 ] # extent of link 2 in its own frame
#                             Link3 does not have an extent


Link1 = Vector.LinkFrame( [ 0.0 , 0.0 , 0.0 ] , 
                          [ Rotation( [0,0,1] , 0 ) ], 
                          Segment( [ [0.0 , 0.0 , 0.0] , Span1[:] ] ) )
             
Link2 = Vector.LinkFrame( Span1[:] , 
                          [ Rotation([0,1,0],0) , Vector.Quaternion.k_rot_to_Quat( [1,0,0] , -pi/2 ) ] , 
                          Segment( [ [0.0 , 0.0 , 0.0] , Span2[:] ] ) )
             
# Link2.parent = Link1 # this one is not currently used
# Link1.subFrames.append( Link2 ) # this connection is important for downstream transformations
Link1.attach_sub( Link2 )

print Link2.objs
print Link1.subFrames

EffectorFrame = Vector.Frame( Span2[:] , # There's no real need for this to be a LinkFrame
                              Rotation([0,1,0],0) )
               
# Link2.subFrames.append( Link3 )
Link2.attach_sub( EffectorFrame )  
              
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
# 
#def link_report():
#    """ Report the link states for debugging """
#    print "Link2 Pose: " # FIXME: I don't think the Frames are broadcasting their poses to their objects
#       
#
foo = LinkFrameApp() # init the app object
#
attach_geometry( Link1 , foo.canvas ) # attach all the segments to the canvas
color_all( Link1 , 'white' )
attach_transform( Link1 , chain_R3_scrn )
#
for segment in foo.staticSegments:
    segment.transform = chain_R3_scrn
#
armJoints = jnt_refs_serial_chain( Link1 )
print "Found", len(armJoints), "arm joints:", armJoints
#
def segment_update( angleList ):
    """ Set all the joint angles to those specified in 'angleList' """
    #global armJoints # Do I need this?
    for jntDex , joint in enumerate(armJoints):
        joint.set_theta( angleList[jntDex] )
    
foo.calcFunc = segment_update
foo.simFrame = Link1
#    
foo.rootWin.after(100,foo.run)  
foo.rootWin.mainloop()
    
# == Abandoned Code ==



# == End Abandoned ==