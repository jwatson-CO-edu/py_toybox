########## INIT ####################################################################################
import numpy as np
from scipy.special import comb



########## UTIL FUNCTIONS ##########################################################################

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



########## Composite ###############################################################################

class Mvec:
    """ Represents a Clifford multivector [ e1, e2, e3, ..., e12, e13, e23, ..., e123, ... ] """
    

    def __init__( self, realDim = 3 ):
        """ Build a list to hold all the parts of a clifford composite """
        self.rDim     = realDim # ------------------------------------- Number of Euclidean dimensions
        self.partLims = count_combos( realDim ) # --------------------- Get all blades that span the space 
        self.blades   = [None for i in range( sum( self.partLims ) )] # ------------------ Blades
        self.bDim     = len( self.blades ) # --------------------------------------------- Number of blades
        self.partLims = accum_elems( self.partLims ) # ----------------------------------- Get the boundary b/n vectors and multivectors
        self.bladNams = self.get_blade_labels() # ---------------------------------------- Generate labels
        self.bldComps = [ self.blade_name_components( bNam ) for bNam in self.bladNams ] # Blade parts, used for wedge rules


    def get_blade_labels( self ):
        """  Create labels e1, e2, e3, ... """
        dimInt = [ i+1 for i in range( self.rDim ) ]
        return [ 'e'+str( elem ) for elem in dimInt ]


    @classmethod
    def blade_name_components( cls, bladeName ):
        """ Split multivectors into the vector names that span it, used for wedge rules """
        return [ 'e'+c for c in bladeName.split('e') if c ]


    def get_wedge_part( self, index ):
        """ Return a blade with wedging information """
        return ( self.blades[ index ], self.bldComps[ index ] )


    def set_by_name( self, compDict ):
        """ Set the blade values by dictionary """
        for k, v in compDict.items():
            try:
                bDex = self.bladNams.index( k )
                self.blades[ bDex ] = v
            except ValueError:
                pass


    def set_value( self, value ):
        """ Set the real values of each of the blades """
        if isinstance( value, (list, np.ndarray) ):
            if len( value ) != len( self.blades ):
                raise IndexError( f"Mvec.set_value: There must be a value for each blade! There are {len(self.blades)} blades and {len(value)} given values!" ) 
            for i, v in enumerate( value ):
                self.blades[i] = v
        elif isinstance( value, dict ):
            self.set_by_name( value )
        else:
            raise ValueError( f"Mvec.set_value: must be dict, list, or numpy array got {type(value)}" ) 


    def __repr__( self ):
        """ Print the multivector """
        rtnStr = '[ '
        for i in range( self.rDim ):
            b = self.blades[i]
            n = self.bladNams[i]
            if b is not None:
                rtnStr += str( b ) + '*' + str( n )
            if i < (self.rDim - 1):
                rtnStr += ', '
        rtnStr += ']'
        return rtnStr



##### Composite Operations #####

### Addition ###

def add( mvc1, mvc2 ):
    """ Add two multivectors by element """
    resVec = Mvec( realDim = max( mvc1.rDim, mvc2.rDim ) )
    for i in range( len( mvc1.blades ) ):
        comp1 = mvc1.blades[i]
        comp2 = mvc2.blades[i]
        if (comp1 is None) and (comp2 is None):
            resVec.blades[i] = None
        elif (comp1 is not None) and (comp2 is not None):
            resVec.blades[i] = comp1 + comp2
        elif comp1 is not None:
            resVec.blades[i] = comp1
        else:
            resVec.blades[i] = comp2
    return resVec


### Wedge Product ###

def wedge_parts( prt1, prt2 ):
    """ Manage rules for wedging of two blades, `prtX` = (number, partNames) """
    (prt1Real, prt1Prts) = prt1
    (prt2Real, prt2Prts) = prt2
    part1set = set( prt1Prts )
    part2set = set( prt2Prts )
    overlap  = part1set.intersection( part2set )
    vecSpan  = part1set.union( part2set )
    if overlap:
        realPart = 0.0
    else:
        realPart = prt1Real * prt2Real
    return ( realPart, vecSpan )


def wedge( mvc1, mvc2 ):
    """ Wedge product of two multivectors """
    # The wedge product is always antisymmetric, associative, and anti-commutative.
    # Oriented length times oriented area equals oriented volume
    # (u^v)_{ij} = ( (u_i)(v_j) - (u_j)(v_i) )

    # 1. Distribute
    prodParts = []
    for i in range( mvc1.bDim ):
        for j in range( mvc2.bDim ):
            prodParts.append( wedge_parts( 
                mvc1.get_wedge_part( i ), 
                mvc2.get_wedge_part( j )
            ) )

    # 2. FIXME


########## Tests ###################################################################################
