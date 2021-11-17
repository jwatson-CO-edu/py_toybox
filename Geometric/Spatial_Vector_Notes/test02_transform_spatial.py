#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2017-05-30

from __future__ import division # MUST be run before all other expressions , including docstrings!

"""
render_cuboid.py
James Watson , 2017 July , Written on Spyder 3 / Python 2.7
Render a cuboid of a type to be used for Spatial Vector investigations

Dependencies: Pyglet
"""

"""
%% Test Sequence %%
<clip>
[Y] 1. Transform a body using the joint transform(s) from the tutorial
    |Y| 1.a. Animate a single primitive that spins using already-implemented transforms - SUCCESS , Although setting the period results in a higher
             than expected framerate , framerate crashes when the window is moved
        {Y} 1.a.1. Fix the helical joint calculation - COMPLETE , Although , in the formulation presented in [2] , the transform matrix differed
                   in size depending on the type of joint implemented. It is not known at this time if this seeming inconsistency is intentional
    |Y| 1.b. Rotate    , 0 pitch
    |Y| 1.c. Translate , infty pitch
    |Y| 1.d. Screw     , finite pitch
<\clip>

~~~ TODO ~~~
* Consider a Spatial Geo Primitive that contains transform operations common to all spatial geometry ( WAIT until operations successfully
  implemented in a presently-useful class )

"""

# == Init ==================================================================================================================================

# ~~ Helpers ~~
def add_valid_to_path( pathList ):
    """ Add all the valid paths in 'pathList' to the Python path """
    import sys , os
    for path in pathList:
        if os.path.isdir( path ):
            sys.path.append( path )
            print "Loaded" , path

# ~~ Imports ~~
# ~ Standard ~
import os , random
from math import pi , cos , sin , degrees , radians
# ~ Special ~
import numpy as np
import pyglet # --------- Package for OpenGL
from pyglet.gl import * #- OpenGL flags and state machine
from pyglet import clock # Animation timing
# ~ Local ~
localPaths = [ os.path.join( "C:" , os.sep , "Users" , "jwatson" , "Documents" , "Python Scripts" ) ] # List of paths to your custom modules
add_valid_to_path( localPaths )
from SpatialVectorRobot import *

# ~~ Aliases & Shortcuts ~~
infty = float('inf') # infinity

# ~~ Setup ~~

# == End Init ==============================================================================================================================


# === OpenGL Classes ===

# == class CartAxes ==

