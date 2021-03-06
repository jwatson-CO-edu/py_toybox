#!/usr/bin/env python3



# James Watson , 2019 August


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
import pyglet
from pyglet.window import key
from pyglet.gl import ( glColor3ub , GL_TRIANGLES )


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
        
        self.set_verts( [ front , bottom , back , top , rghtWTip , leftWTip ] )
        #                 0     , 1      , 2    , 3   , 4        , 5
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
        
        # 2. Set color
        # FIXME
        
    def draw( self ):  
        """ Render the StarGlider """
        # 1. Transform points
        self.xform_lab()
        # 2. Render!
        # 2. Set color
        glColor3ub( *self.color )
        pyglet.graphics.draw_indexed( 
            6 , # ------------------ Number of seqential triplet in vertex list
            GL_TRIANGLES , # ------- Draw quadrilaterals
            self.triangles , # ----- Indices where the coordinates are stored
            ( 'v3f' , self.labVerts ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
        )

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
