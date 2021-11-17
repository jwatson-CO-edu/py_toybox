# == Init ==

from random import random
import numpy as np
from numpy import exp , arange
from pylab import meshgrid , cm , imshow , contour , clabel , colorbar , axis , title , show

# == End Init ==


# == Helper Functions ==

def vec_random( dim ): # <<< resenv
    """ Return a random vector in R-'dim' space with coordinates in [0,1) """
    rtnVec = []
    for i in range(dim):
        rtnVec.append( random() )
    return rtnVec

def vec_mag(vec): # <<< resenv
    """ Return the magnitude of a vector """
    return np.linalg.norm(vec)

def vec_random_limits( dim , limits ): # <<< resenv
    """ Return a vector in which each element takes on a random value between 'limits[i][0]' and 'limits[i][1]' with a uniform distribution """
    rtnVec = []
    randVec = vec_random( dim )
    for i , elem in enumerate( randVec ):
        span = abs( limits[i][1] - limits[i][0] )
        rtnVec.append( elem * span + limits[i][0] )
    return rtnVec

def vec_dif_mag( vec1 , vec2 ): # TODO: ADD TO RESENV
    """ Return the magnitude of the vector difference between 'vec1' and 'vec2' """
    return vec_mag( np.subtract( vec1 , vec2 ) )

def meshgrid_map( X , Y , func ):
    """ Given 'X' and 'Y' created by 'np.meshgrid' , Return 'Z' using 'func( x , y )' , assume 'X' and 'Y' the same size and 'func' accepts scalars """
    Z = np.zeros( ( len(X) , len(X[0]) ) ) # Create a zero matrix the same size as 'X' and 'Y'
    for i in xrange( len( X ) ): # for every row in 'X' and 'Y'
        for j in xrange( len( X[0] ) ): # for every column in 'X' and 'Y'
            Z[i][j] = func( X[i][j] , Y[i][j] ) # Compute 'func( x , y )' and assign to the appropriate index of 'Z'

# == End Helper ==

graphBounds = [ [ -100 , 100 ] , [ -100 , 100 ] ]
pointBounds = [ [  -30 ,  30 ] , [  -30 ,  30 ] ]

trianglePts = [ vec_random_limits( 2 , pointBounds ) for i in xrange(3) ]
print trianglePts

def triangle_dist_func( triPoints ):
    """ Return a function that calculates the sum of the distance from point 'x','y' to all three 'triPoints' """
    
    def tri_dist( x , y ):
        """ sum of the distance from point 'x','y' to all three 'triPoints' """
        temp = [ x , y ]
        # print "temp" , temp
        return sum( [ vec_dif_mag( temp , pnt ) for pnt in trianglePts ] )
    
    return tri_dist

# the function that I'm going to plot
z_func = triangle_dist_func( trianglePts )
# z_func = lambda x , y: x+y

td = triangle_dist_func( trianglePts )
print "Triangle Distance" , td( 10 , 10 )
 
x = arange( -100.0 , 100.0 , 1 )
y = arange( -100.0 , 100.0 , 1 )
X , Y = meshgrid( x , y ) # grid of point
# Z = z_func( X , Y ) # evaluation of the function on the grid
Z = np.zeros( ( len(X) , len(X[0]) ) )

meshgrid_map( X , Y , Z , z_func )

print "Shape of X:" , X.shape # (2000, 2000)
print "Shape of Y:" , Y.shape # (2000, 2000)
print "Shape of Z:" , Z.shape # (2000, 2000)

if 1:
    im = imshow( Z , cmap = cm.RdBu ) # drawing the function
    # adding the Contour lines with labels
    cset = contour( Z , arange( -1 , 1.5 , 0.2 ) , linewidths = 2 , cmap = cm.Set2 )
    clabel( cset , inline = True , fmt = '%1.1f' , fontsize = 10 )
    colorbar( im ) # adding the colobar on the right
    # latex fashion title
    title( '$z=(1-x^2+y^3) e^{-(x^2+y^2)/2}$' )
    show()