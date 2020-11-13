#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Template Version: 2020-02-07

__progname__ = "ships_00.py"
__author__   = "James Watson"
__version__  = "2020.11"
__desc__     = "Display and control of 3D sprites in vpython"

"""  
~~~ DEV PLAN ~~~
[ ] Adapt `Stinger` to inherit `VP_CompositeGeo`
[ ] ITEM2
"""

########## Init Environment #######################################################################
# ~~~ Prepare Paths ~~~
import sys, os.path
SOURCEDIR = os.path.dirname( os.path.abspath( __file__ ) ) # URL, dir containing source file: http://stackoverflow.com/a/7783326
PARENTDIR = os.path.dirname( SOURCEDIR )
#GRANDPRNT = os.path.dirname( PARENTDIR )
sys.path.insert( 0 , SOURCEDIR ) 
sys.path.insert( 0 , PARENTDIR ) # Might need this to fetch a lib in a parent directory


# ~~~ Imports ~~~
# ~~ Standard ~~
# ~~ Special ~~
import vpython 
from vpython import *
from numpy import sqrt, cos, sin, pi
import numpy as np
from marchhare.Vector import vec_unit
# ~~ Local ~~
#import marchhare
#import marchhare.VectorMath.HomogXforms
from marchhare.VectorMath.HomogXforms import set_position , pose_from_position_bases , position_bases_from_pose



########## Helper Functions #######################################################################

def vp_vec_to_np_arr( vpVec ):
    """ Convert a vpython vector to a numpy array """
    return np.array( [ vpVec.x , vpVec.y , vpVec.z ] )

def vp_vectors_to_np_arrays( *vpVecs ):
    rtnLst = []
    for vec in vpVecs:
        rtnLst.append( vp_vec_to_np_arr( vec ) )
    return rtnLst

def np_arr_to_vp_vec( npArr ):
    """ Convert a numpy array to a vpython vector """
    return vec( npArr[0] , npArr[1] , npArr[2] )

def np_arrays_to_vp_vectors( *npArrs ):
    rtnLst = []
    for arr in npArrs:
        rtnLst.append( np_arr_to_vp_vec( arr ) )
    return rtnLst

def vp_bases_from_np_homog( homogPose ):
    """ Extract 3 vpython basis vectors from numpy homogeneous coordinates """
    [ positn , xBasis , yBasis , zBasis ] = np_arrays_to_vp_vectors( *( position_bases_from_pose( homogPose ) ) )
    return positn , xBasis , yBasis , zBasis

########## Classes ################################################################################

class VP_Kit:
    clr_lgt_blue   = vec( 69/255, 118/255, 255/255 )
    clr_lgt_yellow = vec( 1.0 , 1.0 , 0.0 )


class VP_Sprite( vpython.compound ):
    """ vpython drawable """
    
    def __init__( self , name = "VP_Object" ):
        """ Init geometry """
        super().__init__( self.get_geometry() )
        self.name = name    
        self.pose = self.get_geo_pose()
    
    def get_geometry( self ):
        """ Get the drawable geometry """
        return [ box() ]
    
    def get_geo_pose( self ):
        """ Get the geo translation/orientation vectors and convert them into a homogeneous pose """
        # Assume that the `axis` is Z and the `up` is Y. That is, forward is +Z in the ship's own frame
        #print( self.geo.axis , self.geo.up )
        zBasis = vec_unit( vp_vec_to_np_arr( self.axis ) )
        yBasis = vec_unit( vp_vec_to_np_arr( self.up ) )
        xBasis = np.cross( yBasis , zBasis )
        posn   = vp_vec_to_np_arr( self.pos )
        return pose_from_position_bases( posn , xBasis , yBasis , zBasis )    
    
    
