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
[Y] Mobius Track , COMPLETE - 2018-04-16 , 1600 vertices
[Y] Query track for vertex positions , COMPLETE - 2018-04-16
[Y] Show opposite indices tracking a vertical position on the track , COMPLETE - 2018-04-16
[Y] Animate one flag on the track , COMPLETE - 2018-04-16 , There is a very pronounced stretching effect on the turn portion of the track
                                    This is due to the fact that the X step is unchanged with the addition of a circle orbit , Some
                                    trigonometry is required to fix
[ ] Calculate flag spacing along the entire track
    [ ] Remove track outline
    [ ] Fixed camera , Pick a good angle
[ ] Animate a track full of flags
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
from marchhare.marchhare import flatten_nested_sequence , ensure_dir , build_sublists_by_cadence , double_all_elem_except , indexw
from marchhare.Vector import vec_random_range , vec_unit , vec_mag , linspace_endpoints
from marchhare.VectorMath.SpatialVectorRobot import rot_matx_ang_axs , z_rot
from marchhare.VectorMath.Vector3D import vec_proj_to_plane
from marchhare.OGLshapes import Vector_OGL , OGL_App , Icosahedron_Reg , OGLDrawable , Point_OGL
from GIFtools import CircleOrbit , WavyFlag

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
        
        print "There are" , self.pntLen , "points"
        print "There are" , len( self.pntDices ) , "indices"
        print "There are" , len( self.allCoords ) , "coordinates"
        
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
        self.allPts.extend( linspace_endpoints( origin , backTopEnd , 3 * pointsPerUnit + 1 )[1:] )
        # ~ Section 4 ~ : Top-Right Turn
        center = np.add( self.allPts[-1] , [ 0.0 , -diameter / 2.0 , 0.0 ] )
        measVc = [ 0.0 , 1.0 , 0.0 ]
        self.allPts.extend( circle_arc_3D( [ 0.0 , 0.0 , 1.0 ] , center , diameter / 2.0 , measVc , -pi , pointsPerUnit ) )
        # ~ Section 5 ~ : Top-Right 
        frntLen = pi * diameter * 1.0 / 4.0
        frntDir = [ -1 , 0 , 0 ]
        frntTopEnd = np.add( self.allPts[-1] , np.multiply( frntDir , frntLen ) )
        self.allPts.extend( linspace_endpoints( self.allPts[-1] , frntTopEnd , pointsPerUnit + 1 )[1:] )
        # ~ Section 6 ~ : Twist from Top
        # A. Generate an arc that rotates about [ -1 , 0 , 0 ]
        circList = circle_arc_3D( [ -1 , 0 , 0 ] , 
                                  np.add( self.allPts[-1] , [ 0 , 0 , -diameter / 2.0 ] ) , 
                                  diameter / 2.0 , [ 0 , 0 , 1 ] , -pi , pointsPerUnit + 1 )
        # B. Generate offsets in the direction of [ -1 , 0 , 0 ] such that the travel in x is as expected
        # offsets = linspace_endpoints( self.allPts[-1] , [ -frntLen , 0 , 0 ] , pointsPerUnit + 1 ) 
        offsets = linspace_endpoints( [ 0 , 0 , 0 ] , [ -frntLen*4.0 , 0 , 0 ] , pointsPerUnit + 1 ) 
        circCoords = []
        for pDex , pnt in enumerate( circList ):
            circCoords.append( np.add( pnt , offsets[pDex] ) )
        # print "There are" , len( circList ) , "points in the circle"
        # print "There are" , len( circCoords ) , "offset circle points"
        self.allPts.extend( circCoords[1:] )
        # ~ Section 7 ~ : Bottom-Left
        frntLen = pi * diameter * 1.0 / 4.0
        frntTopEnd = np.add( self.allPts[-1] , np.multiply( frntDir , frntLen ) )
        self.allPts.extend( linspace_endpoints( self.allPts[-1] , frntTopEnd , pointsPerUnit + 1 )[1:] )        
        # ~ Section 8 ~ : Top-Right Turn
        center = np.add( self.allPts[-1] , [ 0.0 , diameter / 2.0 , 0.0 ] )
        measVc = [ 0.0 , -1.0 , 0.0 ]
        self.allPts.extend( circle_arc_3D( [ 0.0 , 0.0 , 1.0 ] , center , diameter / 2.0 , measVc , -pi , pointsPerUnit ) ) 
        # ~ Sections 9-11 ~ : Back Bottom Track
        backTopEnd = np.add( self.allPts[-1] , np.multiply( backDir , backLen ) )
        self.allPts.extend( linspace_endpoints( self.allPts[-1] , backTopEnd , 3 * pointsPerUnit + 1 )[1:] )   
        # ~ Section 12 ~ : Bottom-Right Turn
        center = np.add( self.allPts[-1] , [ 0.0 , -diameter / 2.0 , 0.0 ] )
        measVc = [ 0.0 , 1.0 , 0.0 ]
        self.allPts.extend( circle_arc_3D( [ 0.0 , 0.0 , 1.0 ] , center , diameter / 2.0 , measVc , -pi , pointsPerUnit ) )  
        # ~ Section 13 ~ : Bottom-Left
        frntTopEnd = np.add( self.allPts[-1] , np.multiply( frntDir , frntLen ) )
        self.allPts.extend( linspace_endpoints( self.allPts[-1] , frntTopEnd , pointsPerUnit + 1 )[1:] )   
        # ~ Section 14 ~ : Twist from Bottom
        # A. Generate an arc that rotates about [ -1 , 0 , 0 ]
        circList = circle_arc_3D( [ -1 , 0 , 0 ] , 
                                      np.add( self.allPts[-1] , [ 0 , 0 , diameter / 2.0 ] ) , 
                                      diameter / 2.0 , [ 0 , 0 , -1 ] , -pi , pointsPerUnit + 1 )
        # B. Generate offsets in the direction of [ -1 , 0 , 0 ] such that the travel in x is as expected
        # offsets = linspace_endpoints( self.allPts[-1] , [ -frntLen , 0 , 0 ] , pointsPerUnit + 1 ) 
        offsets = linspace_endpoints( [ 0 , 0 , 0 ] , [ -frntLen*4.0 , 0 , 0 ] , pointsPerUnit + 1 ) 
        circCoords = []
        for pDex , pnt in enumerate( circList ):
            circCoords.append( np.add( pnt , offsets[pDex] ) )
        # print "There are" , len( circList ) , "points in the circle"
        # print "There are" , len( circCoords ) , "offset circle points"
        self.allPts.extend( circCoords[1:] )       
        # ~ Section 15 ~ : Top-Right
        frntTopEnd = np.add( self.allPts[-1] , np.multiply( frntDir , frntLen ) )
        self.allPts.extend( linspace_endpoints( self.allPts[-1] , frntTopEnd , pointsPerUnit + 1 )[1:] )          
        # ~ Section 16 ~ : Top-Left Turn
        center = np.add( self.allPts[-1] , [ 0.0 , diameter / 2.0 , 0.0 ] )
        measVc = [ 0.0 , -1.0 , 0.0 ]
        self.allPts.extend( circle_arc_3D( [ 0.0 , 0.0 , 1.0 ] , center , diameter / 2.0 , measVc , -pi , pointsPerUnit )[1:] )         
        
    def get_points_list( self ):
        """ Get a consecutive list [ ... [ x_i , y_i , z_i ] ... ] of all of the points that comprise the edges of the strip / track """
        return self.allPts
    
    def get_point_series( self , bgnDex , endDex ):
        """ Return a list of points from 'bgnDex' to 'endDex' """
        if bgnDex < endDex:
            indices = [ indexw( self.allPts , i ) for i in range( bgnDex , endDex + 1 ) ]
        else:
            indices = [ indexw( self.allPts , i ) for i in range( bgnDex , endDex - 1 , 1 ) ]
        rtnPnts = []
        for index in indices:
            rtnPnts.append( self.allPts[ index ][:] )
        return rtnPnts
        
