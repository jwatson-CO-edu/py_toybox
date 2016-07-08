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
add_first_valid_dir_to_path( [ '/home/jwatson/regrasp_planning/researchenv',
                               '/media/jwatson/FILEPILE/Python/ResearchEnv',
                               'F:\Python\ResearchEnv' ] )
from ResearchEnv import * # Load the custom environment
from ResearchUtils.Vector import * # TODO: Make sure that my local repo is up to date

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
Q01  = Quaternion.k_rot_to_Quat(Vector([0,0,1]), Theta1)
d_01 = Vector([0,0,400]) + Q01.apply_to( Vector([-25,0,0]) )

# ~ Link 2 ~
Alpha1 = pi/2
Q02 = Quaternion.serial_rots( Quaternion.k_rot_to_Quat(Vector([0,0,1]), Theta2) , 
                        Quaternion.k_rot_to_Quat(Vector([1,0,0]), Alpha1), \
                        Q01 )
d_12 = Q02.apply_to( Vector([-455,0,0]) )
                    
# ~ Link 3 ~
Q03 = Quaternion.serial_rots( Quaternion.k_rot_to_Quat( Vector([0,0,1]), Theta3),
                        Q02 )
d_23 = Q03.apply_to( Vector([-35,0,0]) )

# ~ Link 4 ~
Alpha3 = pi/2
Q04 = Quaternion.serial_rots( Quaternion.k_rot_to_Quat( Vector([0,0,1]), Theta4), 
                        Quaternion.k_rot_to_Quat(Vector([1,0,0]), Alpha3), \
                        Q03 )
d_34 = Q04.apply_to( Vector([0,0,420]) )

# ~ Link 5 ~
Alpha4 = -pi/2
Q05 = Quaternion.serial_rots( Quaternion.k_rot_to_Quat( Vector([0,0,1]), Theta5), 
                        Quaternion.k_rot_to_Quat(Vector([1,0,0]), Alpha4), \
                        Q04 )
d_45 = Vector([0,0,0])

# ~ Link 6 ~
Alpha5 = pi/2
Q06 = Quaternion.serial_rots( Quaternion.k_rot_to_Quat( Vector([0,0,1]), Theta6), 
                        Quaternion.k_rot_to_Quat(Vector([1,0,0]), Alpha5), \
                        Q05 )
d_56 = Q06.apply_to( Vector([0,0,80]) )

endpoint = d_01 + d_12 + d_23 + d_34 + d_45 + d_56

print endpoint

X = []
Y = []
Z = []

def pack_vectors_for_plotting(*args):
    global X,Y,Z
    endPoint = Vector([0,0,0])
    for vec in args:
        endPoint = endPoint + vec
        X.append( endPoint[0] )
        Y.append( endPoint[1] )
        Z.append( endPoint[2] )
        
pack_vectors_for_plotting( Vector([0,0,0]) , d_01 , d_12 , d_23 , d_34 , d_45 , d_56 )

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure(figsize=(9, 9), dpi=100)
ax = fig.gca(projection='3d')
#theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
ax.plot( X , Y , Z )
ax.set_xlim(-1000, 1000)
ax.set_ylim(-1000, 1000)
ax.set_zlim(0, 1000)
ax.legend()

plt.show()
                
# == Abandoned Code ==
                
#foo = Quat.k_rot_to_Quat(Vector([1,1,1]), 0)
#bar = Quat.k_rot_to_Quat(Vector([0,1,0]), pi/2)

#print str( Quat.compose_rots(foo, bar) )                
                
# == OLD ==

#foo = Quat.k_rot_to_Quat(Vector([0,1,0]), 0)
#print foo.apply_to( Vector([1,0,0]) )

