#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division

"""
voxel-pyglet.py
Robin Guzniczak & James Watson , 2017 March
Extension of a simple voxel engine originally by Robin Guzniczak 

~~ NOTES ~~
* Maybe pyglet would handy seeing how things are situated in 3D? , Note that pyglet is not limited to voxels! It is a general OpenGL wrapper!
* Voxel Engine , C++ & Python: http://bytebash.com/tag/pyglet/

~~ TODO ~~
[ ] Interactive camera , Fly
    [X] Simplest kb interaction to move camera
    [ ] Sensible camera flight , such that the camera focus is a direction rather than a point , consider Vector3D!
    [ ] Rotate camera with mouse
    [ ] Hold arrow keys to keep flying
[ ] Add FPS , position , and other metrics to the screen
[X] Fix the drawing order of the voxels # glEnable( GL_DEPTH_TEST )
[ ] Optimization I
    [X] Backface culling # glEnable( GL_CULL_FACE ) 
        # http://nullege.com/codes/show/src@p@r@Printrun-HEAD@printrun@stlview.py/119/pyglet.gl.GL_CULL_FACE
    [ ] Interior voxel culling , Use Voxelyze as an example , This should only update if voxels are changed and not change with the view
    [ ] Visible frustum , There is a LOT of research on doing this quickly , probably take advantage of voxel setting and test by voxel centers , easy?
[ ] Interactive camera , Walk
[ ] Generate terrain
"""

# == INIT ==================================================================================================================================
import sys, os.path # To make changes to the PATH

def first_valid_dir(dirList):
    """ Return the first valid directory in 'dirList', otherwise return False if no valid directories exist in the list """
    rtnDir = False
    for drctry in dirList:
        if os.path.exists( drctry ):
			rtnDir = drctry 
			break
    return rtnDir
        
def add_first_valid_dir_to_path(dirList):
    """ Add the first valid directory in 'dirList' to the system path """
    # In lieu of actually installing the library, just keep a list of all the places it could be in each environment
    validDir = first_valid_dir(dirList)
    print __file__ , "is attempting to load a path ...",
    if validDir:
        if validDir in sys.path:
            print "Already in sys.path:", validDir
        else:
            sys.path.append( validDir )
            print 'Loaded:', str(validDir)
    else:
        raise ImportError("None of the specified directories were loaded") # Assume that not having this loaded is a bad thing
# List all the places where the research environment could be
envPaths = [ 'D:\Utah_Research\Assembly_Planner\AsmEnv' ,
             'F:\Utah_Research\Assembly_Planner\AsmEnv' ,
             '/media/mawglin/FILEPILE/Utah_Research/Assembly_Planner/AsmEnv',
             '/media/jwatson/FILEPILE/Utah_Research/Assembly_Planner/AsmEnv']
add_first_valid_dir_to_path( envPaths )
add_first_valid_dir_to_path( [ os.path.join( path , 'VectorMath' ) for path in envPaths ] )

# ~~ Imports ~~
# ~ Standard ~
from random import randint
from math import atan2
# ~ Special ~
import pyglet # 3D graphics for Python
from pyglet.gl import * # Rendering controls
from pyglet.window import key # kb & mouse interaction
from pyglet.window import mouse
# ~ Local ~
from Vector import *
from Vector3D import *

# == END INIT ==============================================================================================================================

# == Voxel Engine ==

