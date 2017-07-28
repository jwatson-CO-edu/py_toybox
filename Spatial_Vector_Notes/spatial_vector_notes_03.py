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
from XOS_util import concat_arr , eq , enumerate_rev , np_dot

# == End Init ==============================================================================================================================

# == Utility Functions ==

def left_divide( A , b ):
    """ Least-squares solution to an under to over-determined linear system  
        x = left_divide( A , b ) is the solution to dot(A,x) = b , and equivalent to MATLAB A\b """
    x , resid , rank , s = np.linalg.lstsq( A , b )
    return x

# == End Utility ==

# == 3D Vector Arithmetic ==

def skew_sym_cross( vecR ):
    """ Return the skew symmetic matrix for the equivalent cross operation: [r_cross][v] = cross( r , v ) """
    return [ [  0       , -vecR[2] ,  vecR[1] ] , 
             [  vecR[2] ,  0       , -vecR[0] ] ,
             [ -vecR[1] ,  vecR[0] ,  0       ] ]
    
def x_rot( theta ):
    """ Return the matrix that performs a rotation of 'theta' about the X axis """
    return [ [  1            ,  0            ,  0            ] , 
             [  0            ,  cos( theta ) ,  sin( theta ) ] , 
             [  0            , -sin( theta ) ,  cos( theta ) ] ]
    
def y_rot( theta ):
    """ Return the matrix that performs a rotation of 'theta' about the Y axis """
    return [ [  cos( theta ) ,  0            , -sin( theta ) ] , 
             [  0            ,  1            ,  0            ] , 
             [  sin( theta ) ,  0            ,  cos( theta ) ] ]
    
def z_rot( theta ):
    """ Return the matrix that performs a rotation of 'theta' about the Z axis """
    return [ [  cos( theta ) ,  sin( theta ) ,  0            ] , 
             [ -sin( theta ) ,  cos( theta ) ,  0            ] , 
             [  0            ,  0            ,  1            ] ]

# == End 3D Vector ==


# == Plucker Coordinates and Operations ==

def xlt( r ):
    """ Rotational transform of Plucker coordinates """
    return np.vstack( ( np.hstack( ( np.eye(3)                               , np.zeros( (3,3) ) ) ) ,
                        np.hstack( ( np.multiply( skew_sym_cross( r ) , -1 ) , np.eye(3)         ) ) ) )

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

def cross_motn_matx( motionVec ): # (Featherstone: crm) # Acts on a motion vector --> produces a motion vector
    """ Return the matrix for the equivalent cross operation: [motionVec_cross][v] = cross( motionVec , v ) """
    return np.vstack( ( np.hstack( ( skew_sym_cross( motionVec[:3] ) , np.zeros( (3,3) )               ) ) , 
                        np.hstack( ( skew_sym_cross( motionVec[3:] ) , skew_sym_cross( motionVec[:3] ) ) ) ) ) # 6x6
    
def cross_forc_matx( forceVec ): # (Featherstone: crf) # Acts on a force vector --> produces a force vector
    """ Return the matrix for the equivalent cross operation: [forceVec_cross][v] = cross_star( forceVec , v ) """
    return np.vstack( ( np.hstack( ( skew_sym_cross( forceVec[:3] ) , skew_sym_cross( forceVec[3:] ) ) ) , 
                        np.hstack( ( np.zeros( (3,3) )              , skew_sym_cross( forceVec[:3] ) ) ) ) ) # 6x6
    

def XtoV( X ):
    """ Calculate the small-magnitude motion vector from the transform for a small change in coordinates """
    return np.multiply( 0.5 , 
                        [ X[1][2] - X[2][1]  ,  X[2][0] - X[0][2]  ,  X[0][1] - X[1][0] , 
                          X[4][2] - X[5][1]  ,  X[5][0] - X[3][2]  ,  X[3][1] - X[4][0] ] )
    """ Suppose A and B are two Cartesian frames ( and also the Plucker coordinate systems defined by those frames ) 
    If A and B are close together , then 'XtoV' approximates the the velocity vector that would move frame A to coincide with B after one
    timestep. This is invariant to 'X' and therefore would be the same for A and B. """

