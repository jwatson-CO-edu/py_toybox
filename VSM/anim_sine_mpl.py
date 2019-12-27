#!/usr/bin/env python

# Animation Example
# URL : https://stackoverflow.com/a/15724978/893511
from math import floor , pi , cos
import numpy as np
import time
import matplotlib
# matplotlib.use('GTKAgg')
from matplotlib import pyplot as plt

class HeartRate: # <<< MH
    """ Sleeps for a time such that the period between calls to sleep results in a frequency not greater than the specified 'Hz' """
    def __init__( self , Hz ):
        """ Create a rate object with a Do-Not-Exceed frequency in 'Hz' """
        self.period = 1.0 / Hz; # Set the period as the inverse of the frequency , hearbeat will not exceed 'Hz' , but can be lower
        self.last = time.time()
    def sleep( self ):
        """ Sleep for a time so that the frequency is not exceeded """
        elapsed = time.time() - self.last
        if elapsed < self.period:
            time.sleep( self.period - elapsed )
        self.last = time.time()


fig , ax = plt.subplots(1, 1)
ax.set_aspect( 'equal' )
ax.set_xlim(  0 , 6 )
ax.set_ylim( -1 , 1 )
plt.show( False )
plt.draw()

rate = HeartRate( 30 )

# cache the background
background = fig.canvas.copy_from_bbox( ax.bbox )



timeStep = 0.05

# Init data
t = list( np.linspace( 0 , 6 , int( floor( 6 / timeStep ) ) ) )
X = [ cos( item ) for item in t ]
N = 1000

points = ax.plot( t , X )[0]

for i in xrange( N ):
    
    # 1. Get next datapoint
    t = t[1:] + [ t[-1] + timeStep ]
    X = X[1:] + [ cos( t[-1] ) ]
    
    ax.set_xlim( t[0] , t[-1] )
    
    # update the xy data
    points.set_data( t , X )    
    
    # restore background
    fig.canvas.restore_region( background )

    # redraw just the points
    ax.draw_artist( points )

    # fill in the axes rectangle
    fig.canvas.blit( ax.bbox )
    
    # Wait sleep until next frame
    rate.sleep()

plt.close( fig )