# __ End MobiusTrack __
        


# === Main =================================================================================================================================

# == Program Vars ==

# ~ FLAGS ~
_SAVEGRAPHICS = False # Set to True to create an animated GIF of the generated graphics
#                       Be patient for the save process to finish after graphics window exit 'X' is clicked

# ~ Generation Settings ~
scale       = 5
camOrbit    = CircleOrbit( [ 0 , 0 , 0 ] , 1.5 * scale , 1 * scale ) # Camera will circle the given point in the X-Y plane at the given radius
dTheta      = pi / 90.0 # ------------------- Radians to advance per frame
totalFrames = 2 * int( ( 2 * pi ) / dTheta ) # ----- Number of frames that will bring the animation to its initial configuration ( GIF loop )
counter     = 0

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
    print "MobiusTrack returned" , len( track.get_points_list() ) , "points"
    poly  = OGL_Polyline( track.get_points_list() , [ 255 , 255 , 255 ] , 3 )
    # Tracking Points
    trackPnt1 = Point_OGL( color = [ 255 , 0 , 0 ] )
    trackPnt2 = Point_OGL( color = [ 0 , 0 , 255 ] )
    trkPositions = track.get_points_list()
    flagWidth = 40
    # Create the flag
    topPts = track.get_point_series( counter , counter + flagWidth )
    btmPts = track.get_point_series( counter + 800  , counter + 800 + flagWidth )
    flag = WavyFlag( topPts , btmPts , sepDist = 0.025 )
    flag.set_colors( [ 255 , 255 , 255 ] , # Border
                     [ 249 ,  93 ,  84 ] , # Side 1 , Lt Red
                     [  89 , 152 , 255 ] ) # Side 2 , Lt Blu    
    
    # 2. Create an OGL window
    window = OGL_App( [ poly , trackPnt1 , trackPnt2 , flag ] , # List of objects to render
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
        counter += 1
        print trkPositions[ indexw( trkPositions , counter       ) ] , trkPositions[ indexw( trkPositions , counter + 800 ) ]
        trackPnt1.set_pos( trkPositions[ indexw( trkPositions , counter       ) ] )
        trackPnt2.set_pos( trkPositions[ indexw( trkPositions , counter + 800 ) ] )
        flag.calc_render_geo( track.get_point_series( counter , counter + flagWidth ) , 
                              track.get_point_series( counter + 800 , counter + 800 + flagWidth ) )        
        
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
