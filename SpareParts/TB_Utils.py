import os , heapq , operator , cPickle
import numpy as np
from math import sqrt

# ~~ Constants , Shortcuts , Aliases ~~
import __builtin__ # URL, add global vars across modules: http://stackoverflow.com/a/15959638/893511
__builtin__.EPSILON = 1e-7
__builtin__.infty = 1e309 # URL: http://stackoverflow.com/questions/1628026/python-infinity-any-caveats#comment31860436_1628026
__builtin__.endl = os.linesep

# == Added for HW02 ==

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
    # print "DEBUG , exited after" , count , "iterations"
    sortBounds = [ sorted( sub ) for sub in members ]
    return [ ( sub[0] , sub[-1] ) for sub in sortBounds ]

# = File Operations =

def struct_to_pkl( struct , pklPath ): 
    """ Serialize a 'struct' to 'pklPath' """
    f = open( pklPath , 'wb') # open a file for binary writing to receive pickled data
    cPickle.dump( struct , f ) # changed: pickle.dump --> cPickle.dump
    f.close()
    
def load_pkl_struct( pklPath ): 
    """ Load a pickled object and return it, return None if error """
    fileLoaded = False
    rtnStruct = None
    try:
        f = open( pklPath , 'rb')
        fileLoaded = True
    except Exception as err:
        print "load_pkl_struct: Could not open file,",pklPath,",",err
    if fileLoaded:
        try:
            rtnStruct = cPickle.load( f )
        except Exception as err:
            print "load_pkl_struct: Could not unpickle file,",pklPath,",",err
        f.close()
    return rtnStruct

# = End File I/O =

def tick_progress( div = 1000 , reset = False ):
    """ Print the 'marker' every 'div' calls """
    if reset:
        tick_progress.totalCalls = 0
    else:
        tick_progress.totalCalls += 1
        if tick_progress.totalCalls % div == 0:
            tick_progress.ticks += 1
            print tick_progress.sequence[ tick_progress.ticks % ( len( tick_progress.sequence ) ) ] ,
tick_progress.totalCalls = 0
tick_progress.sequence = [ '|' , '/' , '-' , '\\' ]
tick_progress.ticks = 0

def percent_change( oldVal , newVal ):
    """ Return the precent change from 'oldVal' to 'newVal' , This version avoids div/0 errors """
    if eq( oldVal , 0 ): # If the old value is zero
        if eq( newVal , 0 ):
            return 0.0 # If both values are zero, no change
        else:
            return infty # else div/0 , undefined , return infinity
    return ( newVal - oldVal ) / oldVal * 100.0

def str_args( *args , **kwargs ):
    """ Print a sequence that is composed of the '__str__' of each of the arguments in the format "elem_0 , ... , elem_n" , separated by commas & spaces """
    prnStr = ""
    for index , elem in enumerate( args ):
        if index < len( args ) - 1:
            prnStr += str( elem ) + " , "
        else:
            prnStr += str( elem )
    if "printStr" in kwargs:
        print prnStr
    else:
        return prnStr

def separation_dist_pts( ptsList ):
    """ Return a list consising of tuples ( pt1 , pt2 , dist ) of the distances between each pair of points in 'ptsList' , O(n^2) """
    distances = []
    for i in xrange( len( ptsList ) ):
        for j in xrange( i+1 , len( ptsList ) ):
            distances.append( ( ptsList[i] , ptsList[j] , vec_dif_mag( ptsList[i] , ptsList[j] ) ) )
    return distances

def tokenize_with_wspace( rawStr , evalFunc=str ): 
    """ Return a list of tokens taken from 'rawStr' that is partitioned with whitespace, transforming each token with 'evalFunc' """
    return [ evalFunc(rawToken) for rawToken in rawStr.split() ]

x_ = lambda pnt: pnt[0]
y_ = lambda pnt: pnt[1]

