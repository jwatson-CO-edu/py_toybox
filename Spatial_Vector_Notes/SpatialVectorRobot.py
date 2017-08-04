#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2017-05-30

from __future__ import division # MUST be run before all other expressions , including docstrings!

"""
SpatialVectorRobot.py
James Watson , 2017 July , Written on Spyder 3 / Python 2.7
Implementation of Spatial Vector (Featherstone) operations , Rigid Body Algorithm , Recursuve Newton-Euler , and Articulated Body Algorithm

Dependencies: numpy , pyglet

%% Test Sequence %%

[N] A. Install and switch to MARCHHARE - This will not be done MARCHHARE is under development in a research environment and risk of accumulating
       restrictions for its use is undesireable.
[Y] 0. Render cuboid, using the primitive voxel engine as an example. Will use cuboids to construct robots - SUCCESS
    |Y| 0.a. Render multiple translated - SUCCESS
    |Y| 0.b. Render multiple rotated , OGL - SUCCESS
    |Y| 0.c. Render multiple rotated , Coord Transformation - SUCCESS
    |Y| 0.d. Compare rotations in Spatial Coordinates to rotations in OGL in order to compare correctness - SUCCESS
    |Y| 0.e. Render axes , will need these to get an idea of the relative positions and orientations of things - SUCCESS
[Y] 1. Transform a body using the joint transform(s) from the tutorial
    |Y| 1.a. Animate a single primitive that spins using already-implemented transforms - SUCCESS , Although setting the period results in a higher
             than expected framerate , framerate crashes when the window is moved
        {Y} 1.a.1. Fix the helical joint calculation - COMPLETE , Although , in the formulation presented in [2] , the transform matrix differed
                   in size depending on the type of joint implemented. It is not known at this time if this seeming inconsistency is intentional
    |Y| 1.b. Rotate    , 0 pitch
    |Y| 1.c. Translate , infty pitch
    |Y| 1.d. Screw     , finite pitch
[ ] 2. Implement a single joint
    | | 2.a. Rotate
    | | 2.b. Translate
    | | 2.c. Screw
    | | 2.d. Implement a control interface with per-joint slider and text input
[ ] 3. Implement a Robot from Robot Intro , Forward Kinematics
    | | 3.a. Position
    | | 3.b. Speed
    | | 3.c. Acceleration
[ ] 4. Implement a Robot from Robot Intro , Dynamics
    | | 4.a. Gravity
    | | 4.b. Coriolis
    | | 4.c. Friction
    | | 4.d. Forward Dynamics
[ ] 5. Implement a Robot from Robot Controls , Inverse Dynamics
[ ] 6. Tools for robot arm design
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
import os
from math import cos , sin
# ~ Special ~
import numpy as np
# ~ Local ~
# localPaths = [ os.path.join( "C:" , os.sep , "Users" , "jwatson" , "Documents" , "Python Scripts" ) ] # List of paths to your custom modules
# add_valid_to_path( localPaths )

# ~~ Aliases & Shortcuts ~~
infty = float('inf') # infinity

# ~~ Setup ~~

# == End Init ==============================================================================================================================

# == Utility Functions ==

def eq( op1 , op2 ):
    """ Return True if 'op1' and 'op2' are within 'EPSILON' of each other , otherwise return False """
    return abs( op1 - op2 ) <= eq.EPSILON
eq.EPSILON = 1e-7

def left_divide( A , b ):
    """ Least-squares solution to an under to over-determined linear system  
        x = left_divide( A , b ) is the solution to dot(A,x) = b , and equivalent to MATLAB A\b """
    x , resid , rank , s = np.linalg.lstsq( A , b )
    return x

# == End Utility ==

# === Geometry ===

# == Vector Operations ==

def vec_unit( vec ):
    """ Return a vector in the direction of 'vec' with unit length """
    return np.divide( vec , np.linalg.norm( vec ) )

def np_dot( *args ): 
    """ Perform 'np.dot' on more than two args """
    if len( args ) > 2: # If there are more than 2 args, add the first arg to recur on remainder of args
        return np.dot( args[0] , np_dot( *args[1:] ) ) # Note the star operator is needed for recursive call, unpack to positional args
    else: # base case, there are 2 args*, use vanilla 'np.add'
        return np.dot( args[0] , args[1] ) # *NOTE: This function assumes there are at least two args, if only 1 an error will occur

# == End Vector ==

# == Trigonometry ==

def ver( theta ):
    """ Versine , radians """
    return 1 - cos( theta )

def verd( theta ):
    """ Versine , degrees """
    return degrees( 1 - cos( theta ) )

# == End Trig ==

# == Geo 3D ==
    
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
    
def rot_matx_ang_axs( theta , k  ):
    """ Return the rotation matrix for the given angle , axis , and position """
    k = vec_unit( k )
    return [ [ k[0]*k[0]*ver(theta) + cos(theta)      , k[0]*k[1]*ver(theta) - k[2]*sin(theta) , k[0]*k[2]*ver(theta) + k[1]*sin(theta) ] , 
             [ k[1]*k[0]*ver(theta) + k[2]*sin(theta) , k[1]*k[1]*ver(theta) + cos(theta)      , k[1]*k[2]*ver(theta) - k[0]*sin(theta) ] , 
             [ k[2]*k[0]*ver(theta) - k[1]*sin(theta) , k[2]*k[1]*ver(theta) + k[0]*sin(theta) , k[2]*k[2]*ver(theta) + cos(theta)      ] ]

def homogeneous_Z( zTheta , pos ):
    """ Return the Homogeneous Transformation for the given parameters """
    return np.vstack( ( np.hstack( (  z_rot( zTheta )  , [ [ pos[0] ] , [ pos[1] ] , [ pos[2] ] ]  ) ) ,
                        np.hstack( (  [ 0 , 0 , 0 ]    , [ 1 ]                                     ) ) ) )
    
def homog_ang_axs( theta , k , pos ):
    """ Return the Homogeneous Transformation for the given angle , axis , and position """
    return np.vstack( ( np.hstack( (  rot_matx_ang_axs( theta , k  ) , [ [ pos[0] ] , [ pos[1] ] , [ pos[2] ] ]  ) ) ,
                        np.hstack( (  [ 0 , 0 , 0 ]                  , [ 1 ]                                     ) ) ) )
    
def apply_homog( homogMat , vec3 ):
    """ Apply a homogeneous transformation to a 3D vector """
    return ( np.dot( homogMat , [ vec3[0] , vec3[1] , vec3[2] , 1 ] ) )[:3]

def apply_spatl_3D( spatlMat , vec3 ):
    """ Apply a spatial transformation to a 3D vector """
    # return np.dot( spatlMat , [ vec3[0] , vec3[1] , vec3[2] , 0 , 0 , 0 ] )[:3]
    return np.dot( spatlMat , [ 0 , 0 , 0 , vec3[0] , vec3[1] , vec3[2] ] )[3:]

def skew_sym_cross( vecR ):
    """ Return the skew symmetic matrix for the equivalent cross operation: [r_cross][v] = cross( r , v ) """
    return [ [  0       , -vecR[2] ,  vecR[1] ] , 
             [  vecR[2] ,  0       , -vecR[0] ] ,
             [ -vecR[1] ,  vecR[0] ,  0       ] ]

def homog_xfrom( E , r ):
    """ Return the combination of rotation matrix 'E' and displacement vector 'r' as a 4x4 homogeneous transformation matrix """
    return np.vstack( ( np.hstack( (  E                              , [ [ r[0] ] , [ r[1] ] , [ r[2] ] ]  ) ) ,
                        np.hstack( (  [ 0 , 0 , 0 ]                  , [ 1 ]                               ) ) ) )

def spatial_xfrom( E , r ): # See Page 141 of [3]
    """ Return the combination of rotation matrix 'E' and displacement vector 'r' as a 6x6 spatial transformation matrix """
    return np.vstack( ( np.hstack( (  E                                                   , np.zeros( ( 3 , 3 ) )  ) ) , 
                        np.hstack( (  np.cross( E , np.transpose( skew_sym_cross( r ) ) ) , E                      ) ) ) )
    
# == End 3D ==

# === End Geometry ===

# == 3D Vector Arithmetic ==



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
        self.name = pName # -- String that uniquely identifies the link
        self.pitch = pPitch #- Describes the pitch (and therefore the type) of the associated joint
        self.parent = None # - Reference to the parent link to which this link is attached
        self.children = [] # - List of child links
        self.linkIndex = 0 # - Index of link in q 
        self.xform = None # -- Plucker coordinate transform that describes the relative position of this joint in the parent frame
        self.I = None # ------ Spatial inertia for this link
        self.q = 0 # --------- Joint configuration ---> These used for caching and for preserving state across timesteps
        self.qDot = 0 # ------ Joint Velocity        /
        self.qDotDot = 0 # --- Joint Acceleration  _/
        self.v = 0 # --------- Link Spatial Velocity     ---> These are the result of dynamics calculations
        self.a = 0 # --------- Link Spatial Acceleration   /
        self.f = 0 # --------- Joint Spatial Force        /
        self.tau = 0 # ------- Torque about this joint  _/
        self.graphics = None # Graphic reprsentation of the link , Contains all of the draw routines , ex: Cuboid
        # NOTE : At this time , not asking LinkSpatial to do any of the graphics setup. This is probably best for keeping the implementation
        #        as simple and display-agnostic as possible
        
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
       
"""
~~~~~~~ FIXME ~~~~~~~

