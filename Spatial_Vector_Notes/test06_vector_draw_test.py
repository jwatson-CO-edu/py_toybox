#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division # MUST be run before all other expressions , including docstrings!

"""
FILENAME.py
James Watson , 2017 MONTHNAME , Written on Spyder 3 / Python 2.7 , Template Version 2017-10-26
A_ONE_LINE_DESCRIPTION_OF_THE_FILE
"""

# === Init =================================================================================================================================

# ~~ Imports ~~
# ~ Standard ~
import time , os
from math import cos , sin , acos , asin , tan , atan2 , radians , degrees , hypot , pi
# ~ Special ~
import numpy as np
# ~ Local ~
from SpatialVectorRobot import vec_randrange , rot_matx_ang_axs , z_rot
from OGLshapes import Vector_OGL , OGL_App

# ~~ Aliases & Shortcuts ~~
endl    = os.linesep # - Line separator
infty   = float('inf') # Infinity
EPSILON = 1e-8 # ------- A very small number below the precision we care about

# ___ End Init _____________________________________________________________________________________________________________________________

class CircleOrbit:
    
    def __init__( self , center , radius ):
        """ Set all the params for a circular orbit """
        self.center    = center
        self.radius    = radius
        
    def __call__( self , theta ):
        """ Return the point in R3 for angle 'theta' """
        offset = np.dot( z_rot( theta ) , [ self.radius , 0 , 0 ] )
        # print "Offset:" , offset
        return np.add( self.center , offset )

# === Main =================================================================================================================================

numVectors  = 30
dimRange    = [ -1   ,  1 ]
perturb     = [ -0.1 ,  0.1 ]
vecCoords   = []
vecDrawList = []
camOrbit    = CircleOrbit( [ 0 , 0 ,0 ] , 2.0 )
dTheta      = pi / 90.0

Vector_OGL.set_vec_props( LineWidth           = 4.00 ,
                          ArrowWidthFraction  = 0.08 ,
                          ArrowLengthFraction = 0.20 )

if __name__ == "__main__":
    # 1. Create a collection of random vectors in a set volume
    for i in xrange( numVectors ):
        head = vec_randrange( [ dimRange for j in xrange(3) ] )
        tail = vec_randrange( [ dimRange for j in xrange(3) ] )
        vecCoords.append( [ tail , np.subtract( head , tail ) ] )
        vecDrawList.append( Vector_OGL( *vecCoords[-1] ) )
    
    # 2. Create an OGL window
    window = OGL_App( vecDrawList , caption = "Vector Drawing Test" )
    
    # 3. Set the camera to look at the collection
    window.set_camera( [ 2 , 2 , 2 ] , [ 0 , 0 , 0 ] , [ 0 , 0 , 1 ] )
    
    theta = 0
    
    # 4. Draw & Display
    while not window.has_exit:        
        for vec in vecDrawList:
            vec.set_origin_displace( np.add( vec.origin , vec_randrange( [ perturb for j in xrange(3) ] ) ) ,
                                     np.add( vec.offset , vec_randrange( [ perturb for j in xrange(3) ] ) ) )
        theta += dTheta
        window.set_camera( camOrbit( theta ) , [ 0 , 0 , 0 ] , [ 0 , 0 , 1 ] )
        window.dispatch_events() # Handle window events
        window.on_draw() # Redraw the scene
        window.flip()

# ___ End Main _____________________________________________________________________________________________________________________________