class VoxelEngine:
    """ The simplest voxel engine """
	
    def __init__( self , w , h , d ):
	""" Create a new voxel engine. """
	self.w = w # Create a world with 'w'idth , 'h'eight , and 'depth' bounds
	self.h = h
	self.d = d
	# Create the 3D array to hold bricks
	self.voxels = []
	for _ in range( self.w ):
	    self.voxels.append( [ [ 0 for _ in range( self.d ) ] for _ in range( self.h ) ] )
	
    def set( self , x , y , z , value ):
	""" Set the value of the voxel at position (x, y, z). """
	self.voxels[x][y][z] = value
    
    def draw( self ):
	""" Draw the voxels. """ # NOTE: This function iterates through all possible addresses within 'w'idth , 'h'eight , and 'depth' and
	#                                renders voxels were a block value has been stored. Would be nice to have some kind of sparse lookup
	vertices = (
	    0 , 0 , 0 ,	# vertex 0    3-------2     # NOTE: Y+ is UP in the original voxel engine from Guzniczak
	    0 , 0 , 1 ,	# vertex 1    !\      !\
	    0 , 1 , 0 ,	# vertex 2    ! \     Y \
	    0 , 1 , 1 ,	# vertex 3    !  7=======6
	    1 , 0 , 0 ,	# vertex 4    1--|Z---0  |
	    1 , 0 , 1 ,	# vertex 5     \ |     \ |
	    1 , 1 , 0 ,	# vertex 6      \|      X|
	    1 , 1 , 1 ,	# vertex 7       5=======4
	)
	indices = ( #                                          NOTE: Vertices must have CCW order to point the normals towards exterior , 
	    0 , 1 , 3 , 2 , # top face                               right hand rule , otherwise dot products computed for backface-culling 
	    4 , 6 , 7 , 5 , # bottom face  # 4 , 5 , 7 , 6 ,         will have the wrong sign! faces vanish!
	    0 , 2 , 6 , 4 , # left face    # 0 , 4 , 6 , 2 ,
	    1 , 5 , 7 , 3 , # right face
	    0 , 4 , 5 , 1 , # down face    # 0 , 1 , 5 , 4 , 
	    2 , 3 , 7 , 6 , # up face
        )
	colors = (
	    ( 107 ,  83 ,  28 ) , # dirt
	    (  18 , 124 ,  39 ) , # grass
	    ( 168 , 142 ,  95 ) , # wood
	    (  88 , 181 ,  74 ) , # leaves
        )
	
	# TODO: If it happens that pyglet does not have an easy to use depth buffer , then it might be fairly easy to paint voxels in 
	#       Manhattan distance order from far to near to the camera
	
	# Loop through each address , draw voxel at address if a brick value has been stored at the address
	for x in range( self.w ): # for each X addr across the width of the world
	    for y in range( self.h ): # for each Y addr across the height of the world
		for z in range( self.d ): # for each Z addr across the depth of the world
		    voxel_type = self.voxels[x][y][z] # Get the value stored at the address
		    if voxel_type != 0: # if the map indicates a brick at this address , draw it
			# Go to the voxel location for drawing , https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glTranslate.xml
			# If the matrix mode is either GL_MODELVIEW or GL_PROJECTION, all objects drawn after a call to glTranslated are translated.
			glTranslated( x , y , z ) # This moves the origin of drawing , so that we can use the above coordinates at each draw location
			glColor3ub( *colors[ voxel_type - 1 ] ) # Get the color according to the voxel type
			pyglet.graphics.draw_indexed( 
			    8 , # Use 8 for 'GL_QUADS'
			    GL_QUADS , # Draw quadrilaterals
			    indices , # The indices where the coordinates are stored
			    ( 'v3i' , vertices ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
			)
			""" URL: http://pyglet.readthedocs.io/en/pyglet-1.2-maintenance/programming_guide/graphics.html#vertex-lists
			
			There is a significant overhead in using pyglet.graphics.draw and pyglet.graphics.draw_indexed due to pyglet 
			interpreting and formatting the vertex data for the video device. Usually the data drawn in each frame (of an animation) 
			is identical or very similar to the previous frame, so this overhead is unnecessarily repeated.

			A VertexList is a list of vertices and their attributes, stored in an efficient manner that’s suitable for direct 
			upload to the video card. On newer video cards (supporting OpenGL 1.5 or later) the data is actually stored in video memory.
			"""
			glTranslated( -x , -y , -z ) # Reset the transform coordinates

# == End Voxel ==


# == Rendering ==

class Camera( Pose ):
    """ A Pose representing the location and direction of the camera """
    
    # def __init__( self , position , focus , upPnt , winWdth , winHght ):
    def __init__( self , position , gazeDir , upDir , winWdth , winHght ):
	""" Create a camera object at a 'position' , looking at a 'focus' point , with 'upPnt' in the vertical plane that includes the camera """
	# gazeDir = vec_dif_unt( focus , position ) # Unit vector for the direction the camera is looking
	# upDir = vec_dif_unt( upPnt , position ) # Assume a point in the vertical plane was specified , otherwise camera will be conked
	yBasis = np.cross( upDir , gazeDir )
	zBasis = np.cross( gazeDir , yBasis ) # Don't assume that the up point forms a proper basis
	Pose.__init__( self , position , Quaternion.principal_rot_Quat( gazeDir , yBasis , zBasis ) )
	self.winWdth = winWdth
	self.winHght = winHght
	self.gazeVec = [ 0 , 0 , 1 ] # Look in the direction of the Z basis vector
	self.upVec =   [ 0 , 1 , 0 ] # Up in the direction of the Y basis vector
	self.xBasis =  [ 1 , 0 , 0 ]
	self.gazeLab = self.gazeVec[:]
	self.upLab = self.upVec[:]
	self.xLab = self.xBasis[:]
	self.XsensYaw = 0.10 # X sensitivity # dx / windowWidth  * XsensYaw = radians YAW per window width moved
	self.YsensPtc = 0.10 # Y sensitivity # dy / windowHeight * YsensPtc = radians PITCH per window height moved
	self.set_yaw_pitch_from_vec( gazeDir )
	
    def update_dir( self ):
	""" Update the gaze and up vectors """
	self.gazeLab =  self.orientation.apply_to( self.gazeVec )
	self.upLab =    self.orientation.apply_to( self.upVec )
	self.xLab =     self.orientation.apply_to( self.xBasis )
    
    def window_rescale( self , winWdth , winHght ): # This is probably a bad idea because it changes UI unexpectedly?
	""" When the window is rescaled , rescale the effect of mouse motion """ 
	self.winWdth = winWdth
	self.winHght = winHght	
	
    def set_yaw_pitch_from_vec( self , lookDir ):
	""" Get the yaw / pitch that will point the camera at 'lookPoint' in the world frame """
	# relVec = np.subtract( lookPoint , self.position ) # Get the direction of the point relative to the camera origin
	# YAW about the world Y axis
	[ rad , lookPitch , lookYaw ] = cart_2_radPtcYaw_YUP( lookDir )
	print "YAW:  " , lookYaw
	print "PITCH:" , lookPitch
	self.yaw = lookYaw
	self.ptc = lookPitch
	
    def turn_with_mouse( self , dx , dy ):
	""" Add yaw and pitch to the camera given mouse motion """
	self.yaw += dx / self.winWdth * self.XsensYaw
	self.ptc += dy / self.winHght * self.YsensPtc
	print "YAW:  " , self.yaw
	print "PITCH:" , self.ptc
	self.orientation = Quaternion.serial_rots( 
	    # Quaternion.k_rot_to_Quat( [ 1 , 0 , 0 ] , -self.ptc  ) , # Apply PITCH
	    Quaternion.k_rot_to_Quat( [ 0 , 1 , 0 ] ,  self.yaw  ) , # Apply YAW
	    Quaternion.k_rot_to_Quat( [ 1 , 0 , 0 ] , -self.ptc  ) , # Apply PITCH
	) 
	self.update_dir()
	
    def move_in_cam_frame( self , vec ):
	""" Displace the camera by 'vec' in its own frame , assumes that the basis vectors have been calculated in the lab frame """
	self.translate( transform_by_bases( vec , self.xLab , self.upLab , self.gazeLab ) )
	
    def calc_glLookAt_args( self ):
	""" Get a list of arguments for glLookAt that will represent this camera pose """
	rtnVec = self.position[:]
	rtnVec.extend( np.add( self.position , self.gazeLab ) ) # FIXME: NUMPY ARRAY DOES NOT HAVE AN EXTEND METHOD!
	rtnVec.extend( np.add( self.position , self.orientation.apply_to( self.upVec ) ) )
	return rtnVec
	

class Window(pyglet.window.Window):
    """ Rendering window and event loop """
    
    def __init__(self):
	""" Init a resizable window and event loop """
	super( Window , self ).__init__( resizable = True, caption = 'Pyglet Voxel Extension')
	self.voxel = VoxelEngine( 20 , 25 , 20 ) # Init the voxel engine with world dimensions
	glClearColor( 0.7 , 0.7 , 0.8 , 1 )
	self.generate_island(  0 ,  5 ,  0 )
	self.generate_island(  0 ,  0 , 10 )

    def generate_island( self , x , y , z ):
	""" Populate the world with a floating island with a tree """
	# a flying island
	for dx in range( randint( 4 , 10 ) ):
	    for dz in range( randint( 4 , 10 ) ):
		for dy in range( randint( 4 , 11 ) ):
		    self.voxel.set( x + dx , 15 - dy + y , z + dz , 1 )
		self.voxel.set( x + dx , y + 15 , z + dz , 2 )
	# a tree
	for i in range( 15 , 18 ):
	    self.voxel.set( x + 2 , y + i , z + 4 , 3 )
	for i in range( 1 , 4 ):
	    for j in range( 3 , 6 ):
		self.voxel.set( x + i , y + 18 , z + j , 4 )
	self.voxel.set( x + 2 , y + 19 , z + 4 , 4 )

    def on_draw( self ):
	""" Repaint the window , per-frame activity """
	self.clear() # Erase window
	self.setup_3D() # Set up the GL context
	self.voxel.draw() # Ask the voxel engine to paint all of the voxel faces

    def setup_3D( self ):
	""" Setup the 3D matrix """
	# glEnable( GL.GL_DEPTH_TEST )
	glEnable( GL_DEPTH_TEST )
	glMatrixMode( GL_PROJECTION )
	glLoadIdentity()
	gluPerspective( 70 , self.width / float( self.height ) , 0.1 , 200 )
	glMatrixMode( GL_MODELVIEW )
	glLoadIdentity()
	gluLookAt( *camera )
	
# == End Rendering ==


# == Main and Interaction ==

if __name__ == '__main__':
    # Create display window , set up camera , begin main event loop
    
    window = Window()
    
    # = Camera and Controls =
    
    # URL: https://www.opengl.org/discussion_boards/showthread.php/165839-Use-gluLookAt-to-navigate-around-the-world
    camera = [ 24 , 20 , 20 , # eyex    , eyey    , eyez    : Camera location , point (world) , XYZ
	        0 , 10 ,  4 , # centerx , centery , centerz : Center of the camera focus , point (world) , XYZ
	        0 ,  1 ,  0 ] # upx     , upy     , upz     : Direction of "up" in the world frame , vector , XYZ
    #                ^--------------------^-- Y is up because graphics people are silly , sensible people know Z is up
    #                                         I can set "up" to be anything I want!
    
    camObj = Camera( [ 24 , 20 , 20 ] , np.subtract( [ 0 , 10 ,  4 ] , [ 24 , 20 , 20 ] ) , [ 0 ,  10 ,  0 ] , window.width , window.height )
    initOrientation = str( camObj.orientation ) # Store the initial orientation
    moveMag = 2
    
    @window.event
    def on_key_press( symbol , modifiers ):
	global camera
	print 'A key was pressed'
	if symbol == key.UP:
	    print 'The up arrow was pressed.'
	    # camera[0] += 1
	    camObj.move_in_cam_frame( [ 0 , 0 , moveMag ] )
	elif symbol == key.DOWN:
	    print 'The down arrow key was pressed.'   
	    # camera[0] -= 1
	    camObj.move_in_cam_frame( [ 0 , 0 , -moveMag ] )
	elif symbol == key.RIGHT:
	    print 'The right arrow key was pressed.'
	    # camera[2] += 1
	    camObj.move_in_cam_frame( [ -moveMag , 0 , 0 ] )
	elif symbol == key.LEFT:
	    print 'The left arrow  was pressed.'   
	    # camera[2] -= 1
	    camObj.move_in_cam_frame( [ moveMag , 0 , 0 ] )
	# print "glLookAt:" , camObj.calc_glLookAt_args()
	
    @window.event
    def on_mouse_press( x , y , button , modifiers ):
	if button == mouse.LEFT:
	    print 'The left mouse button was pressed.'   

    @window.event
    def on_mouse_motion( x , y , dx , dy ):
	global camera
	camObj.turn_with_mouse( dx , dy )
	camera = camObj.calc_glLookAt_args()
	print "Mouse Look , glLookAt:" , camera
    
    # = End Camera =
    
    # ~ Run Graphics Window ~
    pyglet.app.run()
    
    # ~ Post-Window Report ~
    print "PRINT THIS AFTER THE LOOP EXITS"

# == End Main ==