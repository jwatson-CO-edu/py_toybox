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

[N] A. Install and switch to MARCHHARE - This will not be done , MARCHHARE is under development in an academic environment and risk of accumulating
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
[Y] 2. Implement a single joint
    |Y| 2.a. Make the center of the Cuboid settable - COMPLETE , Also corrected some errors in the vertices calculations
    ISSUE      : LINK ROTATES IN THE OPPOSITE DIRECTION FROM EXPECTED FOR POSITIVE 'q'
    RESOLUTION : Needed to do a transformation instead of a rotation
        !N! Find out what reference frame it is supposed to be transforming        
    ISSUE      : PRISMATIC JOINT TRANSFORM DOES NOT RESULT IN A TRANSLATION
    RESOLUTION : There was confusion about trying to use spatial transforms to operate on 3D vectors
        !N! Take a close look about how pure translation happens in a homogeneous transformation
        !N! Develop a spatial transformation matrix that will also cause a pure translation ( Look at DRAKE from MIT , Search below )
    ISSUE      : SOME PROBLEMS HAVE ARISEN FROM THE MISCONCEPTION THAT SPATIAL VECTORS ARE USED TO REPRESENT POSE , THEY ARE NOT. THEY ARE USED
                 TO REPRESENT MOTION AND FORCE.
    RESOLUTION : Spatial and Euclidean vector transformations are now completely separate
        !Y! Recover from the spatial / 3D mixup
            ;Y; Remove functions that were meant to use spatial transforms to operate on 3D points
            ;Y; Separate the spatial and 3D operations from the jacobian and FK operations
    |Y| 2.b. Rotate - COMPLETE
    |Y| 2.c. Translate
    |Y| 2.d. Screw - COMPLETE
    |Y| 2.e. Implement a control interface with per-joint slider , Tested with all three types of joint
    ISSUE    : TKINTER WINDOW DOES NOT PLAY NICE WITH THE PYGLET WINDOW , DOES NOT PAINT PROPERLY , BLOCKS PYGLET WHEN 'mainloop' is called
    RESOLVED : Tkinter hates being told what to do and will not tolerate being outside of the main thread of its program. Solution is to let
               Tkinter be the loop / heartbeat of the program , and not bother trying to get other loops to drive Tkinter , becuase it won't
        !Y! Try driving pyglet from tkinter instead of the other way around - THIS WAS IT
[ ] 3. Implement a Robot from Robot Intro , Forward Kinematics
    | | 3.a. Move OGL classes and functions to their own file , Move Tkinter class to its own file
    | | 3.b. Implement DH Parameters (Hollerbach)
    | | 3.c. Position
    | | 3.d. Speed
    | | 3.e. Acceleration
[ ] 4. Implement a Robot from Robot Intro , Dynamics
    | | 4.a. Gravity
    | | 4.b. Coriolis
    | | 4.c. Friction
    | | 4.d. Forward Dynamics
[ ] 5. Implement a Robot from Robot Controls , Inverse Dynamics
[ ] 6. Implement the same robot from (3.b) with DH Parameters (Hollerbach) and generalize
[ ] 7. Tools for robot arm design
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
from math import cos , sin , acos , degrees
# ~ Special ~
import numpy as np
# ~ Local ~
# localPaths = [ os.path.join( "C:" , os.sep , "Users" , "jwatson" , "Documents" , "Python Scripts" ) ] # List of paths to your custom modules
# add_valid_to_path( localPaths )

# ~~ Aliases & Shortcuts ~~
infty = float('inf') # infinity
endl  = os.linesep # - Line separator (OS Specific)

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

