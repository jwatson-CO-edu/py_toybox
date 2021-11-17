#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2018-03-23

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
mineCraftCraft.py
James Watson, 2019 February
Utilities for working with Minecraft Pi Edition
"""

# ~~~ Imports ~~~
# ~~ Standard ~~
import os
from math import pi , sqrt
# ~~ Special ~~
import numpy as np
# ~~ Local ~~
from marchhare.Graph import Node , Graph

# ~~ Constants , Shortcuts , Aliases ~~
EPSILON = 1e-7
infty   = 1e309 # URL: http://stackoverflow.com/questions/1628026/python-infinity-any-caveats#comment31860436_1628026
endl    = os.linesep


# === GEOMETRY =============================================================================================================================

def solid_cuboid( bbox ):
    """ Return a list of voxels that constitute a cuboid , including the corners """
    # NOTE: This function assumes that the second corner of 'bbox' is larger in all dimensions than the first corner
    rtnVox = []
    X = range( bbox[0][0] , bbox[1][0] + 1 )
    Y = range( bbox[0][1] , bbox[1][1] + 1 )
    Z = range( bbox[0][2] , bbox[1][2] + 1 )
    for z_i in Z:
        for x_i in X:
            for y_i in Y:
                rtnVox.append( [ x_i , y_i , z_i ] )
    return rtnVox

def bounds_from_cntr_wdth( cenInt , wdtInt ):
    """ Given a center and a width, give the bounds """
    # NOTE: When the width is even, there will be one more block on the lower side than the higher side
    hlfWdt = wdtInt // 2
    lowBnd = cenInt - hlfWdt
    hghBnd = lowBnd + wdtInt - 1
    return [ lowBnd , hghBnd ]

# ___ END GEO ______________________________________________________________________________________________________________________________


# === ARCHITECTURE =========================================================================================================================

# URL , L-System: https://en.wikipedia.org/wiki/L-system
# 2019-02-06: For now, create a node-centric system with the hallways serving the rooms, rather than a true L-system

# == Room Generation ==
# NOTE: Rooms are specified from an indoor-centric view 
# NOTE: Hall origin is always at the bottom center

# FIXME: WALLS WILL NOT WORK FOR CIRCULAR / SPHERICAL ROOMS , USE { VOLUMES , CONNECTION POINTS , DOOR VECTORS }

_MCPI_BASICHALL = solid_cuboid( [ [ -1 , -1 , 0 ] , [  1 ,  1 , 2 ] ] )
_MCPI_CUBOIDDIR = [ 'N' , 'S' , 'E' , 'W' , 'U' , 'D' ]

def cuboid_doors( doorSpec ):
    """ Produce a door description from the specification """
    # 1. For each of { N , S , E , W , U , D }
        # 2. Check if the label exists
        # 3. FIXME : DESCRIBE DOOR GENERATION

def make_room_cub( structure , origin , orgn , sizeXYZ , doorSpec ):
    """ Structure , Generate , and Return a cuboid room """
    # NOTE: Room origin is always at the bottom center
    
    # 1. Internal blocks - Rooms are defined by their internal blocks, walls are applied around this region
    xBounds = bounds_from_cntr_wdth( origin[0] , sizeXYZ[0] )
    yBounds = bounds_from_cntr_wdth( origin[1] , sizeXYZ[1] )
    zBounds = [ origin[2] , origin[2] + sizeXYZ[2] - 1 ]
    # A. Bounding box ( Inside )
    bbox    = [ [ min( xBounds ) , min( yBounds ) , min( zBounds ) ] ,
                [ max( xBounds ) , max( yBounds ) , max( zBounds ) ] ]
    internalSpace = solid_cuboid( bbox )
    # 3. Doors
        # A. Location
        # B. Outward Vector
        # C. Profile

# __ End Room Gen __



class MCPi_Room( Node ):
    """ Structure room as a graph node """
    
    def __init__( self , strctr , orgn , wallThic = 1 , rmTyp = "CUBOID" ):
        """ Create a room with generation rules """
        self.structure     = strctr # - Structure that this room belongs to
        self.origin        = orgn # --- Origin voxel of the room
        self.wallThickness = wallThic # Wall thickness
        self.roomType      = rmTyp # -- Room Type
        self.roomSpec      = None # --- Room specification

class MCPi_Structure( Graph ):
    """ A build represented as a growing L-system """
    
    def __init__( self , wallThic = 1 ):
        """ Create a building L-System """
        super( MCPi_Structure , self ).__init__()
        self.wallThickness = wallThic

# ___ END ARCH _____________________________________________________________________________________________________________________________


# === Testing ==============================================================================================================================

if __name__ == "__main__":
    print _MCPI_BASICHALL
    print len( _MCPI_BASICHALL )
    print bounds_from_cntr_wdth( 0 , 3 )
    print bounds_from_cntr_wdth( 0 , 2 )

# ___ End Tests ____________________________________________________________________________________________________________________________