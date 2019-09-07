# light_test.py
# James Watson , 2019 September
# Set up a light source in pyglet

# ~~~ Import Libs ~~~
# ~~ Standard Libs ~~
import os , sys
# ~~ Special Libs ~~
import numpy as np
import pyglet
from pyglet.window import key
from pyglet.gl import ( glColor3ub , GL_TRIANGLES , glEnable , glDisable ,
                        glLightfv , GL_LIGHT0 , GL_POSITION , GLfloat , GL_DIFFUSE , GL_QUADRATIC_ATTENUATION , GL_LIGHTING , )

# ~~ Path Additions ~~
SOURCEDIR = os.path.dirname( os.path.abspath( '__file__' ) ) # URL, dir containing source file: http://stackoverflow.com/a/7783326
PARENTDIR = os.path.dirname( SOURCEDIR )
sys.path.insert( 0 , PARENTDIR ) # Might need this to fetch a lib in a parent directory

# ~~ Local Libs ~~
from marchhare.MeshVFN import VF_to_N , sparse_VF_to_dense_VF , dense_flat_N_from_dense_VF
from marchhare.OGL_Shapes import OGL_App , Point_OGL , CartAxes , Vector_OGL , Trace_OGL , CameraOrbit , OGLDrawable

"""
~~~ DEV PLAN ~~~
[ ] Set up a custom draw function
[ ] Make the orbit camera part of the `OGL_Shapes` lib
[ ] Draw a GL cube primitive
[ ] Recreate the light source from HW5
~~~ CLEANUP ~~~
[ ] Streamline the template
"""

# == class Cuboid ==

class Cuboid( OGLDrawable ):
    """ Rectangular prism rendered in Pyglet """
    
    def resize( self , l , w , h ):
        """ Assign the extents of the Cuboid in 'l'ength , 'w'idth , 'h'eight """
        # NOTE: The origin is at the centroid of the cuboid
        self.l = l ; lHf = l/2
        self.w = w ; wHf = w/2
        self.h = h ; hHf = h/2
        self.corners = ( # Tuple of vertices that define the drawable geometry
            ( -lHf , -wHf , -hHf ) , # vertex 0    3-------2     # NOTE: Z+ is UP
            (  lHf , -wHf , -hHf ) , # vertex 1    !\      !\
            ( -lHf , -wHf ,  hHf ) , # vertex 2    ! \     Z \
            (  lHf , -wHf ,  hHf ) , # vertex 3    !  7=======6
            ( -lHf ,  wHf , -hHf ) , # vertex 4    1--|X---0  |
            (  lHf ,  wHf , -hHf ) , # vertex 5     \ |     \ |
            ( -lHf ,  wHf ,  hHf ) , # vertex 6      \|      Y|
            (  lHf ,  wHf ,  hHf ) , # vertex 7       5=======4
        )
        
        self.quads = ( # NOTE: Vertices must have CCW order to point the normals towards exterior , 
             ( 0 , 1 , 3 , 2 ) , # back face      3-----2    3-----2       right hand rule , otherwise dot products 
             ( 4 , 6 , 7 , 5 ) , # front face     !\  up \   !back !\      computed for backface-culling 
             ( 0 , 2 , 6 , 4 ) , # left face   right7=====6  !     ! 6     will have the wrong sign! faces vanish!
             ( 1 , 5 , 7 , 3 ) , # right face     1 |front|  1-----0l|eft 
             ( 0 , 4 , 5 , 1 ) , # down face       \|     |   \down \|
             ( 2 , 3 , 7 , 6 ) , # up face          5=====4    5=====4          
        )
        
        V_d , F_d      = sparse_VF_to_dense_VF( self.corners , self.quads , cadence = 4 )
        self.V_d       = np.array(  V_d  ).flatten()
        self.normals   = np.array(  dense_flat_N_from_dense_VF( V_d , F_d , cadence = 4 )  ).flatten()
        
        self.model = pyglet.graphics.vertex_list(
            6*4 ,
            ( 'v3f' , self.V_d ) , 
            ( 'n3f' , self.normals ) , 
        )
    
    def __init__( self , l = 1.0 , w = 1.0 , h = 1.0 ):
        """ Create a rectangular prism with 'l' (x) , 'w' (y) , 'h' (z) """
        OGLDrawable.__init__( self ) # -- Parent class init 
        self.resize( l , w , h ) # ------ Assign the extents of the cuboid
        
    def set_len( self , l ):
        """ Set the length of the Cuboid """
        self.resize( l , self.w , self.h )
        
    def draw( self ):
        """ Render the cuboid in OGL , This function assumes that a graphics context already exists """
        self.model.draw( GL_QUADS )

# __ End Cuboid __

if __name__ == "__main__":
    cube = Cuboid()
    # print( dir( __file__ ) )