# == End Plucker ==


# == Robot Model ==

# TODO: Fill in the details of the inverse dynamics function as the article progresses

# = Model Classes & Functions =

class LinkSpatial:
    """ Represents a rigid link and the associated joint using spatial coordinates """
    def __init__( self , pName , pPitch ):
        """ Rigid link struct """
        self.name = pName # - String that uniquely identifies the link
        self.pitch = pPitch # Describes the pitch (and therefore the type) of the associated joint
        self.parent = None #- Reference to the parent link to which this link is attached
        self.children = [] #- List of child links
        self.linkIndex = 0 #- Index of link in q 
        self.xform = None # - Plucker coordinate transform that describes the relative position of this joint in the parent frame
        self.I = None # ----- Spatial inertia for this link
        self.q = 0 # -------- Joint configuration ---> These used for caching and for preserving state across timesteps
        self.qDot = 0 # ----- Joint Velocity        /
        self.qDotDot = 0 # -- Joint Acceleration  _/
        self.v = 0 # -------- Link Spatial Velocity     ---> These are the result of dynamics calculations
        self.a = 0 # -------- Link Spatial Acceleration   /
        self.f = 0 # -------- Joint Spatial Force        /
        self.tau = 0 # ------ Torque about this joint  _/
        
    def calc_link_I( self , mass , COM , I_COM ):
        """ Calculate and set the link rotational inertial about the joint """
        cX = cross_motn_matx( COM )
        self.I = np.vstack( ( np.hstack( ( I_COM - np.multiply( mass , np.dot( cX , cX ) ) , np.multiply( mass , cX )        ) ) , 
                              np.hstack( ( np.multiply( -mass , cX )                       , np.multiply( mass , np.eye(3) ) ) ) ) )

class LinkModel(object):
    """ Represents a serial-link manipulator composed of rigid links and defined with spatial vectors """
    
    def __init__( self ):
        """ Create a model with an empty list of links """
        self.N = 0 # -------------------------------- Number of links in the mechanism
        self.links = []; # -------------------------- Links of the model , stored in the order of q
        self.names = set([]) # ---------------------- Set of all link names in the model
        self.gravity = [ 0 , 0 , 0 , 0 , 0 , 9.81 ] # Default direction of gravity as a spatial vector
        
    def link_ref_by_name( self , linkName ):
        """ Get the reference to the link by its name , linear search """
        if linkName in self.names:
            for lnk in self.links:
                if lnk.name == linkName:
                    return lnk
        raise KeyError( "LinkModel.link_ref_by_name: No link found with name " + str( linkName ) )
        
    def add_and_attach( self , link , parentName = None ):
        """ Add the link to the model , then  """
        link.linkIndex = self.N
        self.N += 1
        self.names.add( link.name )
        self.links.append( link )
        if parentName in self.names: # If there was a parent link specified and such a link has been added to the model
            parent = self.link_ref_by_name( parentName ) # Fetch parent
            link.parent = parent # Add the parent reference # NOTE: This will raise a KeyError if no such parent was stored
            parent.children.append( link ) # Add the child reference
            
    # NOTE: Not implementing the ability to remove links at this time
    
    def set_q( self , q ):
        """ Set the configuration of the robot """
        assert( len( q ) == len( self.links ) , "LinkModel.set_q: 'len(q)' must equal the number of links!" )
        for lnkDex , link in enumerate( self.links ):
            link.q = q[ lnkDex ]
        
def joint_xform( pitch , q ): # Featherstone: jcalc
    """ Return the joint transform and subspace matrix for a joint with 'pitch' and joint variable 'q' """
    if eq( pitch , 0.0 ): # Revolute Joint : Implements pure rotation
        XJ  = x_rot( q ) 
        s_i = [ 0 , 0 , 1 , 0 , 0 , 0 ]
    elif pitch == infty: # Prismatic Joint : Implements pure translation
        XJ  = xlt( [ 0 , 0 , q ] )
        s_i = [ 0 , 0 , 0 , 0 , 0 , 1 ]
    else: #                Helical Joint   : Implements a screwing motion
        XJ  = np.dot( z_rot( q ) , xlt( [ 0 , 0 , q * pitch ] ) )
        s_i = [ 0 , 0 , 1 , 0 , 0 , pitch ]
    return XJ , s_i

