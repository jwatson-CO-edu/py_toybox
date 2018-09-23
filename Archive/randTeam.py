# -*- coding: utf-8 -*-
"""
FILENAME.py , Built on Spyder for Python 2.7
James Watson, YYYY MONTHNAME
A ONE LINE DESCRIPTION OF THE FILE

"""
# == Init Environment ==

# ~ PATH Changes ~ 
def localize():
    """ Add the current directory to Python path if it is not already there """
    from sys import path # I know it is bad style to load modules in function
    import os.path as os_path
    containerDir = os_path.dirname(__file__)
    if containerDir not in path:
        path.append( containerDir )

localize() # You can now load local modules!

# ~ Standard Libraries ~
import math
from math import sqrt, ceil, sin, cos, tan, atan2
# ~ Special Libraries ~
import matplotlib.pyplot as plt
import numpy as np
import random
# ~ Constants ~
EPSILON = 1e-7

# ~ Helper Functions ~

def eq(op1, op2):
    """ Return true if op1 and op2 are close enough """
    return abs(op1 - op2) <= EPSILON
    
def sep(title = ""):
    """ Print a separating title card for printing """
    LINE = '======'
    print LINE + ' ' + title + ' ' + LINE

# == End Init ==

for i in xrange(100):
    print random.randrange(1,4),