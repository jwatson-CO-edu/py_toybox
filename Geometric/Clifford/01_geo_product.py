"""
FIXME: https://www.youtube.com/watch?v=jePGhow3mlA&list=PLxo3PbygE0PLdFFy_2b02JAaUsleFW8py&index=7
t = 13:41
"""


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
    """ Return a list that is the elementwise running sum of `numList` """
    total  = 0
    rtnLst = []
    for num in numLst:
        total += num
        rtnLst.append( total )
    return rtnLst


def ordered_combos( lst, accumList = None, prefix = None, maxLen = None ):
    """ Return all combos of elements in `lst` in lexigraphic order (according to `lst`) """
    ## Init ##
    # Length of current sublist
    N = len( lst )
    # Establish length of symbol lexicon at depth 0
    if (maxLen is None) and (prefix is None):
        maxLen = N
    # Establish or link to the list of accumulated combos
    if not lst: 
        return []
    if accumList is None:
        rtnLst = []
    else:
        rtnLst = accumList
    ## Cases ##
    for i, elem in enumerate( lst ):
        # Base Case, End of original list: Return empty list
        if (prefix is not None) and (len( prefix ) >= maxLen):
            return []
        # Base Case, Beginning of original list: Gather first element
        if prefix is None:
            nuElem = [ elem ]
        # Recursive Case: Append upper level prefix to current element to product combo
        elif prefix is not None:
            nuElem = prefix[:]
            nuElem.append( elem )
        # All Cases: Gather the element / combo
        rtnLst.append( nuElem )
        # Recursive Case: Compute all possible combos with current element as prefix
        if i < N:
            ordered_combos( lst[i+1:], accumList = rtnLst, prefix = nuElem, maxLen = maxLen )
    ## End: Return all combos computed at this depth and below ##
    return rtnLst


def bin_lists_by_length( lstLst ):
    """ Return a dictionary with length keys and values that a lists of lists of that length """
    rtnDct = {}
    for lst in lstLst:
        N = len( lst )
        if N in rtnDct:
            rtnDct[N].append( lst )
        else:
            rtnDct[N] = [ lst, ]
    return rtnDct


def combine_and_sort_string_list( strLstLst ):
    """ Concat the elements of each list in `strLstLst` into single strings, then sort the resulting list """
    rtnLst = []
    for strLst in strLstLst:
        elemStr = ""
        for elem in strLst:
            elemStr += str( elem )
        rtnLst.append( elemStr )
    rtnLst.sort()
    return rtnLst



########## Composite ###############################################################################

class Mvec:
    """ Represents a Clifford multivector [ e1, e2, e3, ..., e12, e13, e23, ..., e123, ... ] """
    

    def __init__( self, realDim = 3 ):
        """ Build a list to hold all the parts of a clifford composite """
        self.e0       = None # Pure scalar part
        self.rDim     = realDim # Number of real dimensions of the space represented
        self.partLims = count_combos( realDim )
        self.blades   = [None for i in range( sum( self.partLims ) )]
        self.partLims = accum_elems( self.partLims )
        self.bladNams = self.get_blade_labels()
        self.nBlades  = len( self.bladNams )


    def get_blade_labels( self ):
        """  Create labels {e1, e2, e3, ..., e12, ...} to appropriate length all the way to `self.rDim` """
        dimStr = [ str( i+1 ) for i in range( self.rDim ) ]
        bldCmb = ordered_combos( dimStr )
        bldDct = bin_lists_by_length( bldCmb )
        bldLst = []
        Nlst   = []
        for k, v in bldDct.items():
            cmbLst = combine_and_sort_string_list( v )
            if (not bldLst) or (k > Nlst[-1]):
                bldLst.append( cmbLst )
                Nlst.append( k )
            elif k < Nlst[0]:
                bldLst.insert( 0, cmbLst )
                Nlst.insert(   0, k      )
            else:
                raise ValueError( "There was a problem with `bin_lists_by_length`" )
        rtnNam = []
        for subLst in bldLst:
            rtnNam.extend( subLst )
        rtnNam = [ 'e'+str( elem ) for elem in rtnNam ]
        return rtnNam


    def set_by_name( self, compDict, ignoreZero = 1 ):
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



##### Multivector Operations #####

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
    

def wedge( mvc1, mvc2 ):
    """ Wedge product of two multivectors """
    # The wedge product is always antisymmetric, associative, and anti-commutative.
    # Oriented length times oriented area equals oriented volume
    # (u^v)_{ij} = ( (u_i)(v_j) - (u_j)(v_i) )
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

    rtnMvc.set_by_name( setDct )
    return rtnMvc


def div( mvc1, mvc2 ):
    """ Multivector ratio --> Scalar """
    # 1. Fetch blade values by name
    mvc1dct = mvc1.get_by_name()
    mvc2dct = mvc2.get_by_name()
    # 2. Init resultant multivector
    rtnMvc    = Mvec( mvc1.rDim )
    rtnMvc.e0 = 0.0
    # 3. Ratio of scalar parts
    if mvc2dct.e0 != 0.0:
        rtnMvc.e0 = mvc1dct.e0 / mvc2dct.e0
    else:
        rtnMvc.e0 = float('nan')
        return rtnMvc 
    # 4. Sum the ratio of each corresponding pair of blades in each operand
    for bldNam1, blvVal1 in mvc1dct.items():
        if bldNam1 in mvc2dct:
            blvVal2 = mvc2dct[ bldNam1 ]
            if (blvVal1 != 0.0) and (blvVal2 != 0.0):
                rtnMvc.e0 += blvVal1 / blvVal2
    # 4. The result is a pure scalar, return it
    return rtnMvc


def mlt( mvc1, mvc2 ):
    """ Multivector product --> Scalar """
    # 1. Fetch blade values by name
    mvc1dct = mvc1.get_by_name()
    mvc2dct = mvc2.get_by_name()
    # 2. Init resultant multivector
    rtnMvc    = Mvec( mvc1.rDim )
    # 3. Product of scalar parts
    rtnMvc.e0 = mvc1dct.e0 * mvc2dct.e0
    # 4. Sum the product of each corresponding pair of blades in each operand
    for bldNam1, blvVal1 in mvc1dct.items():
        if bldNam1 in mvc2dct:
            blvVal2 = mvc2dct[ bldNam1 ]
            if (blvVal1 != 0.0) and (blvVal2 != 0.0):
                rtnMvc.e0 += blvVal1 * blvVal2
    # 4. The result is a pure scalar, return it
    return rtnMvc


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

print( "Wedge Test" )
mvc2 = Mvec()
mvc2.set_by_name({
    'e1': 1, 
    'e2': 2, 
    'e3': 3,
})

mvc3 = wedge( mvc1, mvc1 )
print( mvc3 )

### CalcBLUE 4 : Ch. 16.3 : The Wedge Product, https://www.youtube.com/watch?v=iVwrA0K3ebc ###

print( "CalcBLUE 4 : Ch. 16.3" )

# t = 4:19
alpha = Mvec(6) 
alpha.set_by_name({
    'e1':  3,
    'e3': -2,
    'e6':  1,
})

beta  = Mvec(6) 
beta.set_by_name({
    'e246': -5,
})

omega = Mvec(6)
omega.set_by_name({
    'e12': 1,
    'e34': 1,
}) 

mvc4 = wedge( beta, omega )

print( mvc4 ) # t = 4:19, CORRECT!

mvc5 = wedge( alpha, beta )

print( mvc5 ) # t = 5:37, CORRECT!