# = End Classes =

# = Spatial Dynamics =

def inverse_dynamics( model ): # , q , qDot , qDotDot ):
    """ Compute the inverse dynamics from the model with the Recursive Newton-Euler Algo """ 
    # NOTE: This function assumes that 'model' has 'q' , 'qDot' , 'qDotDot' set for joints
    # ~ Forward Pass ~
    for lnkDex , link in enumerate( model.links ): # For every link in the model , do
        [ XJ , s_i ] = joint_xform( link.pitch , link.q ) # (FS: 'jcalc') calc the joint transformation and freedom (selection) matrix
        vJ = np.dot( s_i , link.qDot ) # Calc joint velocity
        Xup = np.dot( XJ , link.xform ) # Transform the link coordinates into the world frame
        if not link.parent: # if there is no parent link
            link.v = vJ
            link.a = np.dot( Xup , model.gravity ) + np.dot( s_i , link.qDotDot )
        else: # else link is child of another link # NOTE : This will cause problems unless the links are added in levels root to leaf
            link.v = np.dot( Xup , link.parent.v ) + vJ
            link.a = np.dot( Xup , link.parent.a ) + np.dot( s_i , link.qDotDot ) + np.dot( cross_motn_matx( link.v ) , vJ )
        link.f = np.dot( link.I , link.a ) + np.dot( np.dot( cross_forc_matx( link.v , link.I ) ) , 
                                                     link.v )
    # ~ Backward Pass ~ # NOTE : This will cause problems unless the links are added in levels root to leaf
    for lnkDex , link in enumerate_rev( model.links ): # For every link in the model (reverse order) , do
        link.tau = np.dot( np.transpose( s_i ) , link.f )
        if link.parent:
            link.parent.f += np.dot( np.transpose( Xup ) , link.f )
    
# = End Dynamics =

# = Forward Kinematics =

def FK( model , bodyIndex , q ): # ( Featherstone: bodypos )
    """ Compute the pose for a given config 'q' """
    # NOTE: This function does not depend on the presently stored q state , returned pose depends only on given 'q'
    X = np.eye(6) # Init pose frame
    body = model.links[ bodyIndex ] # Fetch the link by index
    while body: 
        [ XJ , s_i ] = joint_xform( body.pitch , q[ bodyIndex ] )
        X = np_dot( X , XJ , body.xform )
        body = body.parent # This will become 'None' after the root link has been processed
        
def jacobn_manip( model , bodyIndex , q ): # ( Featherstone: bodyJac )
    """ Compute the manipulator jacobian up to the specified link in the tree """
    # NOTE: This function does not depend on the presently stored q state , returned pose depends only on given 'q'
    e = np.zeros( model.N )
    body = model.links[ bodyIndex ] # Fetch the link by index
    while body:
        e[ body.linkIndex ] = 1
        body = body.parent # This will become 'None' after the root link has been processed
    J = np.zeros( ( 6 , model.N ) ) # Matrix for the Jacobian
    Xa = np.zeros( model.N ) # An array of transforms
    for lnkDex , link in enumerate( model.links ): 
        if e[ lnkDex ]:
            [ XJ , s_i ] = joint_xform( link.pitch , q[ lnkDex ] )
            Xa[ lnkDex ] = np.dot( XJ , link.xform )
            if link.parent:
                Xa[ lnkDex ] = np.dot( Xa[ lnkDex ] , Xa[ link.parent.linkIndex ] )
            x , resid , rank , s = np.linalg.lstsq( Xa[ lnkDex ] , s_i )
            J[ : , lnkDex ] = x
    return J

# = End FK =

# = Inverse Kinematcis =

# NOTE: This does not check for singularities or infeasible poses and is not a serious IK solution

