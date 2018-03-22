#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division # MUST be run before all other expressions , including docstrings!

"""
GIF001_icos_draw_test.py
James Watson , 2018 March , Written on Spyder 3 / Python 2.7 , Template Version 2017-10-26
Animate and save a spinning icosahedron

Dependencies: numpy , pyglet , imageio , marchhare

NOTE , 2018-03-22: ERROR OCCURS WHILE RUNNING UNDER UBUNTU 16.04 , LAST THIRD OF THE ANIMATION RUNS AT A GREATLY INCREASED FRAMERATE
                   This does not currently happen under Windows 10
"""

"""
~~~ DEV PLAN ~~~
[Y] Save GIF on exit
"""

# === Init =================================================================================================================================

# ~~ Imports ~~
# ~ Standard ~
import time , os
from math import cos , sin , acos , asin , tan , atan2 , radians , degrees , hypot , pi
# ~ Special ~
import numpy as np
import pyglet
import imageio
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
		
def ensure_dir( dirName ):
	""" Create the directory if it does not exist """
	if not os.path.exists( dirName ):
		os.makedirs( dirName )

# === Main =================================================================================================================================

# == Program Vars ==
        
# ~ FLAGS ~
_SAVEGRAPHICS = False # Set to True to create an animated GIF of the generated graphics

# ~ Generation Settings ~
camOrbit    = CircleOrbit( [ 0 , 0 ,0 ] , 3.5 ) # Camera will circle the given point in the X-Y plane at the given radius
dTheta      = pi / 90.0 # ----------------------- Radians to advance per frame
totalFames  = int( ( 2 * pi ) / dTheta  ) # ----- Number of frames that will bring the animation to its initial configuration ( GIF loop )

# ~ File Settings ~
prefix      = "frame_" # Prefix for source frames
postfix     = ".png" # - File extension for source frames ( pyglet can only save as PNG without PILLOW )
frmCount    = 0 # ------ Counting var to keep track of frames
subDirName  = "output" # Subdir for all output files

# ~ Animation Settings ~
FPS         = 24 # -------------- Frame Per Second
outFileName = "icoshearyou.gif" # Name of the output file

# __ End Vars __

if __name__ == "__main__":
    
    # 0. Erase previous frames
    if _SAVEGRAPHICS:
        prevFrames = os.listdir( subDirName )
        for pFrame in prevFrames:
            fullName = os.path.join( subDirName , pFrame )
            if fullName.endswith( ".png" ):
                os.remove( fullName )
    
    # === GRAPHICS CREATION ================================================================================================================
    
    # 1. Create an icosahedron
    icos = Icosahedron_Reg( 2 , pos = [ 0 , 0 , 0 ] )
    
    # 2. Create an OGL window
    window = OGL_App( [ icos ] , caption = "ICOSHEARYOU" )
    
    # 3. Set the camera to look at the collection
    window.set_camera( [ 2 , 2 , 2 ] , [ 0 , 0 , 0 ] , [ 0 , 0 , 1 ] )
    
    theta = 0
    ensure_dir( subDirName )

    # 4. Draw & Display
    while not window.has_exit:
        theta += dTheta
        window.set_camera( camOrbit( theta ) , [ 0 , 0 , 0 ] , [ 0 , 0 , 1 ] )
        window.dispatch_events() # Handle window events
        window.on_draw() # Redraw the scene
        window.flip()
        
        # ___ END GRAPHICS _________________________________________________________________________________________________________________
        
        if _SAVEGRAPHICS:
            # Save one complete rotation
            if frmCount <= totalFames:
                frmCount += 1
                if frmCount > 1:
                    fName = os.path.join( subDirName , prefix + str( frmCount ).zfill( 4 ) + postfix )
                    pyglet.image.get_buffer_manager().get_color_buffer().save( fName )
                    
    # 5. Create an animated GIF after the graphics window has been closed by the user
    if _SAVEGRAPHICS:
        images = [] # Buffer for each frame
        for subdir , dirs , files in os.walk( subDirName ):
            for file in files:
                file_path = os.path.join( subdir , file )
                if file_path.endswith( ".png" ):
                    images.append( imageio.imread( file_path ) )
        			
        imageio.mimsave( os.path.join( subDirName , outFileName ) , images , fps = FPS )

# ___ End Main _____________________________________________________________________________________________________________________________
