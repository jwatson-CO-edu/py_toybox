#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
SVD_and_Pseudoinverse.py , Built on Wing 101 IDE for Python 2.7
James Watson, 2018 May , Template Version: 2018-01-08
Singular Value Decomposition and its geometric meaning
URL: https://www.johndcook.com/blog/2018/05/05/svd/

Dependencies: numpy
"""
__progname__ = "Singular Value Decomposition"
__version__  = "YYYY.MM.DD"
"""  
~~~ Developmnent Plan ~~~
[Y] Generate points in a parallelepiped
[ ] Investigate SVD of points
    [Y] Get SVD of sampled points
    [ ] Test if the Right Singular Vectors are parallel to each other
[ ] Investigate Pseudoinverse of points
"""

# === Init Environment =====================================================================================================================
import sys, os.path
SOURCEDIR = os.path.dirname( os.path.abspath( __file__ ) ) # URL, dir containing source file: http://stackoverflow.com/a/7783326

# ~~~ Imports ~~~
# ~~ Standard ~~
from math import pi , sqrt
from random import random
# ~~ Special ~~
import numpy as np
# ~~ Local ~~
from marchhare.Vector import vec_unit , vec_mag , vec_angle_between

# ~~ Constants , Shortcuts , Aliases ~~
EPSILON = 1e-7
infty   = 1e309 # URL: http://stackoverflow.com/questions/1628026/python-infinity-any-caveats#comment31860436_1628026
endl    = os.linesep

# ~~ Script Signature ~~
def __prog_signature__(): return __progname__ + " , Version " + __version__ # Return a string representing program name and verions

# ___ End Init _____________________________________________________________________________________________________________________________


# === Main Application =====================================================================================================================

# = Program Functions =

def sample_in_hyperparallelepiped( N , corner , magBases ):
    """ Sample 'N' uniformly-distributed points in the 'hyperparallelepiped' with 'corner' and bases 'magBases' """
    # NOTE: 'magBases' also specifies the maximum extent beyond the corner for each dimension
    # NOTE: It is possible for the number of bases to differ from the number of dimensions
    unitBases = [ vec_unit( base ) for base in magBases ]
    baseMags  = [ vec_mag( base )  for base in magBases ]
    rtnSamples = []
    # 1. For each i
    for i in xrange( N ):
        sample = corner[:]
        # 2. For each dimension basis
        for baseDex , base in enumerate( unitBases ):
            # 3. Sample along each of the bases  &&  4. Add all the sample parts to the corner and add to the list
            sample = np.add( sample , 
                             np.multiply( base , baseMags[ baseDex ] * random() ) )
        rtnSamples.append( sample )
    return rtnSamples
# _ End Func _


# = Program Vars =



# _ End Vars _

if __name__ == "__main__":
    print __prog_signature__()
    termArgs = sys.argv[1:] # Terminal arguments , if they exist
    
    #cuboidSamples = sample_in_hyperparallelepiped( 10 , [ 0 , 0, 0 , 0 ] , [ [10,0,0,0] , [0,10,0,0] , [0,0,10,0] ] )
    #print cuboidSamples
    
    prllrppdSamples = sample_in_hyperparallelepiped( 1000 , 
                                                     [  0 ,  0 ,  0 ,  0 ] , 
                                                     [ [  2 ,  2 , 40 ,  0 ] , [ -2 , 20 , -2 , 0] , [ 10 , -2 , -2 , 0 ] ] )
    a = np.matrix( prllrppdSamples )
    u , s , vt = np.linalg.svd( a , full_matrices = True )
    v = np.transpose( vt )
    print "S = " , s , endl , "S , The influence of each Right Singular Vector in decreasing order"
    print "V = " , endl , v , endl , "V , Right Singular (column) Vectors, correspinding to the singular values S"
    # Angles between Right Singular Vectors
    v1 = np.ravel( v[0:3,0].reshape(3,1) ) 
    v2 = np.ravel( v[0:3,1].reshape(3,1) )
    v3 = np.ravel( v[0:3,2].reshape(3,1) )
    print "Angle between Column 1 and 2" , vec_angle_between( v1 , v2 ) / pi , "pi radians"
    print "Angle between Column 2 and 3" , vec_angle_between( v2 , v3 ) / pi , "pi radians"
    print "Angle between Column 3 and 1" , vec_angle_between( v3 , v1 ) / pi , "pi radians"

# ___ End Main _____________________________________________________________________________________________________________________________


# === Spare Parts ==========================================================================================================================



# ___ End Spare ____________________________________________________________________________________________________________________________