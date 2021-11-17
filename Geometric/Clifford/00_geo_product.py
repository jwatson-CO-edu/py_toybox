import numpy as np

class VectorR2:
    # FIXME: START HERE
    pass

class BivectorR2:

    def __init__( self, vec1, vec2, mag ):
        self.vec1 = vec1
        self.vec2 = vec2
        self.mag  = mag

    def wedge( self, other ):
        # FIXME: START HERE
        pass

class CompositeR2:
    """ Represent the general geometric object 
    https://www.youtube.com/watch?v=PNlgMPzj-7Q&list=PLpzmRsG7u_gqaTo_vEseQ7U8KFvtiJY4K&index=1 """
    
    e1 = np.array( [ 1.0, 0.0 ] )
    e2 = np.array( [ 0.0, 1.0 ] )

    def __init__( self, value = [ 1.0, 0.0 ] ):
        self.val = value

    def as_np( self ):
        return np.array( self.val )

    def dot( self, other ):
        return np.dot( self.as_np(), other.as_np() )

    def wedge( self, other ):
        pass