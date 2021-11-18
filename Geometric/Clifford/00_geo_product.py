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

class Composite:
    """ Represents a Clifford object [ e1, e2, e3, ..., e12, e13, e23, ..., e123, ... ] """
    
    def __init__( self, realDim = 3 ):
        """ Build a list to hold all the parts of a clifford composite """
        self.partLims = count_combos( realDim )
        self.parts    = [None for i in range( sum( self.partLims ) )]
        self.partLims = accum_elems( self.partLims )


##### Composite Operations #####

def wedge( cmp1, cmp2 ):
    # FIXME: START HERE
    # FIXME: WEDGE VECTORS
    # FIXME: WEDGE HIGHER VECTORS
    pass