def intersect_pnt_lines( seg1 , seg2 ):
    """ Return the intersection of two lines defined by 'seg1' and 'seg2' , otherwise if lines are coincident or parallel , return None """
    # URL: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
    p1 , p2 , p3 , p4 = seg1[0] , seg1[1] , seg2[0] , seg2[1]
    x1 , y1 , x2 , y2 , x3 , y3 , x4 , y4 = x_( p1 ) , y_( p1 ) , x_( p2 ) , y_( p2 ) , x_( p3 ) , y_( p3 ) , x_( p4 ) , y_( p4 )
    den = ( x1 - x2 ) * ( y3 - y4 ) - ( y1 - y2 ) * ( x3 - x4 )
    if not eq( 0 , den ): # If the denominator is not zero , then there is a definite solution
        num_x = ( x1 * y2 - y1 * x2 ) * ( x3 - x4 ) - ( x1 - x2 ) * ( x3 * y4 - y3 * x4 )
        num_y = ( x1 * y2 - y1 * x2 ) * ( y3 - y4 ) - ( y1 - y2 ) * ( x3 * y4 - y3 * x4 )
        return [ num_x / den , num_y / den ]
    else: # else lines are parallel or coincident , return None
        return None
    
def vec_dif_sqr( vec1 , vec2 ):
    """ Return the squared magnitude of the vector difference between 'vec1' and 'vec2' """
    vecDiff = np.subtract( vec1 , vec2 )
    return np.dot( vecDiff , vecDiff ) # The squared magnitude is just the vector dotted with itself

def vec_mag(vec): 
    """ Return the magnitude of a vector """
    return np.linalg.norm(vec)

def vec_dif_mag( vec1 , vec2 ):
    """ Return the magnitude of the vector difference between 'vec1' and 'vec2' """
    return vec_mag( np.subtract( vec1 , vec2 ) )
    
def indexw( i , iterable ): 
    """ Return the 'i'th index of 'iterable', wrapping to index 0 at all integer multiples of 'len(iterable)' """
    return i % ( len(iterable) )

class Counter(dict):  # TODO: UPDATE ASMENV
    """ The counter object acts as a dict, but sets previously unused keys to a 'default' , the default of 'default' is 0 """
    
    def __init__( self , *args , **kwargs ): # TODO: UPDATE ASMENV
        """ Standard dict init """
        dict.__init__( self , *args , **kwargs )
        if 'default' in kwargs:
            self.default = kwargs['default']
        else:
            self.default = 0
        
    def __getitem__( self , a ):
        """ Get the val with key , otherwise return the 'default' if key DNE """
        if a in self: 
            return dict.__getitem__( self , a )
        return self.default
    
    # __setitem__ provided by 'dict'
    
    def sorted_keyVals( self ):  # TODO: UPDATE ASMENV
        """ Return a list of ( key , value ) tuples sorted by key """
        sortedItems = self.items()
        sortedItems.sort( cmp = lambda keyVal1 , keyVal2 :  np.sign( keyVal2[1] - keyVal1[1] ) )
        return sortedItems

def d_point_to_2Dsegment( point , segment ): # Changed the signature to fit the more recent representation of segments [ [ x0 , y0 ] , [ x1 , y1 ] ]
    """ Return the shortest (perpendicular) distance between 'point' and a line segment defined by 'segPt1' and 'segPt2' """
    # URL: http://mathworld.wolfram.com/Point-LineDistance2-Dimensional.html
    segPt1 = segment[0] ; segPt2 = segment[1]
    return abs( ( segPt2[0] - segPt1[0] ) * ( segPt1[1] - point[1] ) - \
                ( segPt1[0] - point[0] ) * ( segPt2[1] - segPt1[1] ) ) / sqrt( ( segPt2[0] - segPt1[0] )**2 + ( segPt2[1] - segPt1[1] )**2 )

def split_to_components( vecList ): 
    """ Separate a list of R^n vectors into a list of n lists of components , in order """ # because matplotlib likes it that way
    components = [ [] for dim in xrange( len( vecList[0] ) ) ] # NOTE: This function assumes that all vectors of 'vecList' are the same dimensionality
    for vec in vecList:
        for i , elem in enumerate( vec ):
            components[i].append( elem )
    return components

def list_search_w_test( pList , item , eqTest ):
    """ Linear search of 'pList' , determine membership with 'eqTest' and return index if the test passes , Otherwise return None if DNE """
    for i , elem in enumerate( pList ):
        if eqTest( item , elem ):
            return i
    # print "DEBUG , item not found" , item
    return None

