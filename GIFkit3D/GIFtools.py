#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-09-05

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
GIFtools.py
James Watson, 2018 March
Tools and utilities for generative art with Pyglet
"""

# ~~ Imports ~~
# ~ Standard ~
# ~ Special ~
import numpy as np
# ~ Local ~
from marchhare.VectorMath.SpatialVectorRobot import z_rot
from marchhare.OGLshapes import Vector_OGL , OGL_App , Icosahedron_Reg , OGLDrawable

# === Functions ============================================================================================================================

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

# ___ End Functions ________________________________________________________________________________________________________________________


# === Classes ==============================================================================================================================

# == class CircleOrbit ==

class CircleOrbit:
    """ Return the Pyglet camera matrix for a camera that orbits a point while focusing on the point """
    
    def __init__( self , center , radius , zHeight = 0.0 ):
        """ Set all the params for a circular orbit """
        self.center    = center
        self.radius    = radius
        self.height    = zHeight

    def __call__( self , theta ):
        """ Return the point in R3 for angle 'theta' """
        offset = np.dot( z_rot( theta ) , [ self.radius , 0 , self.height ] )
        # print "Offset:" , offset
        return np.add( self.center , offset )
    
# __ End CircleOrbit __


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

# ___ End Classes __________________________________________________________________________________________________________________________


# ~~~ Spare Parts ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#def double_all_middle_vertices( inList , cadence = 3 ):
    #""" Double all elements of a vertex list except the first and last """
    ## NOTE: This is only necessary for the indices, not the vertices themselves
    #coordList = build_sublists_by_cadence( inList , cadence )
    #rtnList = []
    #lastDex = len( coordList ) - 1 
    #for i , elem in enumerate( coordList ):
        #if i == 0 or i == lastDex:
            #rtnList.append( elem )
        #else:
            #rtnList.extend( [ elem , elem ] )
    #return flatten_nested_sequence( rtnList )