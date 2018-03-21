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
from marchhare.Vector import vec_random_range 
from marchhare.VectorMath.SpatialVectorRobot import rot_matx_ang_axs , z_rot
from marchhare.OGLshapes import Vector_OGL , OGL_App , Icosahedron_Reg

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

camOrbit    = CircleOrbit( [ 0 , 0 ,0 ] , 3.5 )
dTheta      = pi / 180.0

if __name__ == "__main__":
    # 1. Create an icosahedron
    icos = Icosahedron_Reg( 2 , pos = [ 0 , 0 , 0 ] )
    
    # 2. Create an OGL window
    window = OGL_App( [ icos ] , caption = "Vector Drawing Test" )
    
    # 3. Set the camera to look at the collection
    window.set_camera( [ 2 , 2 , 2 ] , [ 0 , 0 , 0 ] , [ 0 , 0 , 1 ] )
    
    theta = 0
    
    # 4. Draw & Display
    while not window.has_exit:
        theta += dTheta
        window.set_camera( camOrbit( theta ) , [ 0 , 0 , 0 ] , [ 0 , 0 , 1 ] )
        window.dispatch_events() # Handle window events
        window.on_draw() # Redraw the scene
        window.flip()

# ___ End Main _____________________________________________________________________________________________________________________________
