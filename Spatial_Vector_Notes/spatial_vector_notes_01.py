#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division # MUST be run before all other expressions , including docstrings!

"""
spatial_vector_notes_01.py
James Watson , 2017 May , Written on Spyder 3 / Python 2.7
Beginning notes on Featherstone spatial vectors
"""

# == Init ==================================================================================================================================

from math import atan , sin , cos
import numpy as np
from utils import *

# == End Init ==============================================================================================================================

"""
A spatial vector combines the linear and angular aspects of rigid-body motion or force into a single quantity.


A vector field is itself a vector because it satisfies the formal definition of a vector. Addition of fields and multiplication by a scalar ar defined.


A vector field can describe the velocity of a rigid body.
* A body-fixed point is a point in a fixed location relative to a rigid body. When the body moves, the point moves with it.
  If we imaging the whole of space to be filled with body-fixed points, then the motion of the body defines a vector field.

* The set of vector fields that describe every possible velocity of a rigid body moving in 3D space forms a 6D vector space.
  The elements of this space are spatial velocity vectors.

Screw Theory ( is closely related to spatial vector algebra  )
* The most general movement of a rigid body is a screwing motion consisting of a translation along and a rotation about a particular line in space.
* The spatial vector field that describes this motion is helical about the instantaneous screw axis
* So, the body's velocity can now be described using two scalars and a direction
  - Linear Velocity Magnitude , Scalar
  - Angular Velocity Magnitude , Scalar
  - Instantaneous screw axis , Vector

Plucker Basis
* 3 translations along the principal directions
* 3 rotations about the same axes
* The Plucker basis e on F^6 is reciprocal to d on M^6

Plucker Coordinates
* A Plucker coordinate system is defined by the position and orientation of a single cartesian frame
* A Plucker coordinate system has 12 basis vectors, covering both M^6 and F^6 basis vectors

Spatial Vectors
* Inhabit two vector spaces: Motion and Force
  _ Velocity m = ( m_1 * d_1 ) + ... + ( m_6 * d_6 ) , m_i : component , d_i : basis vector
  _    Force f = ( f_1 * e_1 ) + ... + ( f_6 * e_6 ) , f_i : component , e_i : basis vector
* The scalar product between them defines work

* Velocity
  Define:
      O   : Fixed origin
      P   : Point on a rigid body
      v_p : linear velocity of the rigid body
      w   : Angular velocity of the body through its center of rotation P
      v_O : Linear velocity of a body-fixed point that corresponds with O at this instant
      OP  : Displacement vector between O and P
  v_O = v_p + cross( OP , w )
  The body can now be regarded as translating with a velocity of v_O while simultaneously rotating with an angular velocity of w about an 
  axis passing through O
  
* Define the following Plucker Basis on M^6:
    d_Ox : unit angular motion about Ox
    d_Oy : unit angular motion about Oy
    d_Oz : unit angular motion about Oz
    d_x  : unit linear motion in the x direction
    d_y  : unit linear motion in the y direction
    d_z  : unit linear motion in the z direction
    
* This expression provides a complete description of the velocity of the rigid body and is invariant with respect to the location in the 
  coordinate frame
  - This is not a suitable representation for a non-rigid body , as the displacement of each part of an object will depend on its position in
    the coordinate frame
    
* v = transpose( [ w , v_O ] ) = transpose( [ w_x , w_y , w_z , v_Ox , v_Oy , v_Oz ] )
    = ( w_x * d_Ox ) + ( w_y * d_Oy ) + ( w_z * d_Oz ) + ( v_Ox * d_x ) + ( v_Oy * d_y ) + ( v_Oz * d_z )
"""

print "=== Problem A1 ==="

def v_w_to_Plucker( v_p , w , P ):
    """ Transform a linear velocity 'v' through P and rotational velocity 'w' about a line through P into a Plucker representation """
    v_O = v_p + np.cross( P , w )
    return [ w[0] , w[1] , w[2] , v_O[0] , v_O[1] , v_O[2] ]

