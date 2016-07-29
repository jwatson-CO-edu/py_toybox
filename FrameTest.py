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

"""
  == TODO ==
* Give this application a display window
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
#                             Link3 does not have an extent

#foo = Segment()
#bar = Frame()

Link1 = Vector.Frame( [0.0 , 0.0 , 0.0] , 
                      Rotation([0,0,1],0), 
                      Segment( pCoords=[ [0.0 , 0.0 , 0.0] , Span1  ] ) )
#               
print Link1.objs
#               
Link2 = Vector.Frame( Span1 , 
                      Rotation([0,1,0],0) , 
                      Segment( [ [0.0 , 0.0 , 0.0] , Span2  ] ) )
#               
Link2.parent = Link1 # this one is not currently used
Link1.subFrames.append( Link2 ) # this connection is important for downstream transformations
#
print Link2.objs
print Link1.subFrames
#
Link3 = Vector.Frame( Span2 , 
                      Rotation([0,1,0],0) )
               
Link2.subFrames.append( Link3 )
        
def attach_geometry(rootFrame, pCanvas):
    """ Traverse geometry from the root frame to the all subframes, recursively, attaching all drawable geometry to canvas """
    for obj in rootFrame.objs:
        obj.attach_to_canvas( pCanvas )
    for frame in rootFrame.subFrames:
        attach_geometry( frame , pCanvas )
        
def attach_transform( rootFrame, pTransform ):
    """ Traverse geometry from the root frame to the all subframes, recursively, attaching all drawable geometry to canvas """
    for obj in rootFrame.objs:
        obj.transform = pTransform
    for frame in rootFrame.subFrames:
        attach_transform( frame , pTransform )
        
def color_all(rootFrame, pColor):
    """ Traverse geometry from the root frame to the all subframes, recursively, setting all graphics to 'pColor' """
    for obj in rootFrame.objs:
        obj.set_color( pColor )
    for frame in rootFrame.subFrames:
        color_all( frame , pColor )
        
def jnt_refs_serial_chain( rootLink ):
    """ Return a list of references to Rotations that correspond to each of the links of the manipulator """
    # NOTE: This function assumes that each frame has only one subframe
    jntRefs = [] # [ rootLink.orientation ]
    currLink = rootLink
    
    while len(currLink.subFrames) > 0:
        print "At link:", currLink
        print "This link has",len(currLink.subFrames),"subframes"
        
        jntRefs.append( currLink.orientation ) # TODO: Find out if this attaches the reference or a copy
        currLink = currLink.subFrames[0]
    return jntRefs
        
foo = FrameApp() # init the app object

attach_geometry( Link1 , foo.canvas ) # attach all the segments to the canvas
color_all( Link1 , 'white' )
attach_transform( Link1 , chain_R3_scrn )

for segment in foo.staticSegments:
    segment.transform = chain_R3_scrn

armJoints = jnt_refs_serial_chain( Link1 )
print "Found", len(armJoints), "arm joints:", armJoints

def segment_update( angleList ):
    """ Set all the joint angles to those specified in 'angleList' """
    global armJoints # Do I need this?
    for jntDex , joint in enumerate(armJoints):
        joint.set_theta( angleList[jntDex] )
    
foo.calcFunc = segment_update
foo.simFrame = Link1
    
foo.run()    
    
# == Abandoned Code ==

#def tokenize_with_separator(rawStr,separator,evalFunc=str):
    #""" Return a list of tokens taken from 'rawStr' that is partitioned with 'separator', transforming each token with 'evalFunc' """
    #tokens = [] # list of tokens to return
    #currToken = '' # the current token, built a character at a time
    #for char in rawStr: # for each character of the input string
        #if not char.isspace(): # if the current char is not whitespace, process
            #if not char == separator: # if the character is not a separator, then
                #currToken += char # accumulate the char onto the current token
            #else: # else the character is a separator, process the previous token
                #tokens.append( evalFunc( currToken ) ) # transform token and append to the token list
                #currToken = '' # reset the current token
        ## else is whitespace, ignore
    #if currToken: # If there is data in 'currToken', process it
        #tokens.append( evalFunc( currToken ) ) # transform token and append to the token list
    #return tokens

#def eval_to_float(tokenStr):
    #""" Evaluate a token string and attempt conversion to float """
    #return float( eval( tokenStr ) )

#looping = True # Flag for whether to continue running
## thetaList = [0.0 for i in range(10)]

#while looping: # If the looping flag is set True
    #print endl
    #cmd = raw_input('Angles or Command: ')
    #if cmd == 'q': # User quit, set looping flag False
        #print "Quit"
        #looping = False
    #elif cmd[0] == 'e': # Evaluate
        #try:
            #print eval(cmd[2:]) # Assume the user left a space after the "e", If there is no space - error likely
        #except BaseException as err:
            #print "Your command was not understood!:" , err
    #else: # else assume the user has specified angles
        #print endl
        #angles = tokenize_with_separator(cmd,',',eval_to_float) # Thise will throw an error if input string is malformed
        #print angles
        #Link1.orientation.set_theta(angles[0])
        #print "Link1 theta was set to",Link1.orientation.theta # Link1 theta was set to 1.57079632679
        #Link2.orientation.set_theta(angles[1])
        #print "Link2 theta was set to",Link2.orientation.theta
        #Link1.transform_contents() # Initiate transformation at the root node

#def REP():
    #""" [R]ead , [E]val , [P]rint , Loop is someone else's problem! """
    #print endl
    #cmd = raw_input('Angles or Command: ')
    #if cmd == 'q': # User quit, set looping flag False
        #print "Quit"
    #elif cmd[0] == 'e': # Evaluate
        #try:
            #print eval(cmd[2:]) # Assume the user left a space after the "e", If there is no space - error likely
        #except BaseException as err:
            #print "Your command was not understood!:" , err
    #else: # else assume the user has specified angles
        #print endl
        #angles = tokenize_with_separator(cmd,',',eval_to_float) # Thise will throw an error if input string is malformed
        #print angles
        #Link1.orientation.set_theta(angles[0])
        #print "Link1 theta was set to",Link1.orientation.theta # Link1 theta was set to 1.57079632679
        #Link2.orientation.set_theta(angles[1])
        #print "Link2 theta was set to",Link2.orientation.theta
        #Link1.transform_contents() # Initiate transformation at the root node

# == End Abandoned ==