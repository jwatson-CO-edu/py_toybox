""" 
* https://web.mat.upc.edu/carles.batlle/MOSS/broenink.pdf
"""

# JType = [0,1]

########## Element ################################################################################

class Element:
    """ Models a transfer of energy """
    
    def __init__( self, head = None, tail = None ):
        """ Set connections """
        self.head = head
        self.tail = tail



########## Junction ###############################################################################

class Junction:
    """ Models a connection between elements """

    def __init__( self, typ = -1, ports = None ):
        """ Set type and connected elements """
        self.type = typ
        if ports is None:
            self.ports = []
        else:
            self.ports = ports[:]