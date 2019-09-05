#!/usr/bin/env python3

# plane_test.py
# James Watson , 2019 August
# Little plane

"""
~~~ DEV PLAN ~~~
1. SF Rail Environment
    [ ] Light source
    [ ] Scrolling grid ground
    [ ] kb ctrl
    [ ] js ctrl
    [ ] Exhaust trail
2. VFN Expansion <-from-- Regrasp Planning (Only if multiple models are being made)
"""

import os , sys , time
SOURCEDIR = os.path.dirname( os.path.abspath( '__file__' ) ) # URL, dir containing source file: http://stackoverflow.com/a/7783326
PARENTDIR = os.path.dirname( SOURCEDIR )
# ~~ Path Utilities ~~
def prepend_dir_to_path( pathName ): sys.path.insert( 0 , pathName ) # Might need this to fetch a lib in a parent directory
prepend_dir_to_path( PARENTDIR )

from random import randrange
from math import pi
import numpy as np
from marchhare.OGL_Shapes import OGL_App , Point_OGL , CartAxes , Vector_OGL , Trace_OGL , CameraOrbit , OGLDrawable
from marchhare.Utils3 import build_sublists_by_cadence
from marchhare.MeshVFN import VF_to_N , sparse_VF_to_dense_VF , dense_flat_N_from_dense_VF
import pyglet
from pyglet.window import key
from pyglet.gl import ( glColor3ub , GL_TRIANGLES , glEnable , glDisable ,
                        glLightfv , GL_LIGHT0 , GL_POSITION , GLfloat , GL_DIFFUSE , GL_QUADRATIC_ATTENUATION , GL_LIGHTING , )

def walk_triangles():
    pass

class StarGlider( OGLDrawable ):
    """ Little Wing """
    
    def __init__( self , wingspan = 1.0 ):
        """ Set up as drawable """
        OGLDrawable.__init__( self ) # ------------------------- Parent class init
        
        # 1. Calc and set geo
        length   = wingspan / 2.0
        fuseLen  = length   / 2.0
        depth    = fuseLen  / 2.0
        
        fuseHalf = fuseLen / 2.0
        dpthHalf = depth / 2.0
        wingHalf = wingspan / 2.0
        
        front    = [  fuseHalf        ,  0.0      , 0.0       ]
        bottom   = [  0.0             ,  0.0      , -dpthHalf ]
        back     = [ -fuseHalf        ,  0.0      , 0.0       ]
        top      = [  0.0             ,  0.0      ,  dpthHalf ]
        rghtWTip = [ -length+fuseHalf , -wingHalf , 0.0       ]
        leftWTip = [ -length+fuseHalf ,  wingHalf , 0.0       ]
        
        vertSet = [ front , bottom , back , top , rghtWTip , leftWTip ]
        #           0     , 1      , 2    , 3   , 4        , 5
        
        self.set_verts( vertSet )
        
        self.triangles = (
            3 , 0 , 5 , # Top    Front Left
            2 , 3 , 5 , # Top    Back  Left
            0 , 1 , 5 , # Bottom Front Left
            1 , 2 , 5 , # Bottom Back  Left
            0 , 3 , 4 , # Top    Front Right
            3 , 2 , 4 , # Top    Back  Right
            1 , 0 , 4 , # Bottom Front Right
            2 , 1 , 4 , # Bottom Back  Right
        )
        
        F = build_sublists_by_cadence( self.triangles , 3 )
        
        
        
        V_d , F_d = sparse_VF_to_dense_VF( vertSet , F )
        N_d = dense_flat_N_from_dense_VF( V_d , F_d )
        self.normals = np.array( N_d ).flatten()
        
        self.Vd = np.array( V_d ).flatten()
        
        # FIXME , START HERE: Vertices and normals are different lenghts! Each vertex needs a normal!
        # WONDER: Does `pyglet.graphics.vertex_list` implement a vertex buffer?
        
        print( self.Vd.shape )
        print( len( F_d ) )
        # print( F_d )
        print( self.normals.shape )
        print( len( tuple( list( range( int( len( self.normals )/3 ) ) ) ) ) )
        
        self.model = pyglet.graphics.vertex_list(
            24 ,
            ( 'v3f' , self.Vd ) , 
            # ( 'v3i' , F_d ) ,
            ( 'n3f' , self.normals ) , 
            #( 'n3i' , tuple( list( range( int( len( self.normals )/3 ) ) ) ) )
        )
        
        # 2. Set color
        # FIXME
        
    def draw( self ):  
        """ Render the StarGlider """
        # 1. Transform points
        self.xform_lab()
        # 2. Render!
        # 2. Set color
        glColor3ub( *self.color )
        
        _LIGHT = 0
        
        if _LIGHT: glEnable(GL_LIGHTING)
        
        # FIXME , START HERE :
        # * Add normals to the draw function
        # * Remove invocations of the transform function
        
        
        if 0:
            pyglet.graphics.draw_indexed( 
                6 , # ------------------ Number of seqential triplet in vertex list
                GL_TRIANGLES , # ------- Draw quadrilaterals
                self.triangles , # ----- Indices where the coordinates are stored
                ( 'v3f' , self.labVerts ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
            )
        else:
            if _LIGHT: 
                glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat * 4)(0.75, 0.0, 0.75, 1))
                glLightfv(GL_LIGHT0, GL_DIFFUSE, (GLfloat * 3)(255.0, 255.0, 255.0))
                glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, (GLfloat * 1) (.35))
                glEnable(GL_LIGHT0)
            self.model.draw( GL_TRIANGLES )
        if _LIGHT: glDisable(GL_LIGHTING)

