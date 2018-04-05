#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division # MUST be run before all other expressions , including docstrings!

"""
GIF003_Mobius.py
James Watson , 2018 April , Written on Spyder 3 / Python 2.7 , Template Version 2017-10-26
Flags riding on a rail forming a Mobius strip

Dependencies: numpy , pyglet , imageio , marchhare , GIFtools

NOTE , 2018-03-22: ERROR OCCURS WHILE RUNNING UNDER UBUNTU 16.04 , LAST THIRD OF THE ANIMATION RUNS AT A GREATLY INCREASED FRAMERATE
                   This does not currently happen under Windows 10
                   
Process: [Y] 0. Move previous optimized output to "Gallery" directory
         [Y] 1. Move functions from previous work to "GIFtools.py" , or appropriate MARCHHARE modules
         [ ] 2. Generate & Record in Windows (Python)
         [ ] 3. Optimize GIF in Linux (GIFsicle)
         [ ] 4. Verify (Browser)
         [ ] 5. Post
"""

"""
~~~ DEV PLAN ~~~
[ ] Mobius Track
[ ] Query track for vertex positions
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
from pyglet.gl import ( GL_LINES , glColor3ub , GL_TRIANGLES , glTranslated , glRotated , glMatrixMode )
# ~ Local ~
from marchhare.marchhare import flatten_nested_sequence , ensure_dir , build_sublists_by_cadence
from marchhare.Vector import vec_random_range , vec_unit , vec_mag , linspace_endpoints
from marchhare.VectorMath.SpatialVectorRobot import rot_matx_ang_axs , z_rot
from marchhare.OGLshapes import Vector_OGL , OGL_App , Icosahedron_Reg , OGLDrawable
from GIFtools import CircleOrbit 

# ~~ Aliases & Shortcuts ~~
endl    = os.linesep # - Line separator
infty   = float('inf') # Infinity
EPSILON = 1e-8 # ------- A very small number below the precision we care about

# ___ End Init _____________________________________________________________________________________________________________________________


# == Helper Functions ==

def circle_arc_3D( axis , center , radius , beginMeasureVec , theta , N ):
    """ Return points on a circular arc about 'axis' at 'radius' , beginning at 'beginMeasureVec' and turning 'theta' through 'N' points """
    thetaList = np.linspace( 0 , theta , N )
    
    # FIXME : START HERE

# __ End Helper __


# == class MobiusTrack ==

class MobiusTrack( object ):
    """ A loop of track consisting of "one" rail parrallel to itself such that following opposite sides traces out a Mobius strip """
    
    def __init__( self , origin , diameter , pointsPerUnit = 100 ):
        """ Create a track with a certain origin point and circle diameter """
        # Goal: Complete circuit that ends where it began, such that opposite points are across from each other as the "two" tracks
        self.allPts = [ origin[:] ]
        
        # ~~ There are 16 sections ~~
        # ~ Sections 1-3 ~ : Back Top Track
        backLen = pi * diameter * 3 / 2
        backDir = [ 1 , 0 , 0 ]
        backTopEnd = np.add( origin , np.multiply( backDir , backLen ) )
        self.allPts.extend( linspace_endpoints( origin , backTopEnd , 3 * pointsPerUnit )[1:] )
        
# __ End MobiusTrack __
        
        

# === Main =================================================================================================================================

# == Program Vars ==

# ~ FLAGS ~
_SAVEGRAPHICS = False # Set to True to create an animated GIF of the generated graphics
#                       Be patient for the save process to finish after graphics window exit 'X' is clicked

# ~ Generation Settings ~
scale       = 0.65
camOrbit    = CircleOrbit( [ 0 , 0 , 0 ] , 1.5 * scale , 1 * scale ) # Camera will circle the given point in the X-Y plane at the given radius
dTheta      = pi / 90.0 # ------------------- Radians to advance per frame
totalFrames = 2 * int( ( 2 * pi ) / dTheta ) # ----- Number of frames that will bring the animation to its initial configuration ( GIF loop )

# ~ File Settings & Setup ~
prefix      = "frame_" # - Prefix for source frames
postfix     = ".png" # --- File extension for source frames ( pyglet can only save as PNG without PILLOW )
frmCount    = 0 # -------- Counting var to keep track of frames
subDirName  = "output" # - Subdir for all output files
ensure_dir( subDirName ) # Ensure that the output directory exists

# ~ Animation Settings ~
FPS         = 30 # -------------- Frame Per Second
outFileName = "billowFlaggins.gif" # Name of the output file

# ~ 002 Settings ~
theta  =  0 # --- Current theta for camera and flag edges
dt     =  0.005 # Length of timestep
t     =   0.00 #- time 
numPts = 40 # --- Number of points at the flag edges


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

    # 1. Create the flag
    topPts = linspace_endpoints( [ -0.5 ,  0.0 ,  0.5 ] ,  [ 0.5 ,  0.0 ,  0.5 ] , numPts )
    btmPts = linspace_endpoints( [ -0.5 ,  0.0 , -0.5 ] ,  [ 0.5 ,  0.0 , -0.5 ] , numPts )
    flag = WavyFlag( topPts , btmPts , sepDist = 0.025 )
    flag.set_colors( [ 255 , 255 , 255 ] , # Border
                     [ 249 ,  93 ,  84 ] , # Side 1 , Lt Red
                     [  89 , 152 , 255 ] ) # Side 2 , Lt Blu

    # 2. Create an OGL window
    window = OGL_App( [ flag ] , caption = "BILLOW FLAGGINS" , 
                      clearColor = [ 0 , 0 , 0 , 1 ] ) # BG color black

    # 3. Set the camera to look at the collection
    window.set_camera( [ 2 , 2 , 2 ] , [ 0 , 0 , 0 ] , [ 0 , 0 , 1 ] )

    

    # 4. Draw & Display
    while not window.has_exit:
        
        t += dTheta
        
        flag.calc_render_geo( wave_in_plane_cos( [ -0.5 ,  0.0 ,  0.5 ] ,  [ 0.5 ,  0.0 ,  0.5 ] , [ 0 , 0.125 , 0 ] , numPts , 2/3 , t ) , 
                              wave_in_plane_cos( [ -0.5 ,  0.0 , -0.5 ] ,  [ 0.5 ,  0.0 , -0.5 ] , [ 0 , 0.125 , 0 ] , numPts , 2/3 , t ) )
        
        theta += dTheta
        window.set_camera( camOrbit( theta ) , [ 0 , 0 , 0 ] , [ 0 , 0 , 1 ] )
        window.dispatch_events() # Handle window events
        window.on_draw() # Redraw the scene
        window.flip()

        # ___ END GRAPHICS _________________________________________________________________________________________________________________

        if _SAVEGRAPHICS:
            # Save one complete rotation
            if frmCount <= totalFrames:
                frmCount += 1
                if frmCount > 1: # For some reason the first saved frame is always empty ( 2018-03-22 , Windows 10 )
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

        imageio.mimsave( os.path.join( subDirName , outFileName ) , images , fps = FPS ) # This creates the GIF , Please wait on exit

# ___ End Main _____________________________________________________________________________________________________________________________
