#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-06-25

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
FrameTest.py , Built on Spyder for Python 2.7
James Watson, 2016 July
Testing representation of reference frames in the simplest implementation possible, find out what is going wrong
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


Span1 = [ 100 ,   0 , 100 ] # extent of link 1 in its own frame
Span2 = [ 100 ,   0 ,   0 ] # extent of link 2 in its own frame
Span3 = [ 100 ,   0 ,   0 ] # extent of link 3 in its own frame
#                             Link4 does not have an extent


Link1 = Vector.LinkFrame( [ 0.0 , 0.0 , 0.0 ] , 
                          [ Rotation( [0,0,1] , 0 ) ], 
                          Segment( [ [0.0 , 0.0 , 0.0] , Span1[:] ] ) )
             
Link2 = Vector.LinkFrame( Span1[:] , 
                          [ Rotation([0,0,1],0) , Vector.Quaternion.k_rot_to_Quat( [1,0,0] , -pi/2 ) ] , 
                          Segment( [ [0.0 , 0.0 , 0.0] , Span2[:] ] ) )
                          
Link3 = Vector.LinkFrame( Span2[:] , 
                          [ Rotation([0,0,1],0) , Vector.Quaternion.k_rot_to_Quat( [1,0,0] , pi/2 ) ] , 
                          Segment( [ [0.0 , 0.0 , 0.0] , Span3[:] ] ) )
             
# Link2.parent = Link1 # this one is not currently used
# Link1.subFrames.append( Link2 ) # this connection is important for downstream transformations
Link1.attach_sub( Link2 )

print Link2.objs
print Link1.subFrames
               
# Link2.subFrames.append( Link3 )
Link2.attach_sub( Link3 ) 

EffectorFrame = Vector.Frame( Span3[:] , # There's no real need for this to be a LinkFrame
                              Rotation([0,1,0],0) ) 

Link3.attach_sub( EffectorFrame ) 
              
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