class Origin( VP_Sprite ):
    """ Graphical representation of pose bases """
    
    def __init__( self , homogPose = np.eye(4) , scale = 1.0 ):
        """ Set size and fetch geo """
        self.scale = scale
        super().__init__( name = "Origin" )
    
    def get_geometry( self ):
        """ Get the drawable geometry """
        return [
            arrow(
                pos        = vector( 0.0        , 0.0 , 0.0 ) ,
                axis       = vector( self.scale , 0.0 , 0.0 ) ,
                color      = vector( 1.0        , 0.0 , 0.0 ) ,
                shaftwidth = self.scale/10.0
            ) ,
            arrow(
                pos        = vector( 0.0 , 0.0        , 0.0 ) ,
                axis       = vector( 0.0 , self.scale , 0.0 ) ,
                color      = vector( 0.0 , 1.0        , 0.0 ) ,
                shaftwidth = self.scale/10.0
            ) ,
            arrow(
                pos        = vector( 0.0 , 0.0 , 0.0        ) ,
                axis       = vector( 0.0 , 0.0 , self.scale ) ,
                color      = VP_Kit.clr_lgt_blue              ,
                shaftwidth = self.scale/10.0
            ) ,              
        ]    


class Stinger( VP_Sprite ):
    """ Represents a small craft with high maneuverability and atmospheric capability """
    
    def __init__( self  ):
        super().__init__( name = "Stinger" )
        print( "About to rotate ..." , end=" " )
        self.rotate( angle = -pi/2.0 , axis=vector(1.0,0.0,0.0) )
        self.rotate( angle = -pi     , axis=vector(0.0,1.0,0.0) )        
        print( "Rotated!" )        
        attach_trail( 
            self ,
            retain      = 20 ,
            trail_color = VP_Kit.clr_lgt_yellow
        )
        
    def get_geometry( self ):
        return [
            # Front fusilage
            cone( axis = vector( 0 , 0 , 8 ) , 
                  radius = 3.0 , 
                  color = shipGreen ),
            # Rear fusilage      
            cone( axis = vector( 0 , 0 , -4 ) , 
                  radius = 3.0 , 
                  color = shipGreen ),
            # Top Fin
            triangle(
                v0=vertex( pos=vec(0,0,0) , color = shipOrange ),
                v1=vertex( pos=vec(0,0,8) , color = shipOrange ),
                v2=vertex( pos=vec(0,6,-4) , color = shipOrange ) , 
                color = vector(106/255, 196/255, 124/255) 
            ),
            # Left Fin
            triangle(
                v0=vertex( pos=vec(0,0,0) , color = shipBlue ),
                v1=vertex( pos=vec(0,0,8) , color = shipBlue ),
                v2=vertex( pos=vec(-6,-6,-4) , color = shipBlue ) , 
                color = vector(106/255, 196/255, 124/255) 
            ),
            # Right Fin
            triangle(
                v0=vertex( pos=vec(0,0,0) , color = shipBlue ),
                v1=vertex( pos=vec(0,0,8) , color = shipBlue ),
                v2=vertex( pos=vec(+6,-6,-4) , color = shipBlue ) , 
                color = vector(106/255, 196/255, 124/255) 
            ),
        ]

########## Main Program ###########################################################################

### Vars ###

sqrt2 = sqrt(2)

shipGreen  = vec( 0.0 , 1.0 , 0.0 ) #vector(106/255, 196/255, 124/255)
shipBlue   = VP_Kit.clr_lgt_blue #vector(106/255, 124/255 , 196/255)
shipOrange = vec( 1.0 , 0.0 , 0.0 ) #vector(255/255, 148/255, 54/255)
BGcolor    = vec( 0.0 , 0.0 , 0.0 ) #vec(48/255, 8/255, 8/255)
trailColor = vec( 1.0 , 1.0 , 0.0 ) #vector( 255/255, 244/255, 25/255 )

#print( type( compound([box()]) ) )

if __name__ == "__main__" and 1:
    print( __progname__  , 'by' , __author__ , ', Version:' , __version__ )
    termArgs = sys.argv[1:] # Terminal arguments , if they exist

    # Setup
    
    scene.width      = 800
    scene.height     = 800
    scene.background = BGcolor

    orbitRad = 60.0
    theta    =  0.0
    FPS      = 50
    angSpeed = 0.0625/4.0

    ship = Stinger()
    
    print( "Ship Pose:\n" , ship.get_geo_pose() )
    
    orgn = Origin( scale = 20.0 )
    
    while 1:
        rate( FPS )
        ship.rotate( angle = angSpeed , axis=vector(0.0,0.0,1.0) )
        theta += angSpeed
        Xs = orbitRad * cos( theta )
        Ys = orbitRad * sin( theta )
        ship.pos = vec( Xs , Ys , 0.0 )
        #print( ".", end="" )
