class TestClass( object ):
    """ A class to test inheritance """
    
    def __init__( self , num ):
        """ Store the number """
        self.number = num
        
        
class Class2( TestClass ):
    """ A class to inherit TestClass """
    
    def __init__( self ):
        """ Run the parent initializer """
        TestClass.__init__( self ,  4 )
        
        
if __name__ == "__main__":
    thing1 = Class2()