def IK_pos( model , body , Xd , q0 , criterion = 1e-10 ): 
    """ Perform iterative Jacobian IK for pose 'Xd' starting from configuration 'q0' """ # TODO: Consider implementing an iteration limit
    q = q0 # Init q to the specified starting state
    dPos = np.ones( 6 ) # Init position difference # This is very likely to not define the desired pose
    while np.linalg.norm( dPos ) > criterion: # While the body pose is not close enough to the desired body pose
        X = FK( model , body.linkIndex , q ) # Calc X_{d->b}
        J = jacobn_manip( model , body.linkIndex , q ) # Calc the manipulator Jacobian for the link
        Jm = np.dot( X , J ) # Calc J_{b->b} , Get the jacobian in the body's own frame
        dPos = XtoV( left_divide( Xd , X ) ) # Calc a difference vector between the present and the desired pose
        Jm_T = np.transpose( Jm )
        dq = np.dot( Jm_T , ( left_divide( np.dot( Jm , Jm_T ) , dPos ) ) ) # qDelta = dot( J_pinv_{b->b} , pDelta ) # pseudo-inverse step
        q += dq # Increment q
    return q

# = End IK =

# == End Model ==

"""
=== REVIEW 3 , TUTORIAL 2 =====================================================================================

~~~ Inverse Dynamics , A Computational Example ~~~

Spatial vectors can be used both for positional kinematics and for instantaneous kinematics.

[tau] = ID( model , [q] , [qDot] , [qDotDot] )

 Body parent(i)            Body i
,------------,            ,------------,
|^          ^|   X_J[i]   |^           |
|+-> X_T[i] +-> ......... |+->         |
|F_p(i)     F_p(i),i      |F_i         |
`------------`            `------------`
F_i      : Coordinate frame of Body i
F_p(i)   : Coordinate frame of Body parent(i)
F_p(i),i : Coordinate frame of Joint i in the parent(i) frame
X_T[i]   : Transform from F_p(i) to F_p(i),i , Joint location transform
X_J[i]   : Transform from F_p(i),i to F_i    , Joint config transform

F_i and F_p(i),i must coincide when the joint variable for i is 0
F_i and F_p(i),i must comply with the joint-specific alignment requirements of joint i
    * The Z-axes of F_i and F_p(i),i must coincide for revolute and helical joints
A parent body can have any number of successor bodies

~~ Joint Models ~~

A joint is a kinematic constraint between two bodies.
A mathematical model of a joint consists of two quantities:
    X_J  : Coordinate transform
           X_J(i) : Coordinate transform from F_p(i),i to F_i
    S_i  : Motion subspace matrix (free modes matrix)
    v_Ji : Velocity across the joint
    
v_Ji  = dot( S_i              , qDot_i )
tau_i = dot( transpose( S_i ) , f_Ji   )

If Joint i permits n_i degrees of freedon , S_i is a [ 6 X n_i ] matrix
The total number of joint variables is:
    
n = \sum_{i=1}{N}( n_i )

For this tutorial , the types of joints will be limited to those with 1DOF: { revolute , prismatic , helical }
Revolute and prismatic joints can be treated as special cases of helical joints with zero and infinite pitch, respectively

Power Balance Equation

dot( tau_i , qDot_i ) = dot( f_Ji , v_Ji )

----------------------------------------------------
~~~~ Recursive Newton-Euler for Spatial Vectors ~~~~
----------------------------------------------------

v_i   = v_p(i) + dot( s_i , q_i )  , v_0 = 0  # The velocity of body i is the sum of the velocity of its parent and the velocity across joint i
a_i   = a_p(i) + dot( s_i , qDotDot_i ) + cross( v_i ,                             # The accleration of body i is the sum of the acceleration 
                                                 dot( s_i , qDot_i )  , a_0 = -a_g # of the parent and the acceleration across joint i
f_Bi  = dot( I_i , a_i ) + cross_star( v_i ,                          # ^-- This trick is essentially an "acceleration offset"
                                       dot( I_i , v_i ) ) # Equation of motion: The net force acting on body i is the force across joint i
f_Ji  = f_Bi + \sum_{j \in c(i)}( f_Jj ) # Calculate the joint forces from the body forces
tau_i = dot( transpose( s_i ) , f_Ji ) # Joint torque


~~ Kinematics ~~

Body positions can be calculated recursively using the formula:
    
X_{i->0} = np.dot( X_{i->p(i)} , X_{p(i)->0} ) , p(i) != 0

which calculates the coordinate transform from body coordinate frame i to the reference frame (0) 

If frame b is already close to frame d , then we can use an approximated small screw displacement to move frame b to be coincident with d

pDelta = XtoV( X_{d->b} ) = XtoV( dot( X_{d->0} , X_{0->b} ) )

If frame F_d is a reachable position for body b , then there will be a joint position change , qDelta , that causes a displacement pDelta
in body b. In general, qDelta will not be unique, therefore the relationship between pDelta and qDelta is not closed form and may be 
difficult to obtain. However , this relationship can be approximated:

pDelta = dot( J_{b->b} , qDelta )

J_{b->b} : Jacobian for body b expressed in b coordinates

~~ Jacobians ~~

A jacobian is a matrix that maps the joint-space velocity vector qDot to some other kind of velocity.
In this tutorial, the body Jacobian is the matrix that maps qDot to the spatial velocity of body b.

v_b = dot( J_b , qDot )

The velocity of the body can be expressed as 

v_b = \sum_{i}{body->root}( dot( s_i , qDot_i ) )

which states that v_b is the sum of the joint velocities of all the joints on the path between the body and the fixed base.
This can be rewritten as
                                                                      / 1 , if i in the chain between the body and the root link
v_b = \sum_{i=1}{N}( e_{bi} * dot( s_i , qDot_i ) ) , where e_{bi} = {
                                                                      \ 0 , otherwise
                                                                      
yielding the following expression

J_b = [ e_{b1} * s_1 , e_{b2} * s_2 , ... , e_{bi} * s_i , ... , e_{bN} * s_N ]

So the body jacobian is a 6 x N matrix whose ith column is either s_i or [0] , depending on whether or not joint i is on the path to the root

More generally, a body jacobian is a 1 x N block matrix in which the ith block is a 6 x n_i matrix e_{bi} * s_i
Every column of the body jacobian must be expressed in the same coordinate system as the velocity vector that it maps to.  The coordinate
transformation rule for a body is

J_{B->b} = dot( X_{B->A} , J_{A->b}

~ A Common Trap ~

Consider an equation of the form

[ [ w ] , = dot( [ J ], [ qDot ] ) 
  [ v ] ]
Where w and v are described as the angular and linear velocity of some link expressed in the lab frame coordinates.

In translating this from 3D vectors to spatial vectors, it is tempting to regard the left-hand expression to be the Plucker coordinates of 
the spatial velocity expressed in frame 0.  However, this is probably incorrect, as the 3D vector v usually refers to some particular point
in the end effector, and does not correspond to the origin of F_0.  Rather, the left-hand expression contains the Plucker coordinates of the 
spatial velocity of the end-effector expressed in a coordinate system that is parallel to the absolute coordinates but has it's origin at the
end-effector point referred to by v.

~ Jacobians and Forces ~

If a robot makes contact with its environment through body b, and the environment responds by exerting a force f_e on body b, then the effect
of that force on the robot is equivalent to a joint-space force \tau_e, given by

tau_e = dot( transpose( J_b ) , f_e )

Naturally, the robot's control system can resist this force by adding -tau_e to its joint-force command

~~ Acceleration ~~

Nonrecursive version of the body acceleration calculation:
    
a_b = \sum_{i}{body->root}( dot( s_i , qDotDot_i ) + dot( sDot_i , qDot_i ) )

If we assume that sDot_i = cross( v_i , s_i ) , then the above equation can be further expanded to:
    
a_b = \sum_{i}{body_b->root}( dot( s_i , qDotDot_i ) ) + 
      \sum_{i}{body_b->root}( cross( \sum_{j}{body_i->root}( dot( s_j , qDot_j ) ) , dot( s_i , qDot_i ) ) ) 
      
    = \sum_{i}{body_b->root}( dot( s_i , qDotDot_i ) ) + 
      \sum_{i}{body_b->root}( \sum_{j}{body_i->root}( cross(  dot( s_j , qDot_j ) , dot( s_i , qDot_i ) ) ) )
      
It is sometimes useful to define the velocity product acceleration term as 

aVP_b = \sum_{i}{body_b->root}( \sum_{j}{body_i->root}( cross(  dot( s_j , qDot_j ) , dot( s_i , qDot_i ) ) ) )

'aVP_b' might also include gravitational acceleration if we so choose. 

Velocity product accelerations can be calculated efficiently by the recursive formula:
    
aVP_i = aVP_p + cross( v_i , dot( s_i , qDot_i ) )
        ^-- Velocity product acceleration of the parent body

Alternately, the acceleration of body b can be expressed as

a_b = dot( J_b , qDotDot ) + dot( JDot_b , qDot )

dot( JDot_b , qDot ) is not difficult to calculate if one remembers that 

dot( JDot_b , qDot ) = aVP_b 

and so

a_b = dot( J_b , qDotDot ) + aVP_b 

Constraints on mechanism loop closure, such as for two end effectors (l and r) on a branched robot gripping the same object, 
can be formulated as

dot( ( J_l - J_r ) , qDotDot ) = aVP_r - aVP_l

If this formulation is used in simulation, then care must be taken to stabilize against the accumulation of position and velocity errors


~~~~ Dynamics ~~~~

~~~ Composite Rigid-Body Algorithm ~~~

Canonical form of the joint-space motion of a kinematic tree:
    
tau = dot( [H] , qDot ) + [C]
[H] : Joint-space inertia matrix
[C] : Centrifugal + Coriolis + Gravitational 

In the above code

[C] = ID( model , q , qDot , [0] )

The kinetic energy is given by

T = KE = (0.5) * dot( transpose( qDot ) , [H] , qDot )
       = (0.5) * \sum_{i=1}{n}( \sum_{j=1}{n}( dot( H_ij , qDot_i , qDot_j ) ) ) 
       
       writing in spatial vector notation
       
       = (0.5) * \sum_{k=1}{N}( dot( transpose( v_k ) , I_k , v_k ) )
       
       substituting yields
       
       = (0.5) * \sum_{k=1}{N}( dot( transpose( \sum_{i}{k->root}( dot( s_i , qDot_i ) ) ) , I_k , \sum_{j}{k->root}( dot( s_j , qDot_j ) ) ) )
       
       = (0.5) * \sum_{k=1}{N}( \sum_{i}{k->root}( \sum_{j}{k->root}( dot( transpose( s_i ) , I_k , s_j , qDot_i , qDot_j ) ) ) )
       
       The expression on the right-hand side is a sum over all i,j,k triples in whihc both i and j are on the k->root path
       This is the same as
       
       = (0.5) * \sum_{i=1}{N}( \sum_{j=1}{N}( \sum_{k}{k \in (subtree i union subtree j)}( 
                                                                               dot( transpose( s_i ) , I_k , s_j , qDot_i , qDot_j ) 
                 ) ) )
       
For the class of robots under consideration (both eq true for all qDot and n=N) it follows that
   
[H_ij]= \sum_{k}{k \in (subtree i and subtree j)}( dot( transpose( s_i ) , I_k , s_j ) )

And further simplifications to the inertia matrix can be made
                                        / subtree i , if i \in subtree j
1. ( subtree i ) union ( subtree j ) = {  subtree j , if j \in subtree i
                                        \ 0         , otherwise

2. Define a composite rigid-body inertia Ic_i that is the inertia of all the bodies in the subtree i treated as a single composite rigid body
   Ic_i = \sum_{j \in subtree i}( I_j )
   calculated using the recursive formula
   Ic_i = I_i + \sum_{j \in children of i}( Ic_j )

With the above in mind, we can write
        / dot( transpose( s_i ) , Ic_i , s_j ) , if i \in subtree j
H_ij = {  dot( transpose( s_i ) , Ic_j , s_j ) , if j \in subtree i
        \ 0                                    , otherwise
        
** The Composite Rigid Body Algorithm is composed of the two above formulae **
   
        / dot( transpose( s_i ) , Ic_i , s_j ) , if i \in subtree j
H_ij = {  dot( transpose( s_i ) , Ic_j , s_j ) , if j \in subtree i
        \ 0                                    , otherwise
with

Ic_i = I_i + \sum_{j \in children of i}( Ic_j )     

The algorithm can be expressed in link coordinates

Ic_i = I_i + \sum_{j \in children of i}( dot( Xstar_{i->j} , Ic_j , X_{j->i} ) )

f_{p(j)->i} = dot( Xstar_{p(j)->i} , f_{j->i} )  ,  f_{i->i} = dot( Ic_i , s_i )

        / dot( transpose( f_{j->i} ) , s_j ) , if i \in subtree j
H_ij = {  H_ji                               , if j \in subtree i
        \ 0                                  , otherwise
        
The above show explicitly where the coordinate transforms are performed.
Note that s_i , I_i , and Ic_i are expressed in linki coordinates.
f_{j->i} is the spatial force, expressed in link j coordinates, that imparts an acceleration of s_i to a composite rigid body that is 
composed of all the bodies in subtree i.  The algorithm requires the calculation of f_{i->i} for every i and f_{j->i} for every
j \in {i->root}


~~~ Articulated Body Algorithm ~~~

This algo is O(n) , linear in n.

At the outset, we know neither the acceleration of body i nor the force transmitted across joint i, but we know that the relationship 
between them is linear, it must therefore be possible to express this relationship in the form

f_i = dot( IA_i , a_i ) + pA_i

IA_i : Articulated body inertia of body i
pA_i : Bias force of body i

Together these describe the acceleration response of body i to an applied spatial force, taking into account the influence of all the other
bodies in subtree i. These terms have two special properties that form the basis of the Articulated Body Algorithm. These are:
    
1. They can be calculated recursively from the tips of the tree to the base
2. Once calculated, they allow the calculation of accelerations of the bodies and joints from the base to the tips

If we assume that body i has only one child, the following equations are relevant:
    
f_i - f_j = dot( I_i , a_i ) + p_i  ________ Equation of motion for body i , which has been written in terms of the rigid-body inertia I_i 
                                             and bias force p_i , which make it obvious that the rigid-body and articulated body equations 
                                             have the same algebraic form. 

f_j = dot( IA_j , a_j ) + pA_i  ____________ Equation of motion Articulated body j , describing the relationship between f_j and a_j , taking
                                             into acount the dynamics of every body and joint in subtree j.  We assume that IA_j and pA_i
                                             are known.

a_j = a_i + c_j + dot( s_j , qDotDot_j )  __ Acceleration constraint

where

tau_j = dot( transpose( s_j ) , f_j )  _____ Force constraint

p_i = cross_star( v_i , dot( I_i , v_i ) )

c_j = cross( v_j , dot( s_j , qDot_j ) )

The objective is to use the above to obtain the unkowns f_i and a_i.

( See paper for more detailed derivations ... )

The next step is to drop the assumption that body i has only one child.  It is possible to apply the above procedure to each of the children
in turn.  This can be done because spatial inertias are additive.

IA_i = I_i + \sum_{j}{children(i)}( Ia_j )

pA_i = p_i + \sum_{j}{children(i)}( pa_j )

The definitions of Ia_j and pa_j remain unchanged.

The Articulated Body Algorithm makes a total of 3 passes through the tree:
    
    1. base->tips : Calculate the velocity terms c_i and p_i
    
    2. tips->base : Calculate IA_i , pA_i , and related terms
    
    3. base->tips : Calculate accelerations

"""

"""
=== REVIEW 2 , TUTORIAL 1 =====================================================================================

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
=== REVIEW 1 , SLIDES =========================================================================================

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