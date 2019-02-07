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

# ___ END GEO ______________________________________________________________________________________________________________________________


# === ARCHITECTURE =========================================================================================================================

# URL , L-System: https://en.wikipedia.org/wiki/L-system
# 2019-02-06: For now, create a node-centric system with the hallways serving the rooms, rather than a true L-system

# == Room Generation ==
# NOTE: Rooms are specified from an indoor-centric view 
# NOTE: Hall origin is always at the bottom center

# FIXME: WALLS WILL NOT WORK FOR CIRCULAR / SPHERICAL ROOMS , USE { VOLUMES , CONNECTION POINTS , DOOR VECTORS }

_MCPI_BASICHALL = solid_cuboid( [ [ -1 , -1 , 0 ] , [  1 ,  1 , 2 ] ] )

def make_wall_cub( brct , outVec , hasDoor , drgn , hallProf ):
    """ Structure and Return a cuboid wall """
    
    # 1. Check that the wall lies on a principal plane
    # 2. Return wall specification
    return {
        "boundRect"   : brct ,
        "outwardVec"  : outVec ,
        "hasDoor"     : hasDoor , 
        "doOrigin"    : drgn , 
        "hallProfile" : doorProf 
    }

def make_room_cub( structure , origin , orgn , sizeXYZ ):
    """ Structure , Generate , and Return a cuboid room """
    # NOTE: Room origin is always at the bottom center
    
    # FIXME : CUBOID SPECIFICATION
    # 1. Size
    # 2. Bounding box ( Inside )
    # 3. Walls
        # A. Bounding Rectangle
        # B. Outward Vector
        # C. Doors
            # a. Location
            # b. Profile

# __ End Room Gen __



class MCPi_Room( Node ):
    """ Structure room as a graph node """
    
    def __init__( self , orgn , wallThic = 1 , rmTyp = "CUBOID" ):
        """ Create a room with generation rules """
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

# ___ End Tests ____________________________________________________________________________________________________________________________