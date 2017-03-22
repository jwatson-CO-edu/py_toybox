from random import random
from TB_Utils import *

def index_min( pList ): 
    """ Return the first index of 'pList' with the maximum numeric value """
    return pList.index( min( pList ) )

def kmeans_lloyd_1D( dataList , k , maxIter = 1000 ):
    """ Return the bounds of 'k' clusters determined by Lloyd's algorithm , return when converged or after 'maxIter' """ 
    # https://en.wikipedia.org/wiki/K-means_clustering#Standard_algorithm # NOTE: This is a standard soln that makes no optimizations 
    data = sorted( dataList )
    loBound = data[0] ; hiBound = data[-1]
    means = sorted( [ hiBound * random() for i in xrange( k ) ] )
    lastMem = [ [0] for j in xrange( k ) ]
    count = 0
    converged = False
    while ( not converged ) and ( count < maxIter ):
        members = [ [] for j in xrange( k ) ]
        # Assignment Step
        for elem in data:
            dist = [ abs( elem - mu ) for mu in means ]
            members[ index_min( dist ) ].append( elem )
        # Update step
        means = [ avg( sub ) for sub in members ]
        # Check for convergence
        if [ sum( sub ) for sub in members ] == [ sum( sub ) for sub in lastMem ]:
            converged = True
        # Save clusters
        lastMem = [ sub[:] for sub in members ]
        count += 1
    print "DEBUG , exited after" , count , "iterations"
    sortBounds = [ sorted( sub ) for sub in members ]
    return [ ( sub[0] , sub[-1] ) for sub in sortBounds ]

print kmeans_lloyd_1D( [13,14,15 , 7,8,9 , 1,2,3 ] , 3 , maxIter = 1000 )