class PriorityQueue(list): # Requires heapq 
    """ Implements a priority queue data structure. """ 
    # NOTE: PriorityQueue does not allow you to change the priority of an item. You may insert the same item multiple times with different priorities. 
        
    def __init__( self , *args ):
        """ Normal 'list' init """
        list.__init__( self , *args )   
        self.count = 0
        self.s = set([])    
        
    def push( self , item , priority , hashable=None ):
        """ Push an item on the queue and automatically order by priority , optionally provide 'hashable' version of item for set testing """
        entry = ( priority , self.count , item )
        heapq.heappush( self , entry )
        self.count += 1
        if hashable:
            self.s.add( hashable ) 
            
    def push_uniq( self , item , priority , hashable=None ): # Add to resenv
        """ Only push an item if it has not been pushed before """
        if item not in self:
            self.push( item , priority , hashable ) # This should call the child class version
            
    def push_uniq_test( self , item , priority , hashable=None , test = operator.eq ): # Add to resenv
        """ Only push an item if it has not been pushed before , utilizing a user-specified equality function """
        # if list_search_w_test( self , item , test ) == None:
        if list_search_w_test( [ elem[2] for elem in self ] , item , test ) == None:
            self.push( item , priority , hashable ) # This should call the child class version      
    
    def contains( self , hashable ): 
        ''' Test if 'node' is in the queue '''
        return hashable in self.s

    def pop( self ):
        """ Pop the lowest-priority item from the queue """
        priority , count , item = heapq.heappop( self )
        return item
        
    def pop_with_priority( self ):
        """ Pop the item and the priority associated with it """
        priority , count , item = heapq.heappop( self )
        return item , priority
        
    def pop_opposite( self ):
        """ Remove the item with the longest priority , opoosite of the usual pop """
        priority , count , item = self[-1]
        del self[-1]
        return item

    def isEmpty(self):
        """ Return True if the queue has no items, otherwise return False """
        return len( self ) == 0
        
    # __len__ is provided by 'list'
        
    def unspool( self , N = infty , limit = infty ):
        """ Pop all items as two sorted lists, one of increasing priorities and the other of the corresponding items """
        vals = []
        itms = []
        count = 0
        while not self.isEmpty() and count < N and self.top_priority() <= limit:
            item , valu = self.pop_with_priority()
            vals.append( valu )
            itms.append( item )
            count += 1
        return itms , vals
        
    def peek( self ):
        """ Return the shortest priority item without popping it """
        priority , count , item = self[0]
        return item
        
    def peek_opposite( self ):
        """ Return the longest priority item without popping it """
        priority , count , item = self[-1]
        return item
        
    def top_priority( self ):
        """ Return the value of the shortest priority """
        return self[0][0]
        
    def btm_priority( self ):
        """ Return the value of the longest priority """
        return self[-1][0]

class BPQ( PriorityQueue ):
    """ Bounded Priority Queue , does not keep more than N items in the queue """
    
    def __init__( self , boundN , *args ):
        """ Create a priority queue with a specified bound """
        PriorityQueue.__init__( self , *args )
        self.bound = boundN
    
    def push( self , item , priority , hashable=None ):
        """ Push an item onto the queue and discard largest priority items that are out of bounds """
        PriorityQueue.push( self , item , priority , hashable ) # The usual push
        while len( self ) > self.bound: # If we exceeded the bounds , then discard down to the limit
            self.pop_opposite()

# = Statistics =

def itself( item ): return item # dummy function, return the argument itself # Added to ResearchEnv 2016-09-13
    
def accumulate(pLst , func=itself): 
    """ Return the sum of func(item) for all items in 'pLst'. Return the total number of non-list/tuple items in 'pLst'. Recursive """
    total = 0 # Accumulated total for results of 'func(item)'
    N = 0 # Number of items encountered
    for item in pLst: # for each item in the list
        if isinstance(item, (list,tuple)): # if the list item is itself an iterable
            partTot, partN = accumulate( item , func ) # recur on item
            total += partTot # Accumulate results from greater depth
            N += partN
        else: # else assume item is a number
            total += func( item ) # invoke 'func' on item and accumulate
            N += 1 # count the item
    return total, N # Return the accumulation total and the number of items

