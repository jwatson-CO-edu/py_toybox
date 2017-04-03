#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division

"""
mouselook is broken , fix it!
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

def get_yaw_pitch_from_vec( lookDir ):
    """ Get the yaw / pitch that will point the camera at 'lookPoint' in the world frame """
    # relVec = np.subtract( lookPoint , self.position ) # Get the direction of the point relative to the camera origin
    # YAW about the world Y axis
    [ rad , lookPitch , lookYaw ] = cart_2_radPtcYaw_YUP( lookDir )
    print "YAW:  " , lookYaw
    print "PITCH:" , lookPitch
    return lookYaw , lookPitch

def set_orientation_from_yaw_pitch( modPose , yaw , pitch ):
    """ Set the orientation of 'modPose' so that its gaze direction matches the given 'yaw' and 'pitch' """
    modPose.orientation = Quaternion.serial_rots( 
        Quaternion.k_rot_to_Quat( [ 1 , 0 , 0 ] , -pitch  ) , # Apply PITCH
        Quaternion.k_rot_to_Quat( [ 0 , 1 , 0 ] , yaw  ) , # Apply YAW
        # Quaternion.k_rot_to_Quat( [ 0 , 0 , 1 ] , pitch  )   # Apply PITCH
    )     
    
def gaze_vectors( camPose , originalGaze , originalUp ):
    """ , Return the vectors that determine the view in OpenGL """
    return camPose.orientation.apply_to( originalGaze ) , camPose.orientation.apply_to( originalUp )

if __name__ == "__main__":
    
    # def __init__( self , position , focus , upPnt , winWdth , winHght ):
    # def __init__( self , position , gazeDir , upDir , winWdth , winHght ):
    position = [ 24 , 20 , 20 ] 
    print "position:" , position
    gazeDir =  [   4.02 ,  4.25 , -400 ] 
    print "gazeDir: " , gazeDir
    upDir =    [  0 , 10 ,  0 ]
    print "upDir:   " , upDir
    """ Create a camera object at a 'position' , looking at a 'focus' point , with 'upPnt' in the vertical plane that includes the camera """
    # gazeDir = vec_dif_unt( focus , position ) # Unit vector for the direction the camera is looking
    # upDir = vec_dif_unt( upPnt , position ) # Assume a point in the vertical plane was specified , otherwise camera will be conked
    yBasis = np.cross( upDir , gazeDir )
    print "yBasis:  " , yBasis
    zBasis = np.cross( gazeDir , yBasis ) # Don't assume that the up point forms a proper basis
    print "zBasis:  " , zBasis
    camPose = Pose( position , Quaternion.principal_rot_Quat( gazeDir , yBasis , zBasis ) )
    print "Camera:  " , camPose
    [ yaw , pitch ] = get_yaw_pitch_from_vec( gazeDir )
    set_orientation_from_yaw_pitch( camPose , yaw , pitch )
    [ gaze , up ] = gaze_vectors( camPose , [ 0 , 0 , vec_mag( gazeDir ) ] , upDir )
    print "gazeDir: " , gaze # 2017-03-24: Succesfully recovered gaze direction!
    print "upDir:   " , up