A = vec_unit( [ 0 , 1 , 3 ] )
P = [ 0 , 0 , 0 ]
zeroVec = np.zeros( 3 )
print "A1.a :" , v_w_to_Plucker( zeroVec , A , P ) # CORRECT!
print "A1.b :" , v_w_to_Plucker( A , zeroVec , P ) # CORRECT!
P = [ 1 , 2 , 0 ]
B = [ 0 , 0 , 1 ]
print "A1.c :" , v_w_to_Plucker( zeroVec , B , P ) # CORRECT!
print "A1.d :" , v_w_to_Plucker( np.multiply( B , 2 ) , zeroVec , P ) # CORRECT!
print "A1.e :" , v_w_to_Plucker( np.multiply( B , 2 ) , np.multiply( B , 2 ) , P ) # CORRECT!

if 0: # Set to 1 to check the numbers for parts a and b
    theta = atan( 3 / 1 )
    print "cos( theta ) =" , cos( theta )
    print "sin( theta ) =" , sin( theta )
    
""" 
=== Problem A1 ===

A1.a : Express D_Q in terms of D_O.
d_Qx = d_Ox - l * d_z
d_Qy = d_Oy
d_Qz = d_Oz + l * d_x
d_x  = d_x
d_y  = d_y
d_z  = d_z


A1.b : Express v_Q in terms of v_O.
v_Q = v_O - cross( OQ , w ) , OQ = transpose( [ 0 , l , 0 ] )
w_x  = w_x
w_y  = w_y
w_z  = w_z
v_Qx = v_Ox - l * w_z
v_Qy = v_Oy
v_Qz = v_Oz + l * w_x

A1.c : Show that the expression 
       ( w_x * d_Ox ) + ( w_y * d_Oy ) + ( w_z * d_Oz ) + ( v_Ox * d_x ) + ( v_Oy * d_y ) + ( v_Oz * d_z )
       is the same as
       ( w_x * d_Qx ) + ( w_y * d_Qy ) + ( w_z * d_Qz ) + ( v_Qx * d_x ) + ( v_Qy * d_y ) + ( v_Qz * d_z )
( w_x * d_Qx ) + ( w_y * d_Qy ) + ( w_z * d_Qz ) + ( v_Qx * d_x ) + ( v_Qy * d_y ) + ( v_Qz * d_z )
= ( w_x * ( d_Ox - l * d_z ) ) + ( w_y * d_Oy ) + ( w_z * ( d_Oz + l * d_x ) ) + ( ( v_Ox - l * w_z ) * d_x ) + ( v_Oy * d_y ) + ( ( v_Oz + l * w_x ) * d_z )
= ( w_x * d_Ox ) + ( w_y * d_Oy ) + ( w_z * d_Oz ) + ( v_Ox * d_x ) + ( v_Oy * d_y ) + ( v_Oz * d_z )

"""