def avg(*args): 
    """ Average of args, where args can be numbers, a list, or nested lists """
    total, N = accumulate(args) # Accumulate a straight sum
    if N == 0:
        print "avg: Undefined for 0 items!"
        return None
    return float(total) / N # return mean
    
def variance(*args): 
    """ Variance of args, where args can be numbers, a list of numbers, or nested lists of numbere """
    total, N = accumulate(args) # calc mean
    if N == 0:
        print "variance: Undefined for 0 items!"
        return None
    # print total , 
    mu = float(total) / N
    # print "DEBUG , mu in variance" , mu
    totSqDiffs , N = accumulate( args , lambda x: ( x - mu )**2 ) # calc the per-item variance
    # print "DEBUG , total sq diff" , totSqDiffs , ", N:" , N
    return (1.0 / N) * totSqDiffs # return variance

def std_dev( *args ): 
    """ Standard deviation of args, where args can be numbers, a list of numbers, or nested lists of numbere """
    var = variance(*args)
    # print "DEBUG , Variance:" , var
    if var == None:
        print "std_dev: Undefined for 0 items!"
        return None
    return sqrt( var )

# = End Stats =

def vec_eq( vec1 , vec2 , margin = EPSILON ): # <<< resenv
    """ Return true if two vectors are equal enough, otherwise false """
    if len(vec1) == len(vec2):
        for i in xrange( len(vec1) ):
            if not eq_margin( vec1[i] , vec2[i] , margin):
                return False
        return True # CHANGED
    else:
        return False
    

def vec_eq_test_w_margin( margin = EPSILON ):
    """ Return a function that performs an 'vec_eq' comparison with the specified margin """
    def eq_test( op1 , op2 ):
        return vec_eq( op1 , op2 , margin )
    return eq_test
    
# == End HW02 ==


# == Added for HW01 ==

def eq(op1, op2): 
    """ Return true if op1 and op2 are close enough """
    return abs(op1 - op2) <= EPSILON
    
def eq_margin( op1 , op2 , margin = EPSILON ): 
    """ Return true if op1 and op2 are within 'margin' of each other, where 'margin' is a positive real number """
    return abs( op1 - op2 ) <= margin

def np_add(*args): 
    """ Perform 'np.add' on more than two args """
    if len(args) > 2: # If there are more than 2 args, add the first arg to recur on remainder of args
        return np.add( args[0] , np_add(*args[1:]) ) # Note the star operator is needed for recursive call, unpack to positional args
    else: # base case, there are 2 args*, use vanilla 'np.add'
        return np.add( args[0] , args[1] ) # *NOTE: This function assumes there are at least two args, if only 1 an error will occur

def vec_avg( *vectors ): 
    """ Return a vector that is the average of all the 'vectors', equal weighting """
    vecSum = np_add( *vectors ) # NOTE: This function assumes that all vectors are the same dimensionality
    return np.divide( vecSum , len(vectors) * 1.0 )

def np_dot( *args ): 
    """ Perform 'np.dot' on more than two args """
    if len( args ) > 2: # If there are more than 2 args, subtract the last arg from the preceeding remainder of args
        return np.dot( args[0] , np_dot( *args[1:] ) ) # Note the star operator is needed for recursive call, unpack to positional args
    else: # base case, there are 2 args*, use vanilla 'np.subtract'
        return np.dot( args[0] , args[1] ) # *NOTE: This function assumes there are at least two args, if only 1 an error will occur
    
