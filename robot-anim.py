#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-06-25

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
robot-anim.py , Built on Spyder for Python 2.7
James Watson, 2016 July
Simple graphics for a simple stick-figure robot
"""

"""
  == NOTES ==
* For now, points and segments will have persistence on the canvas and will be moved on repaint. (That is what Tkinter 
  is made for anyway) For the purposes of this stick robot, world objects will not be subject to rapid creation/distruction 
  or occlusion. Those are concerns for a more complex sim on another day!

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
            sys.path.append( drctry )
            print 'Loaded', str(drctry)
            loadedOne = True
            break
    if not loadedOne:
        print "None of the specified directories were loaded"
# List all the places where the research environment could be
add_first_valid_dir_to_path( [ '/home/jwatson/regrasp_planning/researchenv',
                               '/media/jwatson/FILEPILE/Python/ResearchEnv' ] )
from ResearchEnv import * # Load the custom environment
from ResearchUtils.Vector import *

# == End Init ==========================================================================================================

def lab_to_screen_transform(*labFrameCoords):
    """ Transform natural coordinates in the lab frame to coordinates on the screen display """
    if len(labFrameCoords) == 1:
        pass # FIXME: complete this function
    else:
        for coord in labFrameCoords:
            pass
    return None

def polr_2_cart(polarCoords):
    """ Convert polar coordinates [radius , angle (radians)] to cartesian [x , y]. Theta = 0 is UP """
    return [ polarCoords[0] * sin(polarCoords[1]) , polarCoords[0] * cos(polarCoords[1]) ]
    # TODO : Look into imaginary number transformation and perform a benchmark
    
def cart_2_polr(cartCoords):
    pass # FIXME: define this for the sake of symmetry, I feel like I have written this many times!

"""
== Cheap Isometric Projection ==
Three dimensions are represented in a simple isomertic projection. The silhouette of a cube takes on the shape of a regular
hexagon. This is so that no scaling or complex transformations have to take place. All axes have an equal scale in this
representation. Transforming coordinates from R3 to Cheap Iso is just a matter of multiplying each of the components by
a 2D non-orthogonal "basis vector" and adding the resultants.
"""
def cheap_iso_transform(R3triple):
    """ Transform R3 coordinates into a cheap isometric projection in 2D """
    # NOTE: You will need to scale thye resulting coords according to the need of the application
    return np.multiply( cheap_iso_transform.xBasis , R3triple[0] ) + \
           np.multiply( cheap_iso_transform.yBasis , R3triple[1] ) + \
           np.multiply( cheap_iso_transform.zBasis , R3triple[2] ) # Do I need to use 'np_add'?

cheap_iso_transform.zBasis = [ 0.0 , 1.0 ] 
cheap_iso_transform.xBasis = polr_2_cart( [1.0 , 2.0/3 * pi] )
cheap_iso_transform.yBasis = polr_2_cart( [1.0 , 1.0/3 * pi] )