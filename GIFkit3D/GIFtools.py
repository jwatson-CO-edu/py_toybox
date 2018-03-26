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

# == class CircleOrbit ==

class CircleOrbit:
    """ Return the Pyglet camera matrix for a camera that orbits a point while focusing on the point """
    
    def __init__( self , center , radius ):
        """ Set all the params for a circular orbit """
        self.center    = center
        self.radius    = radius

    def __call__( self , theta ):
        """ Return the point in R3 for angle 'theta' """
        offset = np.dot( z_rot( theta ) , [ self.radius , 0 , 0 ] )
        # print "Offset:" , offset
        return np.add( self.center , offset )
    
# __ class CircleOrbit __