def intersect_pnt_2D( seg1 , seg2 , coincidentAvg = True ): 
    """ if line segments 'seg1' and 'seg2' intersect, then return intersection point , otherwise return false """
    #               { seg1: [ [x1,y1] , [x2,y2] ] , seg2: [ [x3,y3] , [x4,y4] ]  }
    # URL: http://www-cs.ccny.cuny.edu/~wolberg/capstone/intersection/Intersection%20point%20of%20two%20lines.html
    den =   (seg2[1][1] - seg2[0][1]) * (seg1[1][0] - seg1[0][0]) - (seg2[1][0] - seg2[0][0]) * (seg1[1][1] - seg1[0][1])
    uAnum = (seg2[1][0] - seg2[0][0]) * (seg1[0][1] - seg2[0][1]) - (seg2[1][1] - seg2[0][1]) * (seg1[0][0] - seg2[0][0])
    uBnum = (seg1[1][0] - seg1[0][0]) * (seg1[0][1] - seg2[0][1]) - (seg1[1][1] - seg1[0][1]) * (seg1[0][0] - seg2[0][0])
    if den == 0:
        if eq(uAnum , 0.0) or eq(uBnum , 0.0):
            if coincidentAvg:
                return vec_avg( seg1[0] , seg1[1] , seg2[0] , seg2[1] ) # Lines are coincident, return the average of segment centers, this is not overlap center
            else:
                return False
        else:
            return False # Lines are parallel
    else:
        uA = uAnum * 1.0 / den
        uB = uBnum * 1.0 / den
        if (uA >= 0 and uA <= 1) and (uB >= 0 and uB <= 1):
        # { seg1:[ [x1,y1] , [x2,y2] ] , seg2: [ [x3,y3] , [x4,y4] ]  }
        #   return [ x1 + uA * ( x2 - x1 ) , y1 + uA * ( y2 - y1 ) ]
            return [ seg1[0][0] + uA * (seg1[1][0] - seg1[0][0]) , seg1[0][1] + uA * (seg1[1][1] - seg1[0][1]) ]
        else:
            return False # Lines do not intersect

def intersect_ray_2D( ray1 , ray2 ): 
    """ if rays 'ray1' and 'ray2' intersect, then return intersection point , otherwise return False """
    #               { ray1: [ [x1,y1] , [x2,y2] ] , ray2: [ [x3,y3] , [x4,y4] ]  }
    # URL: http://www-cs.ccny.cuny.edu/~wolberg/capstone/intersection/Intersection%20point%20of%20two%20lines.html
    den =   (ray2[1][1] - ray2[0][1]) * (ray1[1][0] - ray1[0][0]) - (ray2[1][0] - ray2[0][0]) * (ray1[1][1] - ray1[0][1])
    uAnum = (ray2[1][0] - ray2[0][0]) * (ray1[0][1] - ray2[0][1]) - (ray2[1][1] - ray2[0][1]) * (ray1[0][0] - ray2[0][0])
    uBnum = (ray1[1][0] - ray1[0][0]) * (ray1[0][1] - ray2[0][1]) - (ray1[1][1] - ray1[0][1]) * (ray1[0][0] - ray2[0][0])
    if den == 0:
        if eq(uAnum , 0.0) or eq(uBnum , 0.0):
            return vec_avg( ray1[0] , ray1[1] , ray2[0] , ray2[1] ) # Lines are coincident, return the average of segment centers, this is not overlap center
        else:
            return False # Lines are parallel
    else:
        uA = uAnum * 1.0 / den
        uB = uBnum * 1.0 / den
        if uA >= 0 and uB >= 0:
        # { ray1: [ [x1,y1] , [x2,y2] ] , ray2: [ [x3,y3] , [x4,y4] ]  }
        #   return [ x1 + uA * ( x2 - x1 ) , y1 + uA * ( y2 - y1 ) ]
            return [ ray1[0][0] + uA * (ray1[1][0] - ray1[0][0]) , ray1[0][1] + uA * (ray1[1][1] - ray1[0][1]) ]
        else:
            return False # Lines do not intersect
        
def sep(title = "", width = 6, char = '=', strOut = False): # <<< resenv
    """ Print a separating title card for debug """
    LINE = width*char
    if strOut:
        return LINE + ' ' + title + ' ' + LINE
    else:
        print LINE + ' ' + title + ' ' + LINE
        
def seg_to_line_eq_2D( segment ):
    """ Return 'm' and 'b' of "y=mx+b" corresponding to 'segment' """
    m = ( segment[1][1] - segment[0][1] ) / ( segment[1][0] - segment[0][0] ) # Rise over run
    return m , segment[0][1] + segment[0][0] * -m # y_1 - m * x_1 # Follow the line back from the first point to the y-axis
    
def y_from_xm_b( x , m , b ): return m*x + b # "y=mx+b" , get the y coordinate given 'x' coordinate , slope 'm' , and y-intercept 'b'
    
# == End HW01 ==