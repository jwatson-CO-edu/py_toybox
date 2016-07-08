#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-06-25

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
Kinematics_Serial-Manip.py , Built on Spyder for Python 2.7
James Watson, 2016 July
Simulating kinematics of a serial manipulator
"""
# == Init Environment ==================================================================================================
import sys, os.path
SOURCEDIR = os.path.dirname(os.path.abspath(__file__)) # URL, dir containing source file: http://stackoverflow.com/a/7783326

def add_first_valid_dir_to_path(dirList):
    """ Add the first valid directory in 'dirList' to the system path """
    # In lieu of actually installing the library, just keep a list of all the places it could be in each environment
    loadedOne = False
    for drctry in dirList:
        if os.path.exists( drctry ):
            sys.path.append( drctry )
            print 'Loaded', str(drctry)
            loadedOne = True
            break
    if not loadedOne:
        print "None of the specified directories were loaded"
# List all the places where the research environment could be
add_first_valid_dir_to_path( [ '/media/jwatson/FILEPILE/Python/ResearchEnv',
                               '/home/jwatson/regrasp_planning/researchenv',
                               'F:\Python\ResearchEnv' ] )
from ResearchEnv import * # Load the custom environment
from ResearchUtils.Vector import *
from ResearchUtils.Plotting import *
#import matplotlib as mpl

# == End Init ==========================================================================================================

# ~ Control ~
Theta1 = -90
Theta2 = 40
Theta3 = 0
Theta4 = 0
Theta5 = 0
Theta6 = 0

# Corrections for home position
Theta2 += -90

if Theta1 > 170 or Theta1 < -170:
    raise RuntimeWarning("Theta 1 was out of bounds!")
if Theta2 >  45 or Theta2 < -190:
    raise RuntimeWarning("Theta 2 was out of bounds!")
if Theta3 > 156 or Theta3 < -120:
    raise RuntimeWarning("Theta 3 was out of bounds!")
if Theta4 > 185 or Theta4 < -185:
    raise RuntimeWarning("Theta 4 was out of bounds!")
if Theta5 > 120 or Theta5 < -120:
    raise RuntimeWarning("Theta 5 was out of bounds!")
if Theta5 > 350 or Theta5 < -350:
    raise RuntimeWarning("Theta 6 was out of bounds!")

Theta1 = radians( Theta1 )
Theta2 = radians( Theta2 )
Theta3 = radians( Theta3 )
Theta4 = radians( Theta4 )
Theta5 = radians( Theta5 )
Theta5 = radians( Theta6 )

# ~ Link 1 ~
Q01  = Quaternion.k_rot_to_Quat([0,0,1], Theta1)
d_01 = [0,0,400] + Q01.apply_to( [-25,0,0] )

# ~ Link 2 ~
Alpha1 = pi/2
Q02 = Quaternion.serial_rots( Quaternion.k_rot_to_Quat([0,0,1], Theta2) , 
                        Quaternion.k_rot_to_Quat([1,0,0], Alpha1), \
                        Q01 )
d_12 = Q02.apply_to( [-455,0,0] )
                    
# ~ Link 3 ~
Q03 = Quaternion.serial_rots( Quaternion.k_rot_to_Quat( [0,0,1], Theta3),
                        Q02 )
d_23 = Q03.apply_to( [-35,0,0] )

# ~ Link 4 ~
Alpha3 = pi/2
Q04 = Quaternion.serial_rots( Quaternion.k_rot_to_Quat( [0,0,1], Theta4), 
                        Quaternion.k_rot_to_Quat([1,0,0], Alpha3), \
                        Q03 )
d_34 = Q04.apply_to( [0,0,420] )

# ~ Link 5 ~
Alpha4 = -pi/2
Q05 = Quaternion.serial_rots( Quaternion.k_rot_to_Quat( [0,0,1], Theta5), 
                        Quaternion.k_rot_to_Quat([1,0,0], Alpha4), \
                        Q04 )
d_45 = [0,0,0]

# ~ Link 6 ~
Alpha5 = pi/2
Q06 = Quaternion.serial_rots( Quaternion.k_rot_to_Quat( [0,0,1], Theta6), 
                        Quaternion.k_rot_to_Quat([1,0,0], Alpha5), \
                        Q05 )
d_56 = Q06.apply_to( [0,0,80] )

endpoint = d_01 + d_12 + d_23 + d_34 + d_45 + d_56

print endpoint

plot_chain( [ [0,0,0] , d_01 , d_12 , d_23 , d_34 , d_45 , d_56 ] )