#q1 = Quat.k_rot_to_Quat(Vector([0,0,0]), 0)
#q2 = Quat.k_rot_to_Quat(Vector([0,1,0]), pi/2)
#
##print Quat.compose_rots(q2, q2)
#
#Theta1 = 0
#Theta2 = 0
#Theta3 = pi/2
#Theta4 = 0
#
## corrections for home position
##Theta2 += radians(-90)
#
## warnings
#if Theta1 > radians(170) or Theta1 < radians(-170):
#    raise RuntimeWarning("Theta 1 was out of bounds!")
#if Theta2 > radians(45) or Theta2 < radians(-190):
#    raise RuntimeWarning("Theta 2 was out of bounds!")
#if Theta3 > radians(156) or Theta3 < radians(-120):
#    raise RuntimeWarning("Theta 3 was out of bounds!")
#if Theta4 > radians(185) or Theta4 < radians(-185):
#    raise RuntimeWarning("Theta 4 was out of bounds!")
#    
#k4 = Vector([0,0,1])
#Link4 = [ Vector([0,0,420]) ]
#Quat4 = Quat.k_rot_to_Quat(k4, Theta4)
#d_34 = Vector([0,0,0])
#for param in Link4:
#    d_34 = d_34 + Quat4.apply_to(param)
#    
#Alpha3 = pi/2
#d_34 = Quat.k_rot_to_Quat(Vector([1,0,0]),Alpha3).apply_to(d_34)
#    
#k3 = Vector([0,0,1])
#Link3 = [ Vector([0,-35,0]) ]
#Quat3 = Quat.k_rot_to_Quat(k3, Theta3)
#d_23 = Vector([0,0,0])
#for param in Link3:
#    d_23 = d_23 + Quat3.apply_to(param)
#d_34 = Quat3.apply_to(d_34)
#    
#Theta_star2 = -pi/2
#d_23 = Quat.k_rot_to_Quat(Vector([0,0,1]),Theta_star2).apply_to(d_23)
#d_34 = Quat.k_rot_to_Quat(Vector([0,0,1]),Theta_star2).apply_to(d_34)
#
#k2 = Vector([0,0,1])
#Link2 = [ Vector([-455,0,0]) ]
#Quat2 = Quat.k_rot_to_Quat(k2, Theta2)
#d_12 = Vector([0,0,0])
#for param in Link2:
#    d_12 = d_12 + Quat2.apply_to(param)
#d_23 = Quat2.apply_to(d_23)
#d_34 = Quat2.apply_to(d_34)
##d_23 = Quat.k_rot_to_Quat(k2, Theta2 + radians(90)).apply_to(d_23)
##d_34 = Quat.k_rot_to_Quat(k2, Theta2 + radians(90)).apply_to(d_34)
#    
#Alpha1 = pi/2
#d_12 = Quat.k_rot_to_Quat(Vector([1,0,0]),Alpha1).apply_to(d_12)
#d_23 = Quat.k_rot_to_Quat(Vector([1,0,0]),Alpha1).apply_to(d_23)
#d_34 = Quat.k_rot_to_Quat(Vector([1,0,0]),Alpha1).apply_to(d_34)
#
#k1 = Vector([0,0,1])
#Link1 = [ Vector([0,0,400]) , Vector([-25,0,0]) ]
#Quat1 = Quat.k_rot_to_Quat(k1, Theta1)
#d_01 = Vector([0,0,0])
#for param in Link1:
#    d_01 = d_01 + Quat1.apply_to(param)
#d_12 = Quat1.apply_to(d_12)
#d_23 = Quat1.apply_to(d_23)
#d_34 = Quat1.apply_to(d_34)
#
#endpoint = d_01 + d_12 + d_23 + d_34
#
#print endpoint
                
# ~~ Build Robot ~~

#frame_three = Link([0,0,0])
##frame_three.d_param(0)
#frame_three.a_param(-35)
##frame_three.alpha_param(pi/2)
#
#frame_two = Link([0,0,0])
#frame_two.a_param(-455)
#frame_two.add_joint(  )
##frame_two.add_joint( distalLink = frame_three, minTheta = radians(-120) , maxTheta = radians(156), homeOffset = 0.0 )
#
#frame_one = Link([0,0,0])
#frame_one.d_param(400)
#frame_one.a_param(-25)
#frame_one.alpha_param(pi/2.0)
#frame_one.add_joint( distalLink = frame_two, minTheta = radians(-190), maxTheta = radians(45), homeOffset = radians(-90))
#
##print vars( Segment( Vector([0,0,0]), Vector([1,1,1]) ) )
#
#frame_zero = Link([0,0,0])
#frame_zero.add_joint( distalLink = frame_one , minTheta = radians(-170) , maxTheta = radians(170) )
#
## ~~ Set Angles ~~
#theta1 = pi/2
#theta2 = pi/4
#theta3 = 0
#
## FIXME : FIND OUT WHY I CAN ONLY CALL THESE IN REVERSE ORDER
##frame_two.set_joint_theta(   theta3 )
#frame_one.set_joint_theta(   theta2 )
#frame_zero.set_joint_theta(  theta1 )
#frame_zero.trans_calc_recur()
#
#print "Joint 1 set to {0} radians = {1} degrees".format( theta1 , degrees(theta1) )
#print "Joint 2 set to {0} radians = {1} degrees".format( theta2 , degrees(theta2) )
#print "Joint 3 set to {0} radians = {1} degrees".format( theta3 , degrees(theta3) )
#print frame_one.endpoint()        
#print frame_two.endpoint()  
#print frame_three.endpoint()
#
#def joint_spec(theta1, theta2): # FIXME : FIND OUT WHY THIS DOES NOT REACH THE JOINTS
#    """ Set all joint angles and report the endpoint """
#    global frame_zero, frame_one, frame_two
#    try:
#        frame_zero.set_joint_theta( theta1 )
#        print "Joint 1 set to {0} radians = {1} degrees".format( theta1 , degrees(theta1) )
#        frame_one.set_joint_theta(  theta2 )
#        print "Joint 2 set to {0} radians = {1} degrees".format( theta2 , degrees(theta2) )
#        print frame_one.endpoint()        
#        print frame_two.endpoint()
#    except RuntimeError:
#        print "Setting joints failed"
#        
##joint_spec(pi/4,0)
#
#
##foo = Quat.k_rot_to_Quat([1,0,0], pi/2)
##bar = Quat.k_rot_to_Quat([0,1,0], 5*pi/2)
##baz = Quat.compose_rots(foo, bar)
##print str(baz.apply_to(Vector([1,1,0])))
#
##foo = Geo3D([0,0,0], [[1,0,0],[0,1,0],[0,0,1]], [0,0,1])
##print str(foo)
###foo.rotate(pi/2)
##foo.orient([1,0,0],pi/2)
##print str(foo)
                
#class testClass(object):
#    def __init__(self, lst):
#        self.lst = lst[:] # store a COPY of param 'lst'
                
# == End Abandoned ==