"""
~~ Force ~~
      : A general force on a rigid body can be expressed as the sum of 
        A linear force f acting along a line passing through any chosen point P +
        A couple n_p
        
However, if we choose a different point O as the origin, then the force can be expressed as
        A linear force f acting along a line passing through the new point O +
        A couple n_O = n_p + cross( OP , f )
        
 Define:
      O   : Fixed origin
      P   : Point on a rigid body
      f   : linear force on the rigid body, acting through point O
      n_P : Couple acting on the rigid body
      n_O : couple acting about a line through O , n_p + cross( OP , f )
      OP  : Displacement vector between O and P
      
* f = transpose( [ n_O , f ] ) = transpose( [ n_Ox , n_Oy , n_Oz , f_x , f_y , f_z ] )
    = ( n_Ox * d_x ) + ( n_Oy * d_y ) + ( n_Oz * d_z ) + ( f_x * d_Ox ) + ( f_y * d_Oy ) + ( f_z * d_Oz )

This expression is a complete description of the forces acting on a rigid body , and it is invariant with respect to the location of the coordinate frame

~~ Coordinate Transforms ~~
Transform from A to B for motion vectors

X(A->B) = cross(  [ [ E , 0 ] ,  ,  [ [ 1   , 0 ] ,  )
                    [ 0 , E ] ]       [ rX^T , E ] ]
A  : Original Basis
B  : Transformed Basis
r  : Displacement vector between the bases
rX : Skew symmetic matrix for cross product with r
rX = [ [    0 , -r_z ,  r_y ] ,
       [  r_z ,    0 , -r_x ] , 
       [ -r_y ,  r_x ,    0 ] ]

The corresponding transform for force vectors is the inverse transpose of the above
X*(A->B) = transpose( inv( X(A->B) ) )

~~ Basic Operations ~~

If bodies A and B have velocities v_A and v_B , respectively , then the relative velocity of B with respect to A is
v_rel = v_B - v_A


~~ Spatial Cross Products ~~

There are two cross product operations: One for motion vectors and one for forces

cross( vHat_O , mHat_O ) = cross( transpose( [ w , v_O ] ) , transpose( [ m , m_O ] ) )
                         = [ [           cross( w , m )            ]  , 
                             [ cross( w , m_O ) + cross( v_O , m ) ] ]
                         
cross_star( vHat_O , fHat_O ) = cross_star( transpose( [ w , v_O ] ) , transpose( [ n_O , f ] ) )
                              = [ [ cross( w , n_O ) + cross( v_O , f )  ] , 
                                  [          cross( w , f )              ] ]
                              
vHat_O , mHat_O are motion vectors , and fHat_O is a force

~~ Differentiation ~~

The derivative of a spatial vector is itself a spatial vector

The derivative of a spatial vector that is fixed in a body moving with velocity v is 

d_dt( s ) 
         = cross( v , s )      : if s is a motion vector
         = cross_star( v , s ) : if s is a force vector

~ Differentiation in Moving Coordinates ~
( d_dt( s ) )_O 
                = d_dt( s_O ) + cross( v_O , s_O )      : if s is a motion vector
                = d_dt( s_O ) + cross_star( v_O , s_O ) : if s is a force vector
                
~~ Acceleration ~~

aHat = d_dt( vHat ) = transpose( wDot , vDot_O ) , vDot_O is not the acceleration of any point in the body!

O      : Fixed point in space
v_O(t) : Velocity of the body-fixed point that coincides with O at time t
v_O    : Velocity at which body-fixed points are streaming through O
vDot_O : Rate of change of the stream velocity
________/
\> If a body rotates with constant angular velocity about a fixed axis , then its spatial velocity is constant and its spatial acceleration
   is zero ; but each body-fixed point is following a circular path , and is therefore accelerating

r      : 3D Vector giving the position of the body-fixed point that coincides with O at the current instant , measured relative to any fixed point

vHat = transpose( [ w , v_O ] ) = transpose( [ rDot , v_O ] )

and

aHat = transpose( [ wDot , vDot_O ] ) = [ [             wDot            ] , 
                                          [ rDotDot - cross( w , rDot ) ] ]

The spatial vector derivative of velocity does not include a coriolis term


~~~~ Inverse Dynamics ~~~~

   base
//--------, ,--------, ,----/ /-, ,--------+==]]
// link 0  O  link 1  O    / /   O  link n |
//--------'^'--------'^'--/ /---'^'--------+==]]
  joint 1_/  joint 2_/  joint n_/

qDot_i , qDotDot_i , s_i : joint velocity , joint acceleration , joint axis
               v_i , a_i : link velocity , link acceleration
                     f_i : force transmitted from linke i-1 to i
                   tau_i : joint force
                     I_i : Link inertia
                     
Velocity of Link i :
v_i = v_{i-1} + s_i * qDot_i , The velocity of link i-1 plus the velocty across joint i

Acceleration of Link i : The derivative of velocity
a_i = ( a_{i-1} ) + ( sDot_i * qDot_i + s_i * qDotDot_i )
                    ^-- Product Rule

Equation of Motion for Link i :
f_i - f_{i-1} = I_i * a_i + cross_star( v_i , I_i * v_i )

Force for Joint i :
tau_i = transpose( s_i ) * f_i


~~~ The Recursive Newton-Euler Algorithm ~~~

v_i = v_{i-1} + s_i * qDot_i                              , ( v_0 = 0 )

a_i = ( a_{i-1} ) + ( sDot_i * qDot_i + s_i * qDotDot_i ) , ( a_0 = 0 )

f_i - f_{i-1} = I_i * a_i + cross_star( v_i , I_i * v_i )

tau_i = transpose( s_i ) * f_i
"""