class CartAxes(object):
    """ Standard set of Cartesian coordinate axes """
    # NOTE: At this time , will only draw the axes at the lab frame
    
    def __init__( self , unitLen ):
        """ Set up the vertices for a coordinate axes """
        
        subLen = unitLen / 8.0
        
        self.vertices = (
                  0 ,       0 ,       0 ,     # 0 , Orgn
            unitLen ,       0 ,       0 ,     # 1 , X vec / arw
                  0 , unitLen ,       0 ,     # 2 , Y vec / arw
                  0 ,       0 , unitLen ,     # 3 , Z vec / arw
            unitLen - subLen ,  subLen , 0 ,  # 4 , X arw
            unitLen - subLen , -subLen , 0 ,  # 5 , X arw 
            0 , unitLen - subLen ,  subLen ,  # 6 , Y arw                   
            0 , unitLen - subLen , -subLen ,  # 7 , Y arw
             subLen , 0 , unitLen - subLen ,  # 8 , Z arw
            -subLen  , 0 , unitLen - subLen   # 9 , Z arw
              
        )
        
        self.ndx_Xvec = ( 0 , 1 ) ; self.ndx_Xarw = ( 1 , 4 , 5 )
        self.ndx_Yvec = ( 0 , 2 ) ; self.ndx_Yarw = ( 2 , 6 , 7 )
        self.ndx_Zvec = ( 0 , 3 ) ; self.ndx_Zarw = ( 3 , 8 , 9 )
        
        self.colors  = ( ( 255 ,   0 ,   0 ) , 
                         (   0 , 255 ,   0 ) , 
                         (   0 ,   0 , 255 )  )
        self.vectors = ( self.ndx_Xvec , self.ndx_Yvec , self.ndx_Zvec )
        self.arrows  = ( self.ndx_Xarw , self.ndx_Yarw , self.ndx_Zarw )
        
    def draw( self ):
        """ Draw the axes """
        
        pyglet.gl.glLineWidth( 3 )
        
        for i in xrange(3): # 
            
            glColor3ub( *self.colors[i] )
            
            pyglet.graphics.draw_indexed( 
                10 , # --------------------- Number of seqential triplet in vertex list
                GL_LINES , # -------------- Draw quadrilaterals
                self.vectors[i] , # ---------- Indices where the coordinates are stored
                ( 'v3f' , self.vertices ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
            ) 
            
            pyglet.graphics.draw_indexed( 
                10 , # --------------------- Number of seqential triplet in vertex list
                GL_TRIANGLES , # -------------- Draw quadrilaterals
                self.arrows[i] , # ---------- Indices where the coordinates are stored
                ( 'v3f' , self.vertices ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
            ) 
            
# == End CartAxes ==

# URL , Spatial Transforms: http://drake.mit.edu/doxygen_cxx/group__multibody__spatial__pose.html

# == class Cuboid ==

class Cuboid(object):
    """ Rectnagular prism rendered in Pyglet """
    
    def __init__( self , l , w , h , pos = [ 0 , 0 , 0 ] ):
        """ Create a rectangular prism with 'l' (x) , 'w' (y) , 'h' (z) """
        # NOTE: Poses are stored as transforms , since that is what you need poses for anyway
        
        # FIXME : This object needs a transform to the parent frame
        
        self.vertices = ( # List of untransformed vertices
            0 , 0 , 0 ,	# vertex 0    3-------2     # NOTE: Z+ is UP
            l , 0 , 0 ,	# vertex 1    !\      !\
            0 , 0 , h ,	# vertex 2    ! \     Z \
            l , 0 , h ,	# vertex 3    !  7=======6
            0 , w , 0 ,	# vertex 4    1--|X---0  |
            l , w , 0 ,	# vertex 5     \ |     \ |
            0 , w , h ,	# vertex 6      \|      Y|
            l , w , h ,	# vertex 7       5=======4
        )
        
        self.vertX = list( self.vertices ) # List of transformed vertices
        
        self.indices = ( #                                       NOTE: Vertices must have CCW order to point the normals towards exterior , 
             0 , 1 , 3 , 2 , # back face      3-----2    3-----2       right hand rule , otherwise dot products computed for backface-culling 
             4 , 6 , 7 , 5 , # front face     !\  up \   !back !\      will have the wrong sign! faces vanish!
             0 , 2 , 6 , 4 , # left face   right7=====6  !     ! 6
             1 , 5 , 7 , 3 , # right face     1 |front|  1-----0l|eft 
             0 , 4 , 5 , 1 , # down face       \|     |   \down \|
             2 , 3 , 7 , 6 , # up face          5=====4    5=====4          
        )
        
        self.linDices = (
            3 , 2 ,
            2 , 6 ,
            6 , 7 ,
            7 , 3 ,
            3 , 1 ,
            2 , 0 ,
            6 , 4 ,
            7 , 5 ,
            0 , 4 ,
            4 , 5 ,
            5 , 1 ,
            1 , 0
        )
        
        self.color     = (  88 , 181 ,  74 ) # Body color
        self.colorLine = (   0 ,   0 , 255 ) # Line color
        
        self.pos3D = pos # 3D position in the parent frame
        
        self.thetaDeg = 0.0
        self.thetaRad = 0.0
        self.rotAxis = [ 0.0 , 0.0 , 1.0 ]
        
        self.rotnByOGL = False # Flag for whether to apply rotation by OpenGL: True - OpenGL , False - Matrix Algebra
        
        
    def xform_homog( self , homogXform ):
        """ Transform all of the vertices and store the result for rendering """
        for i in xrange( 0 , len( self.vertices ) , 3 ):
            self.vertX[ i : i+4 ] = apply_homog( homogXform , self.vertices[ i : i+4 ] )
        
    def xform_Z_rot( self , thetaZrad ):
        """ Rotate all of the vertices in the list about the local Z axis """
        self.xform_homog( homogeneous_Z( thetaZrad , [ 0 , 0 , 0 ] ) )
        
    def xform_ang_axs( self , thetaRad , k ):
        """ Rotate all of the vertices in the list about the local Z axis """
        self.xform_homog( homog_ang_axs( thetaRad , k , [ 0 , 0 , 0 ] ) )
        
    def draw( self ):
        """ Render the cuboid in OGL , This function assumes that a graphics context already exists """
        # print "DEBUG:" , "Drawing cuboid!"
        glTranslated( *self.pos3D ) # This moves the origin of drawing , so that we can use the above coordinates at each draw location
        if self.rotnByOGL:
            glRotated( self.thetaDeg , *self.rotAxis )
        # glTranslated( 0 , 0 , 0  ) # This moves the origin of drawing , so that we can use the above coordinates at each draw location
        # print "DEBUG:" , "Translated to" , 0 , 0 , 0
        glColor3ub( *self.color ) # Get the color according to the voxel type
        # print "DEBUG:" , "Set color to" , self.color
        pyglet.graphics.draw_indexed( 
            8 , # --------------------- Number of seqential triplet in vertex list
            GL_QUADS , # -------------- Draw quadrilaterals
            self.indices , # ---------- Indices where the coordinates are stored
            ( 'v3f' , self.vertX ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
        ) #   'v3i' # This is for integers I suppose!
                
        glColor3ub( *self.colorLine )
        pyglet.gl.glLineWidth( 3 )
        pyglet.graphics.draw_indexed( 
            8 , # --------------------- Number of seqential triplet in vertex list
            GL_LINES , # -------------- Draw quadrilaterals
            self.linDices , # ---------- Indices where the coordinates are stored
            ( 'v3f' , self.vertX ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
        ) #   'v3i' # This is for integers I suppose!
                
        # print "DEBUG:" , "Indices"
        # print self.indices      
        # print "DEBUG:" , "Vertices"
        # print self.vertices      
        """ URL: http://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/programming_guide/graphics.html#vertex-lists
        
        There is a significant overhead in using pyglet.graphics.draw and pyglet.graphics.draw_indexed due to pyglet 
        interpreting and formatting the vertex data for the video device. Usually the data drawn in each frame (of an animation) 
        is identical or very similar to the previous frame, so this overhead is unnecessarily repeated.
        
        A VertexList is a list of vertices and their attributes, stored in an efficient manner that’s suitable for direct 
        upload to the video card. On newer video cards (supporting OpenGL 1.5 or later) the data is actually stored in video memory.
        """
        if self.rotnByOGL:
            glRotated( -self.thetaDeg , *self.rotAxis )
        glTranslated( *np.multiply( self.pos3D , -1 ) ) # Reset the transform coordinates
        # print "DEBUG:" , "Translated to" , 0 , 0 , 0
        # print "DEBUG:" , "Done drawing!"

# == End Cuboid ==

# == class OGL_App ==
        
class OGL_App( pyglet.window.Window ):
    """ Bookkeepping for Pyglet rendering """
    
    def __init__( self , objList = [] ):
        """ Instantiate the environment with a list of objhects to render """
        super( OGL_App , self ).__init__( resizable = True, caption = 'Transform a Cuboid' )
        glClearColor( 0.7 , 0.7 , 0.8 , 1 ) # Set the BG color for the OGL window
        
        # URL: https://www.opengl.org/discussion_boards/showthread.php/165839-Use-gluLookAt-to-navigate-around-the-world
        self.camera = [  3 ,  8 ,  4 , # eyex    , eyey    , eyez    : Camera location , point (world) , XYZ
                         3 ,  0 ,  0 , # centerx , centery , centerz : Center of the camera focus , point (world) , XYZ
                         0 ,  0 ,  1 ] # upx     , upy     , upz     : Direction of "up" in the world frame , vector , XYZ
        
        self.renderlist = objList
        self.showFPS = False
        
    def setup_3D( self ):
        """ Setup the 3D matrix """
        # ~ Modes and Flags ~
        # Use 'GL_DEPTH_TEST' to ensure that OpenGL maintains a sensible drawing order for polygons no matter the viewing angle
        glEnable( GL_DEPTH_TEST ) # Do these setup functions really have to be run every single frame? # TODO: Try moving these to the '__init__' , see what happens
        # glEnable( GL_CULL_FACE ) # Uncomment to preform backface culling # This might erase arrowheads if they are away-facing!
        # ~ View Frustum Setup ~
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        gluPerspective( 70 , self.width / float( self.height ) , 0.1 , 200 )
        # ~ View Direction Setup ~
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        gluLookAt( *self.camera )
            
    def on_draw( self ):
        """ Repaint the window , per-frame activity """
        self.clear()
        self.setup_3D()
        # print "DEBUG:" , "There are" , len( self.renderlist ) , "items in 'self.renderlist'"
        for obj in self.renderlist:
            obj.draw()
        if self.showFPS:
            print "FPS:" , pyglet.clock.get_fps() # Print the framerate

# == End OGL_App ==
            
# === End OpenGL ===


# == Main ==================================================================================================================================


if __name__ == "__main__":
    # Create display window , set up camera , begin main event loop
    
    updateHz = 30.0 # Target frame rate
    updatePeriodSec = 1.0 / updateHz 

    # ~ Review XForm Output ~

    print "Z Rotation , Homogeneous Coordinates"
    print homogeneous_Z( pi / 2 , [ 1 , 2 , 3 ] )
    print "Angle-Axis Rotation , Homogeneous Coordinates"
    print homog_ang_axs( pi / 2 , [ 0 , 0 , 1 ] , [ 1 , 2 , 3 ] ) # Yup , they look the same!
    print "Joint XForm , Rotational"
    [ XJ_s , s_i , XJ_h ] = joint_xform( 0.0 , pi / 2 )
    print XJ_h
    print "Joint XForm , Prismatic"
    [ XJ_s , s_i , XJ_h ] = joint_xform( infty , 2 )
    print XJ_h
    print "Joint XForm , Helical"
    [ XJ_s , s_i , XJ_h ] = joint_xform( 4 , pi / 2 )
    print XJ_h


    # Rotation to perform
    turnDeg = 45
    turnAxs = [ 1 , 1 , 1 ]
    q = 0
    pitch = [ 0 , 0.40 , infty ]
    
    # ~ Set up 1st cuboid to turn using matrix algebra ~
    prism1 = Cuboid( 0.5 , 1 , 3 , [ 6 ,  0 ,  0 ] )
    prism1.rotnByOGL = False
    
    # ~ Set up 1st cuboid to turn using matrix algebra ~
    prism2 = Cuboid( 0.5 , 1 , 3 , [ 4 ,  0 ,  0 ] )
    prism2.rotnByOGL = False
    
    # ~ Set up 1st cuboid to turn using matrix algebra ~
    prism3 = Cuboid( 0.5 , 1 , 3 , [ 2 ,  0 ,  0 ] )
    prism3.rotnByOGL = False
    
    window = OGL_App( [ CartAxes( 1 ) , prism1 , prism2 , prism3 ] ) 
    
    # ~ Set up animation ~
    def update( updatePeriodSec ):
        """ Per-frame changes to make prior to redraw """
        global q
        # 1. Update q
        q += pi / 60.0
        # print "DEBUG , q:" , q
        # 2. Apply transform for each of the cuboids
        for cubDex , cuboid in enumerate( [ prism1 , prism2 , prism3 ] ):
            cuboid.xform_homog( joint_xform( pitch[ cubDex ] , q )[2] )
    
    # ~ Begin animation ~
    
    # Create a loop with 'schedule_interval'
    # http://nullege.com/codes/show/src%40c%40h%40chemshapes-HEAD%40host%40pygletHG%40contrib%40layout%40examples%40interpreter.py/116/pyglet.clock.schedule_interval/python
    
    clock.schedule_interval( update , updatePeriodSec ) # update at target frame rate
    window.set_visible()
    
    while not window.has_exit:
        window.dispatch_events() # Handle window events
        clock.tick() # Call the update function
        # glClear( GL_COLOR_BUFFER_BIT )
        window.on_draw() # Redraw the scene
        window.flip()

# == End Main ==============================================================================================================================

        
# == Spare Parts ===========================================================================================================================
        
## ~ Set up 1st cuboid to turn using matrix algebra ~
#prism1 = Cuboid( 0.5 , 1 , 3 , [ 6 ,  0 ,  0 ] )
#prism1.rotnByOGL = False
#
## ~ Set up 2nd cuboid to turn using OGL ~
#prism2 = Cuboid( 1 , 2 , 3 , [  2 ,  0 ,  0 ] )
#prism2.rotnByOGL = True
#prism2.thetaDeg = turnDeg
#prism2.rotAxis = turnAxs
#window = OGL_App( [ CartAxes( 1 ) , prism1 , prism2 ] ) 

# == End Parts =============================================================================================================================