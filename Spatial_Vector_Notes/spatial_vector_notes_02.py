#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division # MUST be run before all other expressions , including docstrings!

"""
spatial_vector_notes_02.py
James Watson , 2017 June , Written on Spyder 3 / Python 2.7
Continuation of Featherstone spatial coordinates with an emphasis on code implementation of worked examples
"""

# == Init ==================================================================================================================================

# ~~ Helpers ~~
def add_valid_to_path( pathList ):
    """ Add all the valid paths in 'pathList' to the Python path """
    import sys , os
    for path in pathList:
        if os.path.isdir( path ):
            sys.path.append( path )
            print "Loaded" , path
# ~~ Imports ~~
# ~ Standard ~
import sys , os , time
from math import atan , sin , cos , pi , radians
# ~ Special ~
import numpy as np
# ~ Local ~
localPaths = [ os.path.join( "C:" , os.sep , "Users" , "jwatson" , "Documents" , "Python Scripts" ) ] # List of paths to your custom modules
add_valid_to_path( localPaths )
from XOS_util import concat_arr

# == End Init ==============================================================================================================================


# == Plucker Coordinates and Operations ==

def v_w_to_Plucker( v_p , w , P ):
    """ Transform a linear velocity 'v' through P and 
    rotational velocity 'w' about a line through P into a Plucker representation """
    v_O = v_p + np.cross( P , w )
    return [ w[0] , w[1] , w[2] , v_O[0] , v_O[1] , v_O[2] ]

def cross_motn( motnVec1 , motnVec2 ):
    """ Take the motion-by-motion cross-product for spatial vectors """
    return concat_arr( np.cross( motnVec1[:3] , motnVec2[:3] ) , 
                       np.cross( motnVec1[:3] , motnVec2[3:] ) + np.cross( motnVec1[3:] , motnVec2[:3] ) )

def cross_forc( motionVec , forceVec ):
    """ Take the motion-by-force cross-product for spatial vectors """
    return concat_arr( np.cross( motionVec[:3] , forceVec[:3] ) + np.cross( motionVec[3:] , forceVec[3:] ) , 
                       np.cross( motionVec[:3] , forceVec[3:] ) )
    
def skew_sym_cross( vecR ):
    """ Return the skew symmetic matrix for the equivalent cross operation: [r_cross][v] = cross( r , v ) """
    return [ [  0       , -vecR[2] ,  vecR[1] ] , 
             [  vecR[2] ,  0       , -vecR[0] ] ,
             [ -vecR[1] ,  vecR[0] ,  0       ] ]

def cross_motn_matx( motionVec ): # Acts on a motion vector --> produces a motion vector
    """ Return the matrix for the equivalent cross operation: [motionVec_cross][v] = cross( motionVec , v ) """
    return np.vstack( ( np.hstack( ( skew_sym_cross( motionVec[:3] ) , np.zeros( (3,3) )               ) ) , 
                        np.hstack( ( skew_sym_cross( motionVec[3:] ) , skew_sym_cross( motionVec[:3] ) ) ) ) ) # 6x6
    
def cross_forc_matx( forceVec ): # Acts on a force vector --> produces a force vector
    """ Return the matrix for the equivalent cross operation: [forceVec_cross][v] = cross_star( forceVec , v ) """
    return np.vstack( ( np.hstack( ( skew_sym_cross( forceVec[:3] ) , skew_sym_cross( forceVec[3:] ) ) ) , 
                        np.hstack( ( np.zeros( (3,3) )              , skew_sym_cross( forceVec[:3] ) ) ) ) ) # 6x6
    

# == End Plucker ==


# == Spatial Dynamics ==



# == End Dynamics

