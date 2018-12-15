# -*- coding: utf-8 -*-
"""
ready-set-calc.py , Built on Spyder for Python 2.7
James Watson, 2015 December
Run this file to use Spyder as a calculator

  == LOG ==
2015-12-XX: Wrote 'degrees' versions of trig functions

  == TODO ==
! When changing this file, back up a copy to an external drive!
* Consider a function that will scrape for important temporary files (might the implementation be platform-dependent?)
  - Back up this file to the regular Python folder
  - Back up the template file to the regular Python folder
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
from math import sqrt, ceil, sin, cos, tan, atan2, asin, acos, atan, pi, degrees, radians, log10
# ~ Special Libraries ~
import matplotlib.pyplot as plt
import numpy as np
# ~ Constants ~
EPSILON = 1e-7

# ~ Helper Functions ~

def eq(op1, op2):
    """ Return true if op1 and op2 are close enough """
    return abs(op1 - op2) <= EPSILON

# == End Init ==

# == Degrees Trigonometry ==

def cosd(angleDeg):
    """ Return the cosine of the angle, given in degrees """
    return cos( radians( angleDeg ) )
    
def sind(angleDeg):
    """ Return the sine of the angle, given in degrees """
    return sin( radians( angleDeg ) )
    
def tand(angleDeg):
    """ Return the tangent of the angle, given in degrees """
    return tan( radians( angleDeg ) )
    
def acosd(ratio):
    """ Return the arccosine of the ratio, in degrees """
    return degrees( acos( ratio ) )
    
def asind(ratio):
    """ Return the arcsine of the ratio, in degrees """
    return degrees( asin( ratio ) )
    
def atand(ratio):
    """ Return the arctangent of the ratio, in degrees """
    return degrees( atan( ratio ) )
    
def atan2d(Ycoord, Xcoord):
    """ Return the quadrant-correct arctangent in degrees, given the Y and X coordinates """
    return degrees( atan2( Ycoord , Xcoord ) )

# == End Degrees ==