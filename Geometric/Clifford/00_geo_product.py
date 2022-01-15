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
<<<<<<< HEAD
        self.e0       = None # Pure scalar part
        self.rDim     = realDim # Number of real dimensions of the space represented
        self.partLims = count_combos( realDim )
        self.blades   = [None for i in range( sum( self.partLims ) )]
        self.partLims = accum_elems( self.partLims )
        self.bladNams = self.get_blade_labels()
        self.nBlades  = len( self.bladNams )
=======
        self.rDim     = realDim # ------------------------------------- Number of Euclidean dimensions
        self.partLims = count_combos( realDim ) # --------------------- Get all blades that span the space 
        self.blades   = [None for i in range( sum( self.partLims ) )] # ------------------ Blades
        self.bDim     = len( self.blades ) # --------------------------------------------- Number of blades
        self.partLims = accum_elems( self.partLims ) # ----------------------------------- Get the boundary b/n vectors and multivectors
        self.bladNams = self.get_blade_labels() # ---------------------------------------- Generate labels
        self.bldComps = [ self.blade_name_components( bNam ) for bNam in self.bladNams ] # Blade parts, used for wedge rules
>>>>>>> 78bd581ad79400540bb8e9eefac8a01098f7d47b


    def get_blade_labels( self ):
        """  Create labels e1, e2, e3, ... """
        # FIXME: THIS IS A HACK FOR R3 AND NOT GENERAL
        dimInt = [ i+1 for i in range( self.rDim ) ]
        rtnNam = [ 'e'+str( elem ) for elem in dimInt ]
        for i in range( 0, self.rDim -1 ):
            for j in range( i+1, self.rDim ):
                rtnNam.append( 'e'+str( dimInt[i] )+str( dimInt[j] ) )
        rtnNam.append( 'e123' )
        return rtnNam


<<<<<<< HEAD
    def set_by_name( self, compDict, ignoreZero = 1 ):
=======
    @classmethod
    def blade_name_components( cls, bladeName ):
        """ Split multivectors into the vector names that span it, used for wedge rules """
        return [ 'e'+c for c in bladeName.split('e') if c ]


    def get_wedge_part( self, index ):
        """ Return a blade with wedging information """
        return ( self.blades[ index ], self.bldComps[ index ] )


    def set_by_name( self, compDict ):
>>>>>>> 78bd581ad79400540bb8e9eefac8a01098f7d47b
        """ Set the blade values by dictionary """
        for k, v in compDict.items():
            try:
                if ignoreZero and (v == 0.0):
                    pass 
                else:
                    bDex = self.bladNams.index( k )
                    self.blades[ bDex ] = v
            except ValueError:
                pass


    def get_by_name( self ):
        """ Get a dictionary of populated blades and their values """
        rtnDct = {}
        for i, b in enumerate( self.blades ):
            if b is not None:
                rtnDct[ self.bladNams[i] ] = b
        return rtnDct


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
        for i in range( self.nBlades ):
            b = self.blades[i]
            n = self.bladNams[i]
            if (b is not None) and (b != 0.0):
                rtnStr += str( b ) + '*' + str( n )
                if i < (self.nBlades - 1):
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


<<<<<<< HEAD
def count_swaps_to_order( arr ):
    """ Count the number of swaps needed to put the list in order """
    # Orignal code by Osman Mamun, https://stackoverflow.com/a/56265854
    swap_cnt = 0
    i = len(arr) - 1
    while i > 0:
        for j in range(i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swap_cnt += 1
        i -= 1
    return arr, swap_cnt


def merge_blade_names( nam1, nam2 ):
    """ Create a blade name of the appropriate order """
    # NOTE: This function assumes blade names will have only one character following 'e'
    return 'e' + nam1.replace( 'e', '' ) + nam2.replace( 'e', '' )


def wedge_blades( nam1, val1, nam2, val2 ):
    """ Wedge two blades """
    rtnNam = merge_blade_names( nam1, nam2 )
    if nam1 == nam2:
        return rtnNam, 0
    rtnVal = val1 * val2
    ordered, nSwaps = count_swaps_to_order( [int( bNam ) for bNam in rtnNam.replace( 'e', '' )] )
    if nSwaps % 2 != 0:
        rtnVal *= -1.0
    rtnNam = 'e' 
    for chr in ordered:
        rtnNam += str( chr )
    return rtnNam, rtnVal
    
=======
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

>>>>>>> 78bd581ad79400540bb8e9eefac8a01098f7d47b

def wedge( mvc1, mvc2 ):
    """ Wedge product of two multivectors """
    # The wedge product is always antisymmetric, associative, and anti-commutative.
    # Oriented length times oriented area equals oriented volume
    # (u^v)_{ij} = ( (u_i)(v_j) - (u_j)(v_i) )
<<<<<<< HEAD
    mvc1dct = mvc1.get_by_name()
    mvc2dct = mvc2.get_by_name()
    setDct  = {}
    rtnMvc  = Mvec( mvc1.rDim )

    for nam1, val1 in mvc1dct.items():
        for nam2, val2 in mvc2dct.items():
            pNam, pVal = wedge_blades( nam1, val1, nam2, val2 )
            tmpMvc = Mvec( mvc1.rDim )
            tmpMvc.set_by_name( {pNam: pVal} )
            rtnMvc = add( tmpMvc, rtnMvc )

    # print( rtnMvc.bladNams )
    # print( setDct )

    rtnMvc.set_by_name( setDct )
    return rtnMvc
=======

    # 1. Distribute
    prodParts = []
    for i in range( mvc1.bDim ):
        for j in range( mvc2.bDim ):
            prodParts.append( wedge_parts( 
                mvc1.get_wedge_part( i ), 
                mvc2.get_wedge_part( j )
            ) )

    # 2. FIXME
>>>>>>> 78bd581ad79400540bb8e9eefac8a01098f7d47b


########## Tests ###################################################################################

##### Creation Test #####

print( "Creation Test" )

mvc1 = Mvec()
mvc1.set_by_name({
    'e1': 1, 
    'e2': 2, 
    'e3': 3,
})
print( mvc1 )

print()


##### Wedge Tests #####

print( "Wedge Tests" )
mvc2 = Mvec()
mvc2.set_by_name({
    'e1': 1, 
    'e2': 2, 
    'e3': 3,
})

mvc3 = wedge( mvc1, mvc1 )
print( mvc3 )

print()