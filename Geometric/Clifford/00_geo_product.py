########## INIT ###################################################################################
import numpy as np
from scipy.special import comb



########## UTIL FUNCTIONS #########################################################################

def count_combos( dim ):
    """ Count the number of combinations we can pick from dim """
    count = []
    for i in range( 1, dim ):
        count.append( int( comb( dim, i ) ) )
    count.append(1) # n choose n = 1
    return count

def accum_elems( numLst ):
    total  = 0
    rtnLst = []
    for num in numLst:
        total += num
        rtnLst.append( total )
    return rtnLst



########## Composite ##############################################################################

class Mvec:
    """ Represents a Clifford multivector [ e1, e2, e3, ..., e12, e13, e23, ..., e123, ... ] """
    
    def __init__( self, realDim = 3 ):
        """ Build a list to hold all the parts of a clifford composite """
        self.rDim     = realDim
        self.partLims = count_combos( realDim )
        self.blades   = [None for i in range( sum( self.partLims ) )]
        self.partLims = accum_elems( self.partLims )
        self.bladNams = self.get_blade_labels()

    def get_blade_labels( self ):
        """  Create labels e1, e2, e3, ... """
        dimInt = [ i+1 for i in range( self.rDim ) ]
        return [ 'e'+str( elem ) for elem in dimInt ]

    def __repr__( self ):
        """ Print the multivector """
        rtnStr = '[ '
        for i in range( self.rDim ):
            rtnStr += str( self.blades[i] ) + '*' + self.bladNams[i] + ', '
        rtnStr += ']'
        return rtnStr



##### Composite Operations #####

def wedge( cmp1, cmp2 ):
    # FIXME: START HERE
    # FIXME: WEDGE VECTORS
    # FIXME: WEDGE HIGHER VECTORS
    pass