_DEBUG = False

if __name__ == "__main__":
    
    
    

    objs = []

    cam = CameraOrbit()

    if 1:
        plane = StarGlider( 1.0 )
        objs.append( plane )
        objs.append( CartAxes() )

    else:
        crtAxes = CartAxes( unitLen = 1.0 )

        for x in [0,1]:
            for y in [0,1]:
                for z in [0,1]:
                    objs.append(
                        Point_OGL( pnt = [ x , y , z ] )
                    )

        objs.append( CartAxes() )

        vec = Vector_OGL()
        vec.set_origin_displace( [0,1,0] , [0,0,1] )
        vec.set_color( (randrange(0,256),randrange(0,256),randrange(0,256),) )
        objs.append( vec )

        trace = Trace_OGL()
        trace.set_color( (255,255,255,) )
        trace.add_point( [0,0,0] )
        trace.add_point( [1,0,0] )
        trace.add_point( [1,1,0] )
        trace.add_point( [0,1,0] )
        trace.add_point( [0,0,1] )
        objs.append( trace )
        
    center = [0,0,0]
    offset = 0.75
    cam.center = center 
    cam.r      = offset
    cam.dR     =  0.050
    nearClip   =  0.01
    farClip    = 10.0


    window = OGL_App( objs , # ------------------------- List of objects to render
                      caption = "Tilt-In"  , # --------- Window caption
                      clearColor = [ 0 , 0 , 0 , 1 ] ) # BG color black


    window.set_camera( *cam.get_cam_vectors() )
    window.set_view_params( 75 , nearClip , farClip )

    @window.event
    def on_key_press( symbol , modifiers ):
        # Handle Keyboard Events
        if symbol == key.LEFT:
            cam.orbit_neg()
            if _DEBUG: print( "Theta:" , cam.th )
        
        if symbol == key.RIGHT:
            cam.orbit_pos()
            if _DEBUG: print( "Theta:" , cam.th )
        
        if symbol == key.UP:
            cam.angle_inc()
            if _DEBUG: print( "Psi:" , cam.ps )
        
        if symbol == key.DOWN:
            cam.angle_dec()
            if _DEBUG: print( "Psi:" , cam.ps )
        
        # Alphabet keys:
        elif symbol == key.O:
            cam.zoom_out()
            if _DEBUG: print( "d:" , cam.r )
            
        elif symbol == key.P:
            cam.zoom_in()
            if _DEBUG: print( "d:" , cam.r )

        # Number keys:
        elif symbol == key._1:
            pass

        # Number keypad keys:
        elif symbol == key.NUM_1:
            pass

        # Modifiers:
        if modifiers & key.MOD_CTRL:
            pass

    window.set_camera( *cam.get_cam_vectors() )

    if _DEBUG: 
        print( [ window.p_point_visible( pnt ) for pnt in trace.vertices ] )
        print( [ window.point_in_view(pnt)['dist'] for pnt in trace.vertices ] )
        print( cam.get_cam_vectors() )

    i = 0


    # 4. Draw & Display
    while not window.has_exit:
        
        # A. Set camera
        window.set_camera( *cam.get_cam_vectors() )
        if _DEBUG: window.prnt_view_params()
        
        # B. Animate Axes
        
        # D. Redraw
        window.dispatch_events() # Handle window events
        window.on_draw() # Redraw the scene
        window.flip()
        
        # E. Slow framerate
        time.sleep( 1/10 )