def concat_arr( *arrays ): 
    """ Concatenate all 'arrays' , any of which can be either a Python list or a Numpy array """
    # URL , Test if any in an iterable belongs to a certain class : https://stackoverflow.com/a/16705879
    if any( isinstance( arr , np.ndarray ) for arr in arrays ): # If any of the 'arrays' are Numpy , work for all cases , 
        if len( arrays ) == 2: # Base case 1 , simple concat    # but always returns np.ndarray
            return np.concatenate( arrays[0] , arrays[1] )  
        elif len( arrays ) > 2: # If there are more than 2 , concat the first two and recur
            return concat_arr( np.concatenate( arrays[0] , arrays[1] ) , *arrays[2:] )
        else: # Base case 2 , there is only once arg , return it
            return arrays[0]
    if len( arrays ) > 1: # else no 'arrays' are Numpy 
        rtnArr = arrays[0]
        for arr in arrays[1:]: # If there are more than one , just use addition operator in a line
            rtnArr += arr
        return rtnArr
    else: # else there was only one , return it
        return arrays[0] 
    
def enumerate_rev( L ): # URL: https://stackoverflow.com/a/529466
    """ Generator to 'enumerate' a list in the reverse order """
    for index in reversed( xrange( len( L ) ) ):
        yield index , L[ index ]    

# == End Utility ==

# === Geometry ===

# == Vector Operations ==

def vec_unit( vec ):
    """ Return a vector in the direction of 'vec' with unit length """
    return np.divide( vec , np.linalg.norm( vec ) )

vec_mag = np.linalg.norm # Alias for 'np.linalg.norm'
    

def np_dot( *args ): 
    """ Perform 'np.dot' on more than two args """
    if len( args ) > 2: # If there are more than 2 args, add the first arg to recur on remainder of args
        return np.dot( args[0] , np_dot( *args[1:] ) ) # Note the star operator is needed for recursive call, unpack to positional args
    else: # base case, there are 2 args*, use vanilla 'np.add'
        return np.dot( args[0] , args[1] ) # *NOTE: This function assumes there are at least two args, if only 1 an error will occur

# == End Vector ==

# == Trigonometry == # TODO: Check that these are in MARCHHARE

def ver( theta ):
    """ Versine , radians """
    return 1 - cos( theta )

def verd( theta ):
    """ Versine , degrees """
    return degrees( 1 - cos( theta ) )

# == End Trig ==

# == Geo 3D == # TODO: Copy all 3D geo to MARCHHARE
    
""" Page 4 of [5]
A few details are worth mentioning here. The symbols [0] and [1] denote the
zero and identity matrices, respectively, and [0] also denotes the zero vector. The
superscript A^{−T} denotes the transpose of the inverse of A, so A^{−T} means ( A^{−1} )^{T} .
"""
    
def x_rot( theta ):
    """ Return the 3x3 matrix that performs a rotation of 'theta' about the X axis """
    return [ [  1            ,  0            ,  0            ] , 
             [  0            ,  cos( theta ) ,  sin( theta ) ] , 
             [  0            , -sin( theta ) ,  cos( theta ) ] ]
    
def x_trn( theta ):
    """ Return the 3x3 matrix that performs a rotation of 'theta' about the X axis """
    return [ [  1            ,  0            ,  0            ] , 
             [  0            ,  cos( theta ) , -sin( theta ) ] , 
             [  0            ,  sin( theta ) ,  cos( theta ) ] ]

    
def y_rot( theta ):
    """ Return the 3x3 matrix that performs a rotation of 'theta' about the Y axis """
    return [ [  cos( theta ) ,  0            , -sin( theta ) ] , 
             [  0            ,  1            ,  0            ] , 
             [  sin( theta ) ,  0            ,  cos( theta ) ] ]
    
def z_rot( theta ):
    """ Return the 3x3 matrix that performs a rotation of 'theta' about the Z axis """
    return [ [  cos( theta ) ,  sin( theta ) ,  0            ] , 
             [ -sin( theta ) ,  cos( theta ) ,  0            ] , 
             [  0            ,  0            ,  1            ] ]
    
def z_trn( theta ):
    """ Return the 3x3 matrix that performs a rotational transformation of 'theta' about the Z axis """
    return [ [  cos( theta ) , -sin( theta ) ,  0            ] , 
             [  sin( theta ) ,  cos( theta ) ,  0            ] , 
             [  0            ,  0            ,  1            ] ]
    
