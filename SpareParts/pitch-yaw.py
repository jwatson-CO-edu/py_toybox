#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division

"""
spherical-coordinates
James Watson , 2017 March
Convert Cartesian to spherical and back , also with Y as up for graphics folks
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
             '/media/mawglin/FILEPILE/Utah_Research/Assembly_Planner/AsmEnv' ,
             '/media/jwatson/FILEPILE/Utah_Research/Assembly_Planner/AsmEnv' ]
add_first_valid_dir_to_path( envPaths )
add_first_valid_dir_to_path( [ os.path.join( path , 'VectorMath' ) for path in envPaths ] )

# ~~ Imports ~~
# ~ Standard ~
from random import randint
from math import atan2 , acos
# ~ Special ~
# import numpy as np
# ~ Local ~
from AsmEnv import sep
from Vector import *
from Vector3D import *

# == END INIT ==============================================================================================================================

# == Mouselook Angles ==

def cart_2_radPtcYaw( cartCoords ):
    """ Convert a Cartesian vector to [ radius , pitch , yaw ] for the purpose of mouselook """
    r , theta , phi = cart_2_sphr( cartCoords )
    return [ r , piHalf - phi , theta ]

def radPtcYaw_2_cart( radPtcYaw ):
    """ Convert [ radius , pitch , yaw ] vector to a Cartesian vector [ x , y , z ] for the purpose of mouselook """
    return sphr_2_cart( [ radPtcYaw[0] , radPtcYaw[2] , piHalf - radPtcYaw[1] ] ) # [ r , \theta , \phi ] --> [ x , y , z ]

def cart_2_radPtcYaw_YUP( cartCoords ):
    """ Convert a Cartesian vector to [ radius , pitch , yaw ] for the purpose of mouselook , Y+ = UP """
    r , theta , phi = cart_2_sphr_YUP( cartCoords )
    return [ r , piHalf - phi , theta ]

def radPtcYaw_2_cart_YUP( radPtcYaw ):
    """ Convert [ radius , pitch , yaw ] vector to a Cartesian vector [ x , y , z ] for the purpose of mouselook , Y+ = UP """
    return sphr_2_cart_YUP( [ radPtcYaw[0] , radPtcYaw[2] , piHalf - radPtcYaw[1] ] ) # [ r , \theta , \phi ] --> [ x , y , z ]

# == End Mouselook ==

if __name__ == "__main__":
     # Convert cart to sphr and recover to cart
    sep( "Regular Spherical" )
    cart1 = [ 10 , -10 , 10 ]
    print "Started with Cartesian:" , cart1
    sphrC = cart_2_sphr( cart1 )
    print "Got spherical coords:  " , sphrC
    cart2 = sphr_2_cart( sphrC )
    print "Recovered Cartesian:   " , cart2
    print "Error after conversion:" , vec_dif_mag( cart1 , cart2 ) # 1.7763568394e-15, Nice!
    sep( "Y+ is UP" )
    cart1 = [ 10 , -10 , 10 ]
    print "Started with Cartesian:" , cart1
    sphrC = cart_2_sphr_YUP( cart1 )
    print "Got spherical coords:  " , sphrC
    cart2 = sphr_2_cart_YUP( sphrC )
    print "Recovered Cartesian:   " , cart2
    print "Error after conversion:" , vec_dif_mag( cart1 , cart2 ) # 1.7763568394e-15, Nice!
    print 
    
    sep( "Regular Rad-Pitch-Yaw" )
    cart1 = [ 10 , -10 , 10 ]
    print "Started with Cartesian:" , cart1
    radPtchYaw = cart_2_radPtcYaw( cart1 )
    print "Got radPtchYaw coords:  " , radPtchYaw
    cart2 = radPtcYaw_2_cart( radPtchYaw )
    print "Recovered Cartesian:   " , cart2
    print "Error after conversion:" , vec_dif_mag( cart1 , cart2 ) # 1.7763568394e-15, Nice!
    sep( "Y+ is UP" )
    cart1 = [ 10 , -10 , 10 ]
    print "Started with Cartesian:" , cart1
    radPtchYaw = cart_2_radPtcYaw_YUP( cart1 )
    print "Got radPtchYaw coords:  " , radPtchYaw
    cart2 = radPtcYaw_2_cart_YUP( radPtchYaw )
    print "Recovered Cartesian:   " , cart2
    print "Error after conversion:" , vec_dif_mag( cart1 , cart2 ) # 1.7763568394e-15, Nice!    