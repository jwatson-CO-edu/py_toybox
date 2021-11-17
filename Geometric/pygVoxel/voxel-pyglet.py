#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
voxel-pyglet.py
Robin Guzniczak , 2016 March
A simple voxel engine originally by Robin Guzniczak , with additional comments from James Watson
Maybe pyglet would handy seeing how things are situated in 3D?

~~ NOTES ~~
Voxel Engine , C++ & Python: http://bytebash.com/tag/pyglet/

~~ TODO ~~
[ ] Interactive camera , Fly
[ ] Add FPS , position , and other metrics to the screen
[ ] Backface culling , calc normals from edges and store # glEnable(GL_CULL_FACE) # http://nullege.com/codes/show/src@p@r@Printrun-HEAD@printrun@stlview.py/119/pyglet.gl.GL_CULL_FACE
[ ] Interior voxel culling , Use Voxelyze as an example , This should only update if voxels are changed and not change with the view
[ ] Visible frustum , There is a LOT of research on doing this quickly , probably take advantage of voxel setting and test by voxel centers , easy?
[ ] Interactive camera , Walk
[ ] Generate terrain
"""

import pyglet
import random
from pyglet.gl import *

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
	    0 , 0 , 0 ,	# vertex 0
	    0 , 0 , 1 ,	# vertex 1
	    0 , 1 , 0 ,	# vertex 2
	    0 , 1 , 1 ,	# vertex 3
	    1 , 0 , 0 ,	# vertex 4
	    1 , 0 , 1 ,	# vertex 5
	    1 , 1 , 0 ,	# vertex 6
	    1 , 1 , 1 ,	# vertex 7
	)
	indices = (
	    0 , 1 , 3 , 2 , # top face
	    4 , 5 , 7 , 6 , # bottom face
	    0 , 4 , 6 , 2 , # left face
	    1 , 5 , 7 , 3 , # right face
	    0 , 1 , 5 , 4 , # down face
	    2 , 3 , 7 , 6 , # up face
        )
	colors = (
	    ( 107 ,  83 ,  28 ) , # dirt
	    (  18 , 124 ,  39 ) , # grass
	    ( 168 , 142 ,  95 ) , # wood
	    (  88 , 181 ,  74 ) , # leaves
        )
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


class Window(pyglet.window.Window):
    """ Rendering window and event loop """
    
    def __init__(self):
	""" Init a resizable window and event loop """
	super( Window , self ).__init__( resizable = True, caption = 'Pyglet Voxel Demo')
	self.voxel = VoxelEngine( 20 , 25 , 20 ) # Init the voxel engine with world dimensions
	glClearColor( 0.7 , 0.7 , 0.8 , 1 )
	self.generate_island(  0 ,  5 ,  0 )
	self.generate_island(  0 ,  0 , 10 )

    def generate_island( self , x , y , z ):
	""" Populate the world with a floating island with a tree """
	# a flying island
	for dx in range( random.randint( 4 , 10 ) ):
	    for dz in range( random.randint( 4 , 10 ) ):
		for dy in range( random.randint( 4 , 11 ) ):
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
	self.clear()
	self.setup_3D()
	self.voxel.draw()

    def setup_3D( self ):
	""" Setup the 3D matrix """
	glMatrixMode( GL_PROJECTION )
	glLoadIdentity()
	gluPerspective( 70 , self.width / float( self.height ) , 0.1 , 200 )
	glMatrixMode( GL_MODELVIEW )
	glLoadIdentity()
	# URL: https://www.opengl.org/discussion_boards/showthread.php/165839-Use-gluLookAt-to-navigate-around-the-world
	gluLookAt( 24 , 20 , 20 , # eyex    , eyey    , eyez    : Camera location , point , XYZ
	            0 , 10 ,  4 , # centerx , centery , centerz : Direction camera is pointing , vector , XYZ
	            0 ,  1 ,  0 ) # upx     , upy     , upz     : Direction of "up" in the world frame , vector , XYZ
	#                ^--------------------^-- Y is up because graphics people are silly , everyone knows Z is up

if __name__ == '__main__':
    window = Window()
    pyglet.app.run()
