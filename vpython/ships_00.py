#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Template Version: 2020-02-07

__progname__ = "PROGRAM_NAME.py"
__author__   = "James Watson"
__version__  = "YYYY.MM"
__desc__     = "A_ONE_LINE_DESCRIPTION_OF_THE_FILE"

"""  
~~~ DEV PLAN ~~~
[ ] ITEM1
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

class Origin:
    """ Graphical representation of pose bases """
    
    def __init__( self , homogPose , scale ):
        pass

class Starship:
    """ Represents a star-craft in a simulation """
    
    def __init__( self , name = "Starship" ):
        """ Init the bare minimum for a starship object """
        self.geo  = None
        self.name = name
        self.pose = np.eye(4)
        
    def load_geo_pose( self ):
        """ Get the geo translation/orientation vectors and convert them into a homogeneous pose """
        # Assume that the `axis` is Z and the `up` is Y. That is, forward is +Z in the ship's own frame
        #print( self.geo.axis , self.geo.up )
        zBasis = vec_unit( vp_vec_to_np_arr( self.geo.axis ) )
        yBasis = vec_unit( vp_vec_to_np_arr( self.geo.up ) )
        xBasis = np.cross( yBasis , zBasis )
        posn   = vp_vec_to_np_arr( self.geo.pos )
        #print( posn , xBasis , yBasis , zBasis )
        self.pose = pose_from_position_bases( posn , xBasis , yBasis , zBasis )
        
    
class Stinger( Starship ):
    """ Represents a small craft with high maneuverability and atmospheric capability """
    def __init__( self , name = "Stinger" ):
        super().__init__( name )
        self.geo = compound( [
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
        ],make_trail = True, retain = 20, trail_color = trailColor )

########## Main Program ###########################################################################

### Vars ###

sqrt2 = sqrt(2)

shipGreen  = vec( 0.0 , 1.0 , 0.0 ) #vector(106/255, 196/255, 124/255)
shipBlue   = vec( 69/255, 118/255, 255/255 ) #vector(106/255, 124/255 , 196/255)
shipOrange = vec( 1.0 , 0.0 , 0.0 ) #vector(255/255, 148/255, 54/255)
BGcolor    = vec( 0.0 , 0.0 , 0.0 ) #vec(48/255, 8/255, 8/255)
trailColor = vec( 1.0 , 1.0 , 0.0 ) #vector( 255/255, 244/255, 25/255 )

if __name__ == "__main__" and 0:
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
    
    ship.geo.rotate( angle = -pi/2.0 , axis=vector(1.0,0.0,0.0) )
    
    ship.load_geo_pose()
    
    while 1:
        rate( FPS )
        ship.geo.rotate( angle = angSpeed , axis=vector(0.0,0.0,1.0) )
        theta += angSpeed
        Xs = orbitRad * cos( theta )
        Ys = orbitRad * sin( theta )
        ship.geo.pos = vec( Xs , Ys , 0.0 )
          
