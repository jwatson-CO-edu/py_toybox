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
[ ] 0. Render cuboid, using the primitive voxel engine as an example. Will use cuboids to construct robots
    |Y| 0.a. Render multiple translated - SUCCESS
    |Y| 0.b. Render multiple rotated , OGL - SUCCESS
    | | 0.c. Render multiple rotated , Coord Transformation
    | | 0.d. Compare rotations in Spatial Coordinates to rotations in OGL in order to compare correctness
    |Y| 0.e. Render axes , will need these to get an idea of the relative positions and orientations of things - SUCCESS
    
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
from math import pi , cos , sin , degrees
# ~ Special ~
import numpy as np
import pyglet
from pyglet.gl import *
# ~ Local ~
localPaths = [ os.path.join( "C:" , os.sep , "Users" , "jwatson" , "Documents" , "Python Scripts" ) ] # List of paths to your custom modules
add_valid_to_path( localPaths )
from SpatialVectorRobot import *

# ~~ Setup ~~

# == End Init ==============================================================================================================================

# === Geometry ===

# == Trigonometry ==

def ver( theta ):
    """ Versine , radians """
    return 1 - cos( theta )

def verd( theta ):
    """ Versine , degrees """
    return degrees( 1 - cos( theta ) )

# == End Trig ==

# == Geo 3D ==

def homogeneous_Z( x , y , z , zTheta ):
    """ Return the Homogeneous Transformation for the given parameters """
    return np.vstack( ( np.hstack( (  z_rot( zTheta ) , [ [x] , [y] , [z] ]  ) ) ,
                        np.hstack( ( [ 0 , 0 , 0 ]   , [1]  ) ) ) )
    
def homog_ang_axs( theta , r , pos ):
    """ Return the Homogeneous Transformation for the given angle , axis , and position """
    # FIXME : START HERE , INTRO ROBOTICS PG 28 [26]
    
    
def apply_homog( homogMat , vec3 ):
    """ Apply a homogeneous transformation to a 3D vector """
    return ( np.dot( homogMat , [ vec3[0] , vec3[1] , vec3[2] , 0 ] ) )[:3]
    
# == End 3D ==

# === End Geometry ===

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

# URL , Spatial Transforms: http://drake.mit.edu/doxygen_cxx/group__multibody__spatial__pose.html

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
        
        self.vertX = self.vertices[:] # List of transformed vertices
        
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
        
        self.color     = (  88 , 181 ,  74 )
        self.colorLine = (   0 ,   0 , 255 )
        
        self.pos3D = pos
        
        self.thetaDeg = 0;
        self.rotAxis = [ 0 , 0 , 1 ];
        
    def draw( self ):
        """ Render the cuboid in OGL , This function assumes that a graphics context already exists """
        print "Drawing cuboid!"
        glTranslated( *self.pos3D ) # This moves the origin of drawing , so that we can use the above coordinates at each draw location
        glRotated( self.thetaDeg , *self.rotAxis )
        # glTranslated( 0 , 0 , 0  ) # This moves the origin of drawing , so that we can use the above coordinates at each draw location
        print "DEBUG:" , "Translated to" , 0 , 0 , 0
        glColor3ub( *self.color ) # Get the color according to the voxel type
        print "DEBUG:" , "Set color to" , self.color
        pyglet.graphics.draw_indexed( 
            8 , # --------------------- Number of seqential triplet in vertex list
            GL_QUADS , # -------------- Draw quadrilaterals
            self.indices , # ---------- Indices where the coordinates are stored
            ( 'v3f' , self.vertices ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
        ) #   'v3i' # This is for integers I suppose!
                
        glColor3ub( *self.colorLine )
        pyglet.gl.glLineWidth( 3 )
        pyglet.graphics.draw_indexed( 
            8 , # --------------------- Number of seqential triplet in vertex list
            GL_LINES , # -------------- Draw quadrilaterals
            self.linDices , # ---------- Indices where the coordinates are stored
            ( 'v3f' , self.vertices ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
        ) #   'v3i' # This is for integers I suppose!
                
        print "DEBUG:" , "Indices"
        print self.indices      
        print "DEBUG:" , "Vertices"
        print self.vertices      
        """ URL: http://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/programming_guide/graphics.html#vertex-lists
        
        There is a significant overhead in using pyglet.graphics.draw and pyglet.graphics.draw_indexed due to pyglet 
        interpreting and formatting the vertex data for the video device. Usually the data drawn in each frame (of an animation) 
        is identical or very similar to the previous frame, so this overhead is unnecessarily repeated.
        
        A VertexList is a list of vertices and their attributes, stored in an efficient manner that’s suitable for direct 
        upload to the video card. On newer video cards (supporting OpenGL 1.5 or later) the data is actually stored in video memory.
        """
        # glTranslated( 0 , 0 , 0 ) # Reset the transform coordinates
        glRotated( -self.thetaDeg , *self.rotAxis )
        glTranslated( *np.multiply( self.pos3D , -1 ) ) # Reset the transform coordinates
        print "DEBUG:" , "Translated to" , 0 , 0 , 0
        print "Done drawing!"

        
class OGL_App( pyglet.window.Window ):
    """ Bookkeepping for Pyglet rendering """
    
    def __init__( self , objList = [] ):
        """ Instantiate the environment with a list of objhects to render """
        super( OGL_App , self ).__init__( resizable = True, caption = 'Render a Cuboid' )
        glClearColor( 0.7 , 0.7 , 0.8 , 1 ) # Set the BG color for the OGL window
        
        # URL: https://www.opengl.org/discussion_boards/showthread.php/165839-Use-gluLookAt-to-navigate-around-the-world
        self.camera = [  4 ,  4 ,  4 , # eyex    , eyey    , eyez    : Camera location , point (world) , XYZ
                         0 ,  0 ,  0 , # centerx , centery , centerz : Center of the camera focus , point (world) , XYZ
                         0 ,  0 ,  1 ] # upx     , upy     , upz     : Direction of "up" in the world frame , vector , XYZ
        
        self.renderlist = objList
        
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
        print "DEBUG:" , "There are" , len( self.renderlist ) , "items in 'self.renderlist'"
        for obj in self.renderlist:
            obj.draw()

# == Main ==================================================================================================================================

if __name__ == "__main__":
    # Create display window , set up camera , begin main event loop

    print homogeneous_Z( 1 , 2 , 3 , pi / 2 )
#    print apply_homog( homogeneous_Z( 1 , 2 , 3 , pi / 2 ) , 
#                       [ 3 , 3 , 3 ] )

    # window = OGL_App( [ Cuboid( 1 , 2 , 3 ) , Cuboid( 1 , 2 , 3 , [ 2 , 0 , 0 ] ) ] ) 
    # window = OGL_App( [ CartAxes( 1 ) ] ) 
    prism1 = Cuboid( 1 , 2 , 3 , [ -2 , 0 , 0 ] )
    prism2 = Cuboid( 1 , 2 , 3 , [ 2 , 0 , 0 ] )
    prism2.thetaDeg = 122.5
    prism2.rotAxis = [ 0 , 0 , 1 ]
    window = OGL_App( [ CartAxes( 1 ) , prism1 , prism2 ] ) 
    pyglet.app.run()
    

# == End Main ==============================================================================================================================