ISSUE : IN THE ORIGINAL FORMATION OF 'jcalc' in [2] , THE TRANSFORMATION MATRIX 'XJ' HAS A DIFFERENT SHAPE DEPENDING ON THE JOINT TYPE
        SPECIFIED. THIS SEEMS INCONSISTENT AND AT THIS POINT IT IS NOT COMPLETELY CLEAR IF THIS SHAPE DIFFERENCE IS CARRIED THROUGHOUT THE
        IMPLEMENTATION.
        
[Y] Make the transform available in both homogeneous and spatial forms 
[ ] Test until until advantages and drawbacks of differing sizes become clear
"""
# TODO : TEST THIS
def joint_xform( pitch , q ): # Featherstone: jcalc
    """ Return the joint transform and subspace matrix for a joint with 'pitch' and joint variable 'q' """
    # See page 135 of [3] for the homogeneous transformations for each type
    if eq( pitch , 0.0 ): # Revolute Joint : Implements pure rotation 
        # XJ  = z_rot( q ) # Returns 3x3 matrix 
        E = z_rot( q ); r = [ 0 , 0 , 0 ]
        s_i = [ 0 , 0 , 1 , 0 , 0 , 0 ]
        XJ_s = spatial_xfrom( E , r )
        XJ_h = homog_xfrom( E , r )
    elif pitch == infty: # Prismatic Joint : Implements pure translation
        # XJ  = xlt( [ 0 , 0 , q ] ) # Returns 6x6 matrix
        E = [ [ 1 , 0 , 0 ] , 
              [ 0 , 1 , 0 ] , 
              [ 0 , 0 , 1 ] ]
        r = [ 0 , 0 , q ]
        s_i = [ 0 , 0 , 0 , 0 , 0 , 1 ]
        XJ_s = spatial_xfrom( E , r )
        XJ_h = homog_xfrom( E , r )
    else: #                Helical Joint   : Implements a screwing motion
        # XJ  = np.dot( z_rot( q ) , xlt( [ 0 , 0 , q * pitch ] ) ) # FIXME : ValueError: shapes (3,3) and (6,6) not aligned: 3 (dim 1) != 6 (dim 0)
        E = z_rot( q ); r = [ 0 , 0 , pitch * q ]
        s_i = [ 0 , 0 , 1 , 0 , 0 , pitch ]
        XJ_s = spatial_xfrom( E , r )
        XJ_h = homog_xfrom( E , r )
    return XJ_s , s_i , XJ_h
    #      ^,           ^-- May need this?
    #       `-- Assume Featherstone intends this to be XJ in Figure 4 of [2]
    
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
    # NOTE: This function assumes that every link between 'bodyIndex' and the root has 'xform' set
    X_tot = np.eye(6) # Total transform , the returned value # Base case: No links , Unity xform
    body = model.links[ bodyIndex ] # Fetch the link by index
    while body: # While the reference 'body' points to a link object
        [ XJ_s , s_i , XJ_h ] = joint_xform( body.pitch , q[ bodyIndex ] ) # Calculate the joint transform given the current joint config
        print "DEBUG: " , X_tot
        print "DEBUG: " , XJ_s
        print "DEBUG: " , body.xform
        X_tot = np_dot( X_tot , XJ_s , body.xform ) # Apply the joint transform and body transform to the accumulated transform
        body = body.parent # This will become 'None' after the root link has been processed
    return X_tot # After the root has been processed , there are no more transformations to perform , return
        
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

# == Main ==================================================================================================================================

if __name__ == "__main__":
    pass

# == End Main ==============================================================================================================================
    

# === References ===
"""
[1] Featherstone, Roy. "A beginner's guide to 6-d vectors (part 1)." IEEE robotics & automation magazine 17.3 (2010): 83-94.
[2] Featherstone, Roy. "A beginner's guide to 6-D vectors (part 2)[tutorial]." IEEE robotics & automation magazine 17.4 (2010): 88-99.
[3] Featherstone, Roy. "Robot dynamics algorithms." (1984).
"""
# === End Ref ===
