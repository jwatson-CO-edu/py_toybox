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
                               'F:\Python\ResearchEnv',
                               '/media/mawglin/FILEPILE/Python/ResearchEnv'] )
from ResearchEnv import * # Load the custom environment
from ResearchUtils.Vector import *
from ResearchUtils.Plotting import *
from robotAnim import *

# == End Init ==========================================================================================================

#def sum_vector_chain(vecList):
#    ptsList = [ vecList[0] ]
#    for i in range(1,len(vecList)):
#        ptsList.append( np.add( vecList[-1] , vecList[i] ) )
#    return ptsList

def KUKA_chain_from_jnt_angles( Theta1 = 0 , Theta2 = 0 , Theta3 = 0 , Theta4 = 0 , Theta5 = 0 , Theta6 = 0): # TODO: ITERATIVE TROUBLESHOOTING

    # Home position is not the same as the zero-angle position
    
    if Theta1 > 170 or Theta1 < -170:
        raise RuntimeWarning("Theta 1 was out of bounds! " + str(Theta1))
    if Theta2 >  45 or Theta2 < -190:
        raise RuntimeWarning("Theta 2 was out of bounds! " + str(Theta2)) # TODO: ITERATIVE TROUBLESHOOTING
    if Theta3 > 156 or Theta3 < -120:
        raise RuntimeWarning("Theta 3 was out of bounds! " + str(Theta3))
    if Theta4 > 185 or Theta4 < -185:
        raise RuntimeWarning("Theta 4 was out of bounds! " + str(Theta4))
    if Theta5 > 120 or Theta5 < -120:
        raise RuntimeWarning("Theta 5 was out of bounds! " + str(Theta5))
    if Theta6 > 350 or Theta5 < -350:
        raise RuntimeWarning("Theta 6 was out of bounds! " + str(Theta6))
    
    Theta1 = radians( Theta1 )
    Theta2 = radians( Theta2 ) # TODO: ITERATIVE TROUBLESHOOTING
    Theta3 = radians( Theta3 )
    Theta4 = radians( Theta4 )
    Theta5 = radians( Theta5 )
    Theta6 = radians( Theta6 )
    
    # ~ Link 1 ~ # OK
    
    # ~ Link 2 ~
    Alpha1 = pi/2
                      
    # ~ Link 3 ~
  
    # ~ Link 4 ~
    Alpha3 = pi/2

    # ~ Link 5 ~
    Alpha4 = -pi/2

    # ~ Link 6 ~
    Alpha5 = pi/2

    
    startpoint = [0,0,0] # This is where the robot will be planted in the world frame
    #endpoint = startpoint + d_01 + d_12 + d_23 + d_34 + d_45 + d_56
    
    # Link 6
    a = Quaternion.k_rot_to_Quat( [0,0,1], Theta6)
    b = Quaternion.k_rot_to_Quat([1,0,0], Alpha5)
    # Link 5
    c = Quaternion.k_rot_to_Quat( [0,0,1], Theta5)
    d = Quaternion.k_rot_to_Quat([1,0,0], Alpha4)
    # Link 4
    e = Quaternion.k_rot_to_Quat( [0,0,1], Theta4)
    f = Quaternion.k_rot_to_Quat([1,0,0], Alpha3) 
    # Link 3
    g = Quaternion.k_rot_to_Quat( [0,0,1], Theta3)
    # Link 2
    h = Quaternion.k_rot_to_Quat([0,0,1], Theta2) # TODO: ITERATIVE TROUBLESHOOTING
    i = Quaternion.k_rot_to_Quat([1,0,0], Alpha1) 
    # Link 1
    j = Quaternion.k_rot_to_Quat([0,0,1], Theta1)
    
    Q06 = Quaternion.serial_rots( a , b , c , d , e , f , g , h , i , j )
   #Q05 =         Quaternion.serial_rots( c , d , e , f , g , h , i , j ) # No link to rotate, joints are coincident
    Q04 =                 Quaternion.serial_rots( e , f , g , h , i , j )
    Q03 =                         Quaternion.serial_rots( g , h , i , j )
    Q02 =                             Quaternion.serial_rots( h , i , j ) # TODO: ITERATIVE TROUBLESHOOTING
    Q01 =                                                             j

    d_01 =  Q01.apply_to( np.add( [0,0,400] , [-25,0,0] ) )
    d_12 = Q02.apply_to( [-455,0,0] ) # TODO: ITERATIVE TROUBLESHOOTING
    d_23 = Q03.apply_to( [-35,0,0] )
    d_34 = Q04.apply_to( [0,0,420] )
    d_45 = [0,0,0]
    d_56 = Q06.apply_to( [0,0,80] )
    
    
    #print endpoint
    #print startpoint , d_01 , d_12 , d_23 , d_34 , d_45 , d_56
    return vec_sum_chain( [ startpoint , d_01 , d_12 , d_23 , d_34 , d_45 , d_56 ] ) # TODO: ITERATIVE TROUBLESHOOTING

    
linkPoints = KUKA_chain_from_jnt_angles(0,0,0,0,0,0) # TODO: ITERATIVE TROUBLESHOOTING
print linkPoints
print bound_box_3D( linkPoints )

foo = SegmentApp()

armSegments = []
for index in range(1,len(linkPoints)):
    armSegments.append( Segment(linkPoints[index - 1] , linkPoints[index] , foo.canvas , 'white' ) )
    
foo.dynamicSegments = armSegments

def link_update_from_chain(linkPoints, segmentList):
    #print linkPoints
    print "Sim side:", segmentList[0].bgn, segmentList[0].end
    for index in range(1,len(linkPoints)):
        segmentList[index - 1].set_pnts( linkPoints[index - 1] , linkPoints[index] )
        segmentList[index - 1].update()
        
def segment_update(angleList):
    link_update_from_chain(KUKA_chain_from_jnt_angles(*angleList), armSegments)
    
foo.calcFunc = segment_update
    
foo.run()