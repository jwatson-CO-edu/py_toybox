#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
voxel_test.py
Robin Guzniczak & James Watson , 2017 July
Simple voxel engine to test the Pyglet package

~~ NOTES ~~
* Maybe pyglet would handy seeing how things are situated in 3D? , Note that pyglet is not limited to voxels! It is a general OpenGL wrapper!
* Voxel Engine , C++ & Python: http://bytebash.com/tag/pyglet/

~~ TODO ~~
[Y] Figure out why my barebones example "render_cuboid.py" does not work - COMPLETE: I had reordered commands that affect view and camera
                                                                                     that need to be in a certain order!
[N] Strip this file down until it either stops working or does what I want - ABANDONED: "render_cuboid.py" is now functional!
"""

# == INIT ==================================================================================================================================
# ~~ Imports ~~
# ~ Standard ~
from random import randint
# ~ Special ~
import numpy as np
import pyglet # 3D graphics for Python
from pyglet.gl import * # Rendering controls
from pyglet.window import key # kb & mouse interaction
from pyglet.window import mouse
# ~ Local ~
# from Vector import *
# from Vector3D import *

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
                            ( 'v3f' , np.multiply( vertices , 1.5 ) ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
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

class Window(pyglet.window.Window):
    """ Rendering window and event loop """
    
    def __init__(self):
        """ Init a resizable window and event loop """
        super( Window , self ).__init__( resizable = True, caption = 'Pyglet Rendering Test')
        self.voxel = VoxelEngine( 20 , 25 , 20 ) # Init the voxel engine with world dimensions
        glClearColor( 0.7 , 0.7 , 0.8 , 1 )
        # self.generate_island(  0 ,  5 ,  0 )
        # self.generate_island(  0 ,  0 , 10 )
        self.set_one_cube( 0 , 0 , 0 )
        
    def generate_island( self , x , y , z ):
        """ Populate the world with a floating island with a tree """
        # a flying island
        for dx in range( randint( 4 , 10 ) ):
            for dz in range( randint( 4 , 10 ) ):
                for dy in range( randint( 4 , 11 ) ):
                    self.voxel.set( x + dx , 15 - dy + y , z + dz , 1 )
                    self.voxel.set( x + dx , y + 15 , z + dz , 2 )
        # a tree
        for i in range( 15 , 18 ): # Trunk
            self.voxel.set( x + 2 , y + i , z + 4 , 3 )
        for i in range( 1 , 4 ): # Branches
            for j in range( 3 , 6 ):
                self.voxel.set( x + i , y + 18 , z + j , 4 )
                self.voxel.set( x + 2 , y + 19 , z + 4 , 4 )
                
    def set_one_cube( self , x , y , z ):
        """ Put only one voxel at 'x' , 'y' , 'z' , This is the least test of the drawing framework! """
        self.voxel.set( x , y , z , 4 )
        print "Put one voxel at " , x , y , z
                
    def on_draw( self ):
        """ Repaint the window , per-frame activity """
        self.clear()
        self.setup_3D()
        self.voxel.draw()
        
    def setup_3D( self ):
        """ Setup the 3D matrix """
        # Use 'GL_DEPTH_TEST' to ensure that OpenGL maintains a sensible drawing order for polygons no matter the viewing angle
        # glEnable( GL_DEPTH_TEST ) # Do these setup functions really have to be run every single frame? # TODO: Try moving these to the '__init__' , see what happens
        # glEnable( GL_CULL_FACE ) # Uncomment to preform backface culling , however the present ordering of the vertices is somehow not right
        #                            http://stackoverflow.com/questions/23320017/incorrect-occluded-front-face-culling-in-opengl
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
    camera = [  4 ,  4 ,  4 , # eyex    , eyey    , eyez    : Camera location , point (world) , XYZ
                0 ,  0 ,  0 , # centerx , centery , centerz : Center of the camera focus , point (world) , XYZ
                0 ,  0 ,  1 ] # upx     , upy     , upz     : Direction of "up" in the world frame , vector , XYZ
    
    @window.event
    def on_key_press( symbol , modifiers ):
        """ Pyglet window event handler for the kb """
        global camera
        print 'A key was pressed'
        if symbol == key.UP:
            print 'The up arrow was pressed.'
            camera[0] -= 1
        elif symbol == key.DOWN:
            print 'The down arrow key was pressed.'   
            camera[0] += 1
        elif symbol == key.RIGHT:
            print 'The right arrow key was pressed.'
            camera[2] += 1
        elif symbol == key.LEFT:
            print 'The left arrow  was pressed.'   
            camera[2] -= 1
            
    # = End Camera =
    
    pyglet.app.run()
    
# == End Main ==