"""
Vector spaces only require that addition and multiplication be defined. Euclidean vectors are special in that
they have other operations defined , like the inner product , which give them the property of magnitude and
direction.

A coordinate vector can be expressed as a linear combination of basis vectors. The most useful bases for a
Euclidean vector space are orthonormal bases , which give rise to the Cartesian coordinate system.

Spatial Vectors are not Euclidean.

Motion vectors and Force vectors are duals of each other. To qualify as a dual basis , the vectors d_i and 
e_i must satisfy the following condition:
    
    dot( d_i , e_j ) = / 1 , if i = j 
                      {
                       \ 0 , otherwise
                       
dot( m , f ) = transpose( m ) * f
Dual coordinates are the spatial vector equivalent 
  - A general property of dual coordinate systems is that motion and force vectors obey different  
    coordinate transformation rules
    
In screw theory , the combination of linear and angular motion is called a twist..
  - In general , the instantaneous screw axis of motion will change moment to moment
  - If the linear magnitude is 0 , then the motion is pure rotation
  - If the angular magnitude is 0 , then the motion is pure translation
  - The ratio of the angular and linear magnitudes is called the pitch
  
In screw theory , the combination of linear force and angular torque is called a wrench
  - If the linear magnitude is 0 , then the motion is pure torque (moment)
  - If the angular magnitude is 0 , then the motion is pure force
  
The choice of a reference point is not important to spatial vector operations , and is akin to choosing a
coordinate system.

X_BA      : The coordinate transformation matrix  A --> B ( Motion Vectors )
X_Star_BA : The coordinate transformation matrix  A --> B ( Force Vectors )

X_Star_BA = transpose( inverse( X_BA ) )

X_BA      = np.dot(  [ [ [E] , [0] ]         [ [  [1]       ,  [0]       ] 
                       [ [0] , [E] ] ]   ,     [ -[r_cross] ,  [1]       ] ]

X_Star_BA = np.dot(  [ [ [E] , [0] ]         [ [  [1]       , -[r_cross] ] 
                       [ [0] , [E] ] ]   ,     [  [0]       ,  [1]       ] ]

E   : Coordinate transform from Cartesian basis C_A to C_B    
[1] : Identity Matrix
[0] : Zero Matrix

The derivative of a coordinate vector is always its component-wise derivative. If the basis vectors vary 
with [x], the derivative will vary from the case in which they do not by a term depending on the derivatives
of the basis vectors. 

If m and f are fixed in a body B and are varying only because B is in motion , then

mDot =      cross( v , m )
fDot = cross_star( v , f )

Spatial acceleration is just the time derivative of spatial velocity.

O   : fixed point in space
O'  : body-fixed point that happens to coincide with O athe current instant time
B   : rigid body 
w   : rotational velocity of B
v_O : linear velocity of B

r   : vector O-->O'
      r = [0] at this instant , but r != [0] in general
     
v_{O'} = rDot , vDot_{O'} = rDotDot , so

v_O    = v_{O'}    - cross( w    , r )
vDot_O = vDot_{O'} - cross( wDot , r ) - cross( w , rDot )

when r = [0]

v_{O'}    = rDot    , v_O    = rDot
vDot_{O'} = rDotDot , vDot_O = rDotDot - cross( w , rDot )

So the formula for spatial acceleration is
     d        d [ [ w   ] ,     [ [ wDot                        ] ,
a = ---(v) = ---  [ v_O ] ]  =    [ rDotDot - cross( w , rDot ) ] ]
     dt       dt
     
rDot is the velocity of a particular body-fixed partivle ,  but v_O is the velocity of a measured at O of
the stream of body-fixed particles passing through 0.
rDotDot is the acceleration of a a particular body-fixed particle , but vDot_O is the rate of change in the
velocity ot which successive fixed-body particles stream through O.

Spatial accelerations can be summed like velocities.  That is , the formulation includes coriolis accelerations.

If 2 bodies B1 and B2 are connected by a joint such that the two velocities obey

v_2 = v_1 + s * qDot
s    : joint axis
qDot : joint velocity

then the relationship between their accelerations is obtained by acceleration

a_2 = a_1 + sDot * qDot + s * qDotDot

~~~ Inertia ~~~

The spatial inertia of a rigid body is a tensor that maps its velocity to its momentum

h = [I]v

I rigid bodies B1 ... Bn are rigidly connected together to form a composite body , then the inertia of the 
composite is

[I_tot] = sum_{i=1}{N}( [I_i] )

Spatial inertia is a symmetric , positive-definite matrix when expressed in any dual coordinate system
(positive , semi-definite in some special cases)

Expressed in Plucker Coordinates , the spatial inertia of a rigid body is

[I] = [ [ [I_c] + m * dot( [c_cross] , transpose( [c_cross] ) ) , m * [c_cross] ] , 
        [ m * transpose( [c_cross] )                            , m * [1]       ] ]
m     : body mass
c     : COM (3D vector)
[I_c] : body's rotational inertia about its center of mass

~ Coordinate Transform of Spatial Inertia ~

I_b = dot( X_Star_BA , I_A , X_AB )

X_BA      : The coordinate transformation matrix  A --> B ( Motion Vectors )
X_Star_BA : The coordinate transformation matrix  A --> B ( Force Vectors )
X_AB      : The coordinate transformation matrix  B --> A ( Motion Vectors )

The above formula is valid for any dual coordinate system , not only Plucker coordinates.

The time derivative of inertia is
 d
---[I] = cross_star( v , [I] ) - dot( [I] , [v_cross] )
 dt
 
The kinetic energy of a rigid body is

E = 0.5 * dot( v , [I] , v )


~~ Equations of Motion ~~

      d
f =  ---( dot( [I] , v ) ) = dot( [I] , a ) + cross_star( v , dot( I , v ) )
      dt
      
Which can be rewritten in a simplified form:
    
f = dot( [I] , a ) + p

p : bias force , known component
f : total force , unknown component

Example: Of the forces acting on a body consisted of an unknown force and a gravitational force , the bias 
         force can be defined as follows
         
TODO: Need to find out if dot( v_cross_star , [I] , v )    is the same as
                          cross_star( v , dot( [I] , v ) ) in general
         
p = cross_star( v , dot( [I] , v ) ) - f_g

and

f_g = dot( [I] , a_g )

f_g : gravitational force
a_g : acceleration due to gravity


~~ Motion Constraints ~~

In the simplest case , a motion constraint between two rigid bodies B1 and B2 resctricts their relative 
velocity to a vector subspace  S \in M^6 , which can vary with time. If r is the dimensionality of S , 
then the constrain allows r DOF of relative motion between the two bodies and imposes 6-r constraints.
Let { s_1 ... s_r } be any set of vectors that span S (forming a basis on S).  The relative velocity between
the two bodies can be expressed:
    
v_rel = v_2 - v_1 = \sum_{i=1}{r}( s_i * qDot_i )

{ qDot_i } : A set of velocity variables , one for each DOF

Usually { s_1 ... s_r } are gathered into a single 6 x r matrix [S] , such that

v_rel = v_2 - v_1 = dot( [S] , [qDot] )

[qDot] : An r-dimensional coordinate vector of the velocity variables

Differentiate for relative acceleration:
    
a_rel = a_2 - a_1 = dot( [SDot] , [qDot] ) + dot( [S] , [qDotDot] )

Motion constraints are implemented by constraint forces , and constraint forces all have the following
special property: A constraint force does no work in any direction of motion permitted by the constraint:
    
dot( transpose( [S] ) , f_c ) = [0]

f_c : A constraint force transmitted B1 --> B2 , -f_c acts B2 --> B1

~ Powered Joints ~

dot( transpose( [S] ) , f_J ) = [\tau]

f_J    : Total force transmiited across the joint (active and constraint forces)
[\tau] : Vector of generalized force variables

[\tau] must be defined such that 
dot( transpose( [\tau] ) , [qDot] ) is the instantaneous power delivered by the joint to the system
"""

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