def rot_matx_ang_axs( theta , k  ):
    """ Return the 3x3 rotation matrix for the given angle 'theta' and axis 'k' """
    k = vec_unit( k )
    return [ [ k[0]*k[0]*ver(theta) + cos(theta)      , k[0]*k[1]*ver(theta) - k[2]*sin(theta) , k[0]*k[2]*ver(theta) + k[1]*sin(theta) ] , 
             [ k[1]*k[0]*ver(theta) + k[2]*sin(theta) , k[1]*k[1]*ver(theta) + cos(theta)      , k[1]*k[2]*ver(theta) - k[0]*sin(theta) ] , 
             [ k[2]*k[0]*ver(theta) - k[1]*sin(theta) , k[2]*k[1]*ver(theta) + k[0]*sin(theta) , k[2]*k[2]*ver(theta) + cos(theta)      ] ]

def ang_axs_from_rot_matx( R ):
    """ Return the angle 'theta' and axis 'k' for the given 3x3 rotation matrix 'R' """
    # NOTE : This function returns only one solution out of 2 possible , these solution are equivalen with opposite
    theta = acos( ( np.trace( R ) - 1.0 ) / 2.0 )
    k = np.multiply( [ R[2][1] - R[1][2] , 
                       R[0][2] - R[2][0] , 
                       R[1][0] - R[0][1] ] , 0.5 * sin( theta ) )
    return theta , k
    
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

def skew_sym_cross( vecR ):
    """ Return the skew symmetic matrix for the equivalent cross operation: [r_cross][v] = cross( r , v ) """
    return [ [  0       , -vecR[2] ,  vecR[1] ] , 
             [  vecR[2] ,  0       , -vecR[0] ] ,
             [ -vecR[1] ,  vecR[0] ,  0       ] ]

def homog_xfrom( E , r ): 
    """ Return the combination of rotation matrix 'E' and displacement vector 'r' as a 4x4 homogeneous transformation matrix """
    return np.vstack( ( np.hstack( (  E                              , [ [ r[0] ] , [ r[1] ] , [ r[2] ] ]  ) ) ,
                        np.hstack( (  [ 0 , 0 , 0 ]                  , [ 1 ]                               ) ) ) )

def sp_trn_xfrm_mtn( r ): # (2.21) of [5]
    """ Return the spatial transformation of a motion vector that corresponds to a translation of R3 vector 'r' """
    return np.vstack( (  np.hstack( (  np.eye( 3 )                             , np.zeros( ( 3 , 3 ) )  ) ) , 
                         np.hstack( (  np.multiply( skew_sym_cross( r ) , -1 ) , np.eye( 3 )            ) ) ) )

def sp_trn_xfrm_frc( r ): # (2.22) of [5]
    """ Return the spatial transformation of a velocity vector that corresponds to a translation of R3 vector 'r' """
    return np.vstack( (  np.hstack( (  np.eye( 3 )           , np.multiply( skew_sym_cross( r ) , -1 )  ) ) , 
                         np.hstack( (  np.zeros( ( 3 , 3 ) ) , np.eye( 3 )                              ) ) ) )

def sp_rot_xfrm( E ): # Eq. (2.19) and (2.20) in [5]
    """ Return the spatial transformation that corresponds to a 3x3 rotation matrix 'E' """
    # NOTE: Transform is the same for both velocity and force vectors , [5]
    return np.vstack( (  np.hstack( (  E                     , np.zeros( ( 3 , 3 ) )  ) ) , 
                         np.hstack( (  np.zeros( ( 3 , 3 ) ) , E                      ) ) ) )    

def spatl_xfrm_mtn( E , r ): # (2.24) of [5]
    """ Return the spatial motion vector transformation that corresponds to a translation by 'r' followed by rotation by 'E' """
    return np.dot( sp_rot_xfrm( E ) , sp_trn_xfrm_mtn( r ) )

def spatl_xfrm_frc( E , r ): # (2.25) of [5]
    """ Return the spatial force vector transformation that corresponds to a translation by 'r' followed by rotation by 'E' """
    return np.dot( sp_rot_xfrm( E ) , sp_trn_xfrm_frc( r ) )
    
# == End 3D ==

# === End Geometry ===

# == 3D Vector Arithmetic ==



# == End 3D Vector ==


# == Plucker Coordinates and Operations ==

# FIXME : THERE ARE DIFFERENT TRANSFORMS FOR TRANSLATION AND ROTATION!

def xlt( r ):
    """ Translational transform of Plucker coordinates """
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


# = Spatial <--> Cartesian =
    
# [6] Part V , Page 4
    
# _ End Sptl <--> Cart _

# == End Plucker ==


# == Robot Model ==

# TODO: Fill in the details of the inverse dynamics function as the article progresses

# = Model Classes & Functions =

class LinkSpatial:
    """ Represents a rigid link and the associated joint using spatial coordinates """
    def __init__( self , pName , pPitch , E_xfrm = None , r_xfrm = None ):
        """ Rigid link struct """
        print "DEBUG LinkSpatial.__init__" , endl , "E_xfrm" , endl , E_xfrm , endl , "r_xfrm" , endl , r_xfrm
        self.name = pName # ------------------------------- String that uniquely identifies the link
        self.pitch = pPitch # ----------------------------- Describes the pitch (and therefore the type) of the associated joint
        self.parent = None # ------------------------------ Reference to the parent link to which this link is attached
        self.children = [] # -----------------------------  List of child links
        self.linkIndex = 0 # ------------------------------ Index of link in q 
        self.xform = homog_xfrom( E_xfrm , r_xfrm ) # ----- Homogeneous coordinate transform -> position of this joint in the parent frame
        self.xSptlMtn = spatl_xfrm_mtn( E_xfrm , r_xfrm ) # Spatial Motion Xform -> position of this joint in the parent frame
        self.xSptlFrc = spatl_xfrm_frc( E_xfrm , r_xfrm ) # Spatial Force Xform -> position of this joint in the parent frame
        self.pose = np.eye( 4 ) # ------------------------- Cached homogeneous transform that represents the pose of the link
        self.poseReady = False # -------------------------- Flag , False if the cached version is old , True if the cached pose is ready for use
        self.I = None # ----------------------------------- Spatial inertia for this link
        self.q = 0 # -------------------------------------- Joint configuration ---> These used for caching and for preserving state across timesteps
        self.qDot = 0 # ----------------------------------- Joint Velocity        /
        self.qDotDot = 0 # -------------------------------- Joint Acceleration  _/
        self.v = 0 # -------------------------------------- Link Spatial Velocity     ---> These are the result of dynamics calculations
        self.a = 0 # -------------------------------------- Link Spatial Acceleration   /
        self.f = 0 # -------------------------------------- Joint Spatial Force        /
        self.tau = 0 # ------------------------------------ Torque about this joint  _/
        self.graphics = None # ---------------------------- Graphic reprsentation of the link , Contains all of the draw routines , ex: Cuboid
        # NOTE : At this time , not asking LinkSpatial to do any of the graphics setup. This is probably best for keeping the implementation
        #        as simple and display-agnostic as possible
        
    def calc_link_I( self , mass , COM , I_COM ):
        """ Calculate and set the link rotational inertial about the joint """
        cX = cross_motn_matx( COM )
        self.I = np.vstack( ( np.hstack( ( I_COM - np.multiply( mass , np.dot( cX , cX ) ) , np.multiply( mass , cX )        ) ) , 
                              np.hstack( ( np.multiply( -mass , cX )                       , np.multiply( mass , np.eye(3) ) ) ) ) )
        
    def calc_xforms( self , E , r ):
        """ Given 3D transform of translation 'r' followed by rotation 'E' set equivalent homogeneous , 6D velocity , and 6D force transforms """
        # FIXME : START HERE

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
                    # print "DEBUG:" , "Found link" , lnk.name
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
        if not len( q ) == len( self.links ):
            raise IndexError( "LinkModel.set_q: 'len(q)' must equal the number of links!" )
        for lnkDex , link in enumerate( self.links ):
            link.q = q[ lnkDex ]
            
    def get_link_names( self ):
        """ Return a list of all the link names """
        return [ lnk.name for lnk in self.links ]
       
"""
~~~~~~~ FIXME ~~~~~~~

ISSUE : IN THE ORIGINAL FORMATION OF 'jcalc' in [2] , THE TRANSFORMATION MATRIX 'XJ' HAS A DIFFERENT SHAPE DEPENDING ON THE JOINT TYPE
        SPECIFIED. THIS SEEMS INCONSISTENT AND AT THIS POINT IT IS NOT COMPLETELY CLEAR IF THIS SHAPE DIFFERENCE IS CARRIED THROUGHOUT THE
        IMPLEMENTATION.
        
[Y] Make the transform available in both homogeneous and spatial forms 
[ ] Test until until advantages and drawbacks of differing sizes become clear
"""
def joint_spatl( pitch , q ): # Featherstone: jcalc
    """ Return the joint spatial coordinate transform and subspace matrix for a joint with 'pitch' and joint variable 'q' """
    # NOTE : This function is for transform coordinate bases , not positions
    
    if eq( pitch , 0.0 ): # Revolute Joint : Implements pure rotation 
        E = z_trn( q ); r = [ 0 , 0 , 0 ]
        s_i = [ 0 , 0 , 1 , 0 , 0 , 0 ]
        XJ_s = sp_rot_xfrm( E )
        
    elif pitch == infty: #- Prismatic Joint : Implements pure translation
        E = np.eye( 3 ); r = [ 0 , 0 , q ]
        s_i = [ 0 , 0 , 0 , 0 , 0 , 1 ]
        XJ_s = sp_trn_xfrm_mtn( r )
        
    else: # --------------- Helical Joint   : Implements a screwing motion
        E = z_trn( q ); r = [ 0 , 0 , pitch * q ]
        s_i = [ 0 , 0 , 1 , 0 , 0 , pitch ]
        XJ_s = np.dot( sp_rot_xfrm( E ) , sp_trn_xfrm_mtn( r ) )
    
    return XJ_s , s_i 
    #      ^-- Assume Featherstone intends this to be XJ in Figure 4 of [2]

def joint_homog( pitch , q ): 
    """ Return the joint homogeneous transform matrix for a joint with 'pitch' and joint variable 'q' """
    # See page 135 of [3] for the homogeneous transformations for each type
    
    if eq( pitch , 0.0 ): # Revolute Joint : Implements pure rotation 
        E = z_trn( q )
        r = [ 0 , 0 , 0 ]
    
    elif pitch == infty: #- Prismatic Joint : Implements pure translation
        E = np.eye( 3 )
        r = [ 0 , 0 , q ]

    else: # --------------- Helical Joint   : Implements a screwing motion
        E = z_trn( q )
        r = [ 0 , 0 , pitch * q ]

    return homog_xfrom( E , r )
    
# = End Classes =

# = Spatial Dynamics =

def inverse_dynamics( model ): # , q , qDot , qDotDot ):
    """ Compute the inverse dynamics from the model with the Recursive Newton-Euler Algo """ 
    # NOTE: This function assumes that 'model' has 'q' , 'qDot' , 'qDotDot' set for joints
    # ~ Forward Pass ~
    for lnkDex , link in enumerate( model.links ): # For every link in the model , do
#        [ XJ , s_i ] = joint_xform( link.pitch , link.q ) # (FS: 'jcalc') calc the joint transformation and freedom (selection) matrix
        [ XJ , s_i ] = joint_spatl( link.pitch , link.q ) # (FS: 'jcalc') calc the joint transformation and freedom (selection) matrix
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

def FK( model , bodyIndex , q ): # ( Featherstone: bodypos ) # This is modified from 'bodypos' and operates on homogeneous transforms instead
    """ Compute the pose ( as a homogeneous transform ) for a given config 'q' """
    # NOTE: This function does not depend on the presently stored q state , returned pose depends only on given 'q'
    # NOTE: This function assumes that every link between 'bodyIndex' and the root has 'xform' set
    X_tot = []
    body = model.links[ bodyIndex ] # Fetch the link by index
    while body: # While the reference 'body' points to a link object
        # XJ_h = 
        temp = [ body.xform , joint_homog( body.pitch , q[ body.linkIndex ] ) ]
        temp.extend( X_tot ) # Prepend the transforms associated with the parent joint
        X_tot = temp
        body = body.parent # This will become 'None' after the root link has been processed
    return np_dot( *X_tot ) # After the root has been processed , there are no more transformations to perform , return
        
def jacobn_manip( model , bodyIndex , q ): # ( Featherstone: bodyJac )
    """ Compute the manipulator jacobian up to the specified link in the tree """
    # NOTE: This function does not depend on the presently stored q state , returned pose depends only on given 'q'
    e = np.zeros( model.N ) # Selector vector
    body = model.links[ bodyIndex ] # Fetch the link by index
    while body: # Build the selector vector
        e[ body.linkIndex ] = 1 # Place a 1 at the index of every link between 'body' and the root
        body = body.parent # This will become 'None' after the root link has been processed
    J = np.zeros( ( 6 , model.N ) ) # Matrix for the Jacobian
    # Xa = np.zeros( model.N ) # An array of transforms
    # Xa = np.zeros( ( model.N , model.N ) ) # An array of transforms
    Xa =  [ None ] * model.N # An array of transforms
    for lnkDex , link in enumerate( model.links ): # For each link in the model
        if e[ lnkDex ]: # If the link is in the chain from the selected body to the root
            # print "DEBUG , jacobn_manip : In link" , lnkDex
            # [ XJ , s_i ] = joint_xform( link.pitch , q[ lnkDex ] )
            [ XJ , s_i ] = joint_spatl( link.pitch , q[ lnkDex ] )
#            print "DEBUG , jacobn_manip : XJ" , endl , XJ
#            print "DEBUG , jacobn_manip : link.xSptlMtn" , endl , link.xSptlMtn
#            print "DEBUG , jacobn_manip : np.dot( XJ , link.xSptlMtn )" , endl , np.dot( XJ , link.xSptlMtn )
            Xa[ lnkDex ] = np.dot( XJ , link.xSptlMtn )
            # print "DEBUG , jacobn_manip : Xa[" , lnkDex , "]" , Xa[ lnkDex ]
            if link.parent:
                Xa[ lnkDex ] = np.dot( Xa[ lnkDex ] , Xa[ link.parent.linkIndex ] )
            x , resid , rank , s = np.linalg.lstsq( Xa[ lnkDex ] , s_i ) # Solving what exactly?
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

# __ End Main ______________________________________________________________________________________________________________________________
    

# === References ===
"""
[1] Featherstone, Roy. "A beginner's guide to 6-D vectors (part 1)." IEEE robotics & automation magazine 17.3 (2010): 83-94.
[2] Featherstone, Roy. "A beginner's guide to 6-D vectors (part 2)[tutorial]." IEEE robotics & automation magazine 17.4 (2010): 88-99.
[3] Featherstone, Roy. "Robot dynamics algorithms." (1984).
[4] Ralf Grosse-Kunstleve. "scitbx_rigid_body_essence Python Library" ,Lawrence Berkeley National Laboratory , Computational Crystallography Initiative
    http://cctbx.sourceforge.net/scitbx_rigid_body_essence/
[5] Featherstone, Roy. Rigid body dynamics algorithms. Springer, 2008.
[6] Featherstone, Roy. "Plucker basis vectors." In Robotics and Automation, 2006. ICRA 2006. Proceedings 2006 IEEE International Conference on, pp. 1892-1897. IEEE, 2006.
[7] Featherstone, Roy. "A Short Course on Spatial Vector Algebra: The Easy Way to do Rigid Body Dynamics", Dept. Information Engineering, RSISE, The Autralian National University
"""
# ___ End Ref ___
