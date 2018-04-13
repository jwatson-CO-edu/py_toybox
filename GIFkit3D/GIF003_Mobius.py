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
from marchhare.marchhare import flatten_nested_sequence , ensure_dir , build_sublists_by_cadence , double_all_elem_except
from marchhare.Vector import vec_random_range , vec_unit , vec_mag , linspace_endpoints
from marchhare.VectorMath.SpatialVectorRobot import rot_matx_ang_axs , z_rot
from marchhare.VectorMath.Vector3D import vec_proj_to_plane
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
    k         = vec_unit( axis )
    rtnList   = []
    # 1. Project the theta = 0 vector onto the circle plane
    measrVec = vec_unit( vec_proj_to_plane( beginMeasureVec , axis ) )
    # 2. For each theta
    for theta_i in thetaList:
        # 3. Create a rotation matrix for the rotation
        R = rot_matx_ang_axs( theta_i , k  )
        # 4. Apply rotation to the measure vector && 5. Scale the vector to the radius && 6. Add to the center && 7. Append to the list
        rtnList.append( np.add( center , np.multiply( np.dot( R , measrVec ) , radius ) ) )
    # 8. Return
    return rtnList

def paint_polyline( consecutivePoints , color , thickness ):
    """ Paint a list of points [ ... [ x_i , y_i , z_i ] ... ] to the graphics context , with a segment between each consecutive pair """
    
    
      
    
# __ End Helper __

class OGL_Polyline( object ):
    """ Static polyline in 3D space """
    # NOTE: This object does not support rotations or translations
    
    def __init__( self , consecutivePoints , color , thickness ):
        """ Populate segments to render """
        self.color  = color
        self.thic   = thickness
        self.pntLen = len( consecutivePoints )
        # 1. Repeat middle indiced
        self.pntDices = double_all_elem_except( range( self.pntLen ) , [ 0 , self.pntLen - 1 ] )
        # 2. Flatten into vertices list
        self.allCoords = flatten_nested_sequence( consecutivePoints )     
        
    def draw( self ):
        """ Render the polyline to the graphics context """
        # 3. Paint
        # A. Set color
        glColor3ub( *self.color )
        # B. Set line width
        pyglet.gl.glLineWidth( self.thic )
        # C. Render segments
        pyglet.graphics.draw_indexed( 
            self.pntLen , # ------------ Number of seqential triplet in vertex list
            GL_LINES , # ---------- Draw lines
            self.pntDices , # ---------- Indices where the coordinates are stored
            ( 'v3f' , self.allCoords ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
        )           
        


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
        # ~ Section 4 ~ : Top-Right Turn
        center = np.add( self.allPts[-1] , [ 0.0 , -diameter / 2.0 , 0.0 ] )
        measVc = [ 0.0 , 1.0 , 0.0 ]
        self.allPts.extend( circle_arc_3D( [ 0.0 , 0.0 , 1.0 ] , center , diameter / 2.0 , measVc , -pi , pointsPerUnit ) )
        # ~ Section 5 ~ : Top-Right 
        # FIXME : START HERE
        
    def get_points_list( self ):
        """ Get a consecutive list [ ... [ x_i , y_i , z_i ] ... ] of all of the points that comprise the edges of the strip / track """
        return self.allPts
        
# __ End MobiusTrack __
        


# === Main =================================================================================================================================

# == Program Vars ==

# ~ FLAGS ~
_SAVEGRAPHICS = False # Set to True to create an animated GIF of the generated graphics
#                       Be patient for the save process to finish after graphics window exit 'X' is clicked

# ~ Generation Settings ~
scale       = 4
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
outFileName = "mobius.gif" # Name of the output file

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

    # 1. Instantiate geometry
    track = MobiusTrack( [ 0.0 , 0.0 , 0.0 ] , 1.0 )
    poly  = OGL_Polyline( track.get_points_list() , [ 255 , 255 , 255 ] , 3 )
    
    # 2. Create an OGL window
    window = OGL_App( [ poly ] , # List of objects to render
                      caption = "MOBIUS"  , # ---------- Window caption
                      clearColor = [ 0 , 0 , 0 , 1 ] ) # BG color black

    # 3. Set the camera to look at the center of the action
    window.set_camera( [ 2 , 2 , 2 ] , # Camera position
                       [ 0 , 0 , 0 ] , # Focal point of camera
                       [ 0 , 0 , 1 ] ) # Direction of up

    

    # 4. Draw & Display
    while not window.has_exit:
        # A. Update the timestep
        theta += dt
        
        # B. Update animation
        
        # C. Move camera
        
        window.set_camera( camOrbit( theta ) , [ 0 , 0 , 0 ] , [ 0 , 0 , 1 ] )
        
        # D. Redraw
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
