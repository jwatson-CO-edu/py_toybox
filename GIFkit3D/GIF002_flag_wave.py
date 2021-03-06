#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division # MUST be run before all other expressions , including docstrings!

"""
GIF002_flag_wave.py
James Watson , 2018 March , Written on Spyder 3 / Python 2.7 , Template Version 2017-10-26
Flag waves while the camera orbits

Dependencies: numpy , pyglet , imageio , marchhare

NOTE , 2018-03-22: ERROR OCCURS WHILE RUNNING UNDER UBUNTU 16.04 , LAST THIRD OF THE ANIMATION RUNS AT A GREATLY INCREASED FRAMERATE
                   This does not currently happen under Windows 10
                   
Process: [Y] 0. Move previous optimized output to "Gallery" directory
         [Y] 1. Move functions from previous work to "GIFtools.py"
         [Y] 2. Generate & Record in Windows (Python)
         [ ] 3. Optimize GIF in Linux (GIFsicle)
         [ ] 4. Verify (Browser)
         [ ] 5. Post
"""

"""
~~~ DEV PLAN ~~~
[Y] Finish WavyFlag
[Y] Rotate about static flag to verify that both sides and border render
[Y] Wavy ( cos , sin ) in planes that intersects top and bottom edges and is perpendiular to the face of an unperturbed, flat flag
[Y] Adjust to colors that will be used in Mobius
[Y] Adjust rotation period and wave period to a harmonic - There appears to be a small jump.  Experiment with onsies twosies frame adjustment
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
from marchhare.marchhare import flatten_nested_sequence , ensure_dir , build_sublists_by_cadence
from marchhare.Vector import vec_random_range , vec_unit , vec_mag
from marchhare.VectorMath.SpatialVectorRobot import rot_matx_ang_axs , z_rot
from marchhare.OGLshapes import Vector_OGL , OGL_App , Icosahedron_Reg , OGLDrawable
from GIFtools import CircleOrbit 

# ~~ Aliases & Shortcuts ~~
endl    = os.linesep # - Line separator
infty   = float('inf') # Infinity
EPSILON = 1e-8 # ------- A very small number below the precision we care about

# ___ End Init _____________________________________________________________________________________________________________________________

def tri_normal( p0 , p1 , p2 ):
    """ Return the unit normal vector for a triangle with points specified in CCW order """
    vec1 = np.subtract( p1 , p0 )
    vec2 = np.subtract( p2 , p0 )
    return vec_unit( np.cross( vec1 , vec2 ) )

def double_all_elem_except( inList , exceptedIndices = [] ):
    """ Double all elements of a list except those indicated by 'exceptedIndices' """
    rtnList = []
    for i , elem in enumerate( inList ):
        if i in exceptedIndices:
            rtnList.append( elem )
        else:
            rtnList.extend( [ elem , elem ] )
    return rtnList

def double_all_middle_vertices( inList , cadence = 3 ):
    """ Double all elements of a vertex list except the first and last """
    # NOTE: This is only necessary for the indices, not the vertices themselves
    coordList = build_sublists_by_cadence( inList , cadence )
    rtnList = []
    lastDex = len( coordList ) - 1 
    for i , elem in enumerate( coordList ):
        if i == 0 or i == lastDex:
            rtnList.append( elem )
        else:
            rtnList.extend( [ elem , elem ] )
    return flatten_nested_sequence( rtnList )
        

# == class WavyFlag ==    

class WavyFlag( OGLDrawable ):
    """ Waving flag made of vertical strips , Each side is represented by a separate set of triangles to allow a bicolor effect """
    # NOTE: This class does not model fabric , does not conserve area , and does not have a "rest state"
    
    def __init__( self , topEdgePoints , btmEdgePoints , sepDist = 1 , absolutePoints = True ):
        """ Create a wavy flag with its origin at the first point in 'topEdgePoints' """
        # 2018-03-23 , NOTE: At this time only the default 'absolutePoints' mode is considered.  Relative mode is not considered
        # 0---1---2 ... 'topEdgePoints'
        # |  /|  /|
        # | / | / | ... There are two triangles for every corresponding top-btm pair following the 0-pair , 0-pair is the leading edge
        # |/  |/  |
        # 0---1---2 ... 'btmEdgePoints'
        if absolutePoints:
            # The default mode is to specify all of the vertices in lab frame coordinates , no whole-model transform is performed
            OGLDrawable.__init__( self , [ 0.0 , 0.0 , 0.0 ] ) # -- Parent class init , Center will be used for OGL rendering transform
        else:
            # The alternate mode is to specify nonrigid 'vertices' that can be further transformed to the overall flag pose in the lab frame
            OGLDrawable.__init__( self , topEdgePoints[0] ) # -- Parent class init , Center will be used for OGL rendering transform
        self.numPts = len( topEdgePoints ) # Both lists must be the same length , Drawing stops before this index
        self.numTri = 2 * ( self.numPts - 1 )
        self.numSeg = 2 * self.numPts
        self.set_edge_points( topEdgePoints , btmEdgePoints )
        self.separation = sepDist * 1.0 # Ensure it is float
        self.colors = [ [ 255 , 255 , 255 ] , # Border
                        [ 255 ,   0 ,   0 ] , # Side 1
                        [   0 ,   0 , 255 ] ] # Side 2
        self.calc_render_geo( topEdgePoints , btmEdgePoints )
        
    def set_edge_points( self , topEdgePoints , btmEdgePoints ):
        """ Store the edge points , enforce equal length """
        if len( topEdgePoints ) != len( btmEdgePoints ):
            raise IndexError( "'topEdgePoints' and 'btmEdgePoints' must be of equal length!" )
        else:
            self.topEdge = topEdgePoints[:]
            self.btmEdge = btmEdgePoints[:]
        
    def set_colors( self , borderClr , side1clr , side2clr ):
        """ Set the colors for the border , side 1 , and side 2 , respectively """
        self.colors = [ borderClr , 
                        side1clr  , 
                        side2clr  ];
        
    def calc_render_geo( self , topEdgePoints , btmEdgePoints ):
        """ Calculate the triangles for the bicolor effect """
        # Requirements:  1. Adjacent triangles must meet  2. Sides should not intersect
        top1 = [] ; btm1 = [] # Positive N
        top2 = [] ; btm2 = [] # Negative N
        self.vertX1 = [] # ----- Master list of side 1 vertices
        self.vertX2 = [] # ----- Master list of side 2 vertices
        self.F = [] # Side 1 / 2
        self.linDices = [] # Border
        # n_top = [ 0 , numPts - 1 ] , n_btm = [ numPts , 2 * numPts - 1 ]
        topHalfBase = 0;
        btmHalfBase = self.numPts;
        # 0. For each pair of edge points
        for i in xrange( 1 , self.numPts ):
            # 1. Extract triangles for this pair
            topTri = [ topEdgePoints[i][:] , topEdgePoints[i-1][:] , btmEdgePoints[i-1][:] ]
            btmTri = [ btmEdgePoints[i][:] , topEdgePoints[i][:]   , btmEdgePoints[i-1][:] ]
            # 5. Get face indices for both layers
            self.F.extend( [ topHalfBase + i , topHalfBase + i - 1 , btmHalfBase + i - 1 ,
                             btmHalfBase + i , topHalfBase + i     , btmHalfBase + i - 1 ] )
            # 2. Get triangle normals
            N_top = tri_normal( *topTri )
            N_btm = tri_normal( *btmTri )
            # 3. Separate points into 2 layers by spacing them by their normals
            if i == 1: # If this is the first pair , then ensure that the leading edge is properly separated and stored
                top1.append( np.add( topEdgePoints[0] , 
                                     np.multiply( N_top ,  self.separation / 2.0 ) ) )
                top2.append( np.add( topEdgePoints[0] , 
                                     np.multiply( N_top , -self.separation / 2.0 ) ) )
                btm1.append( np.add( btmEdgePoints[0] , 
                                     np.multiply( N_btm ,  self.separation / 2.0 ) ) )
                btm2.append( np.add( btmEdgePoints[0] , 
                                     np.multiply( N_btm , -self.separation / 2.0 ) ) )
            top1.append( np.add( topEdgePoints[i] , 
                                 np.multiply( N_top ,  self.separation / 2.0 ) ) )
            top2.append( np.add( topEdgePoints[i] , 
                                 np.multiply( N_top , -self.separation / 2.0 ) ) )
            btm1.append( np.add( btmEdgePoints[i] , 
                                 np.multiply( N_btm ,  self.separation / 2.0 ) ) )
            btm2.append( np.add( btmEdgePoints[i] , 
                                 np.multiply( N_btm , -self.separation / 2.0 ) ) )
        # 4. Load all of the points into a flat structure
        self.vertX1 = flatten_nested_sequence( [ top1 , btm1 ] )
        self.vertX2 = flatten_nested_sequence( [ top2 , btm2 ] )
        # 6. Load the original points into a flat structure
        self.borderVerts = flatten_nested_sequence( [ topEdgePoints , btmEdgePoints ] )
        # 7. Get edge indices for the flag border
        self.linDices = flatten_nested_sequence( [ double_all_elem_except( range( self.numPts ) , [ 0 ] )  , 
                                                   double_all_elem_except( range( 2 * self.numPts - 1 , self.numPts - 1 , -1 ) ) ,
                                                   0 ] )
        
        # ~ DEBUG OUTPUT ~
        #print "DEBUG , Side 1 has" , len( self.vertX1 ) , "vertex elements , Elem 0:" , self.vertX1[0]
        #print "DEBUG , Side 2 has" , len( self.vertX2 ) , "vertex elements"
        #print "DEBUG , Border has" , len( self.borderVerts ) , "vertex elements"
        #print "DEBUG , Border has" , len( self.linDices ) , "segment endpoint indices"
        #print "DEBUG , Therea are" , self.numTri , "triangles"
        #print "DEBUG , Therea are" , len( self.F ) , "triangle vertex indices"
        
    def draw( self ):
        """ Render both sides of the flag as well as the border """
        # ~~ Implementation Template ~~
        # [1]. If OGL transforms enabled , Translate and rotate the OGL state machine to desired rendering frame
        self.state_transform()
        
        # [2]. Render
        # 2.A. Set  Side 1 Color
        glColor3ub( *self.colors[1] )
        # 2.B. Draw Side 1 Tris
        pyglet.graphics.draw_indexed( 
            self.numPts * 2 , # --------------------- Number of seqential triplet in vertex list
            GL_TRIANGLES , # -------------- Draw quadrilaterals
            self.F , # ---------- Indices where the coordinates are stored
            ( 'v3f' , self.vertX1 ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
        ) 
        # 2.C. Set  Side 2 Color
        glColor3ub( *self.colors[2] )
        # 2.D. Draw Side 2 Tris
        pyglet.graphics.draw_indexed( 
            self.numPts * 2 , # --------------------- Number of seqential triplet in vertex list
            GL_TRIANGLES , # -------------- Draw quadrilaterals
            self.F , # ---------- Indices where the coordinates are stored
            ( 'v3f' , self.vertX2 ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
        ) 
        # 2.E. Set  Border Color
        glColor3ub( *self.colors[0] )
        # 2.F. Draw Border Tris
        pyglet.gl.glLineWidth( 6 )
        # [3]. Render! 
        pyglet.graphics.draw_indexed( 
            self.numPts * 2, # --------------------- Number of seqential triplet in vertex list
            GL_LINES , # -------------- Draw lines
            self.linDices , # ---------- Indices where the coordinates are stored
            ( 'v3f' , self.borderVerts ) # vertex list , OpenGL offers an optimized vertex list object , but this is not it
        )        
        # [4]. If OGL transforms enabled , Return the OGL state machine to previous rendering frame
        self.state_untransform()

# __ End WavyFlag __

def linspace_endpoints( bgnPnt , endPnt , numPnts ):
    """ Create a list of 'numPnts' points between 'bgnPnt' and 'endPnt' , inclusive """
    # NOTE: This function assumes that 'bgnPnt' and 'endPnt' have the same dimensionality
    # NOTE: This is a re-implementation of 'Vector.vec_linspace' , but without np.ndarray
    coordsList = []
    rtnList = []
    for i in xrange( len( bgnPnt ) ):
        coordsList.append( np.linspace( bgnPnt[i] , endPnt[i] , numPnts ) )
    for i in xrange( numPnts ):
        temp = []
        for j in xrange( len( bgnPnt ) ):
            temp.append( coordsList[j][i] )
        rtnList.append( temp )
    return rtnList
    
def wave_in_plane_cos( pnt1 , pnt2 , transVec , numPts , period , t ):
    """ Return a list of points that define a cosine wave from 'pnt1' to 'pnt2' with transverse in 'transVec' and 'period' at time 't' """
    # NOTE: 'transVec' defines both the direction and magnitude of the transverse wave 
    baseLin   = linspace_endpoints( pnt1 , pnt2 , numPts )
    tTotal    = vec_mag( np.subtract( pnt1 , pnt2 ) )
    timeStep  = tTotal * 1.0 / ( numPts - 1 )
    amplitude = vec_mag( transVec )
    transDir  = vec_unit( transVec )
    rtnPnts = []
    for i in xrange( numPts ):
        y = amplitude * cos( ( t + i * timeStep ) / period * 2 * pi )
        rtnPnts.append( np.add( baseLin[i] , np.multiply( transDir , y ) ) )
    return rtnPnts

# === Main =================================================================================================================================

# == Program Vars ==

# ~ FLAGS ~
_SAVEGRAPHICS = True # Set to True to create an animated GIF of the generated graphics
#                       Be patient for the save process to finish after graphics window exit 'X' is clicked

# ~ Generation Settings ~
scale       = 0.65
camOrbit    = CircleOrbit( [ 0 , 0 , 0 ] , 1.5 * scale , 1 * scale ) # Camera will circle the given point in the X-Y plane at the given radius
dTheta      = pi / 90.0 # ------------------- Radians to advance per frame
totalFrames = 2 * int( ( 2 * pi ) / dTheta ) # ----- Number of frames that will bring the animation to its initial configuration ( GIF loop )

# ~ File Settings & Setup ~
prefix      = "frame_" # - Prefix for source frames
postfix     = ".png" # --- File extension for source frames ( pyglet can only save as PNG without PILLOW )
frmCount    = 0 # -------- Counting var to keep track of frames
subDirName  = "output" # - Subdir for all output files
ensure_dir( subDirName ) # Ensure that the output directory exists

# ~ Animation Settings ~
FPS         = 30 # -------------- Frame Per Second
outFileName = "billowFlaggins.gif" # Name of the output file

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

    # 1. Create the flag
    topPts = linspace_endpoints( [ -0.5 ,  0.0 ,  0.5 ] ,  [ 0.5 ,  0.0 ,  0.5 ] , numPts )
    btmPts = linspace_endpoints( [ -0.5 ,  0.0 , -0.5 ] ,  [ 0.5 ,  0.0 , -0.5 ] , numPts )
    flag = WavyFlag( topPts , btmPts , sepDist = 0.025 )
    flag.set_colors( [ 255 , 255 , 255 ] , # Border
                     [ 249 ,  93 ,  84 ] , # Side 1 , Lt Red
                     [  89 , 152 , 255 ] ) # Side 2 , Lt Blu

    # 2. Create an OGL window
    window = OGL_App( [ flag ] , caption = "BILLOW FLAGGINS" , 
                      clearColor = [ 0 , 0 , 0 , 1 ] ) # BG color black

    # 3. Set the camera to look at the collection
    window.set_camera( [ 2 , 2 , 2 ] , [ 0 , 0 , 0 ] , [ 0 , 0 , 1 ] )

    

    # 4. Draw & Display
    while not window.has_exit:
        
        t += dTheta
        
        flag.calc_render_geo( wave_in_plane_cos( [ -0.5 ,  0.0 ,  0.5 ] ,  [ 0.5 ,  0.0 ,  0.5 ] , [ 0 , 0.125 , 0 ] , numPts , 2/3 , t ) , 
                              wave_in_plane_cos( [ -0.5 ,  0.0 , -0.5 ] ,  [ 0.5 ,  0.0 , -0.5 ] , [ 0 , 0.125 , 0 ] , numPts , 2/3 , t ) )
        
        theta += dTheta
        window.set_camera( camOrbit( theta ) , [ 0 , 0 , 0 ] , [ 0 , 0 , 1 ] )
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
