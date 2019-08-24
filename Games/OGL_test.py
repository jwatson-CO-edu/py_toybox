import marchhare.OGL_Shapes

#!/usr/bin/env python3
# show_spiral.py
# James Watson , 2019 August
# Show a spiral insertion operation

import os , sys , time

from random import randrange
from math import pi
import numpy as np
from OGL_Shapes import OGL_App , Point_OGL , CartAxes , Vector_OGL , Trace_OGL
from pyglet.window import key

from dataProcess import *
from math_kit import vec_sphr

libPath = os.path.join( os.path.expanduser( '~' ) , 'dev_rmstudio/lib/' )
print( libPath )

sys.path.insert( 0 , libPath )

_DEBUG = False

# ~~ Render Data ~~

objs = []

_SHOWTRACE = 1

cam = CameraOrbit()

tcpAxes = CartAxes( unitLen = 0.002 )
forceVc = Vector_OGL()
torqVec = Vector_OGL()
torqVec.color = ( 200 , 200 , 200 )

if _SHOWTRACE:
    trace = Trace_OGL()
    trace.set_color( (255,255,255,) )
    for pnt in positions:
        trace.add_point( pnt )
        if _DEBUG: print( "Adding:" , pnt )
    objs.append( trace )
    center = positions[-1]
    offset = 0.005
    cam.center = center 
    cam.r      = offset
    cam.dR     = 0.0005
    nearClip   = 0.001
    farClip    = 0.750
    
    objs.append( tcpAxes )
    objs.append( forceVc )
    objs.append( torqVec )
    
else:
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
    cam.dR     = 0.050
    nearClip   = 0.001
    farClip    = 0.100


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
    if _SHOWTRACE:
        index = i % len( posSeries )
        i += 1
        tcpXform = poselib.pose_vec_to_mtrx( posSeries[ index ] )
        tcpAxes.xform = tcpXform
        forceVc.xform = tcpXform
        torqVec.xform = tcpXform
        
        # C. Animate forces
        forceVc.set_origin_displace( [0,0,0] ,
                                     np.multiply( forces[ index ] , 0.0001 ) )
        torqVec.set_origin_displace( [0,0,0] ,
                                     np.multiply( torques[ index ] , 0.0005 ) )
        
    
    # D. Redraw
    window.dispatch_events() # Handle window events
    window.on_draw() # Redraw the scene
    window.flip()
    
    # E. Slow framerate
    time.sleep( 1/10 )
