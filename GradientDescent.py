#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-07-21

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
GaussianProcess.py , Built on Spyder for Python 2.7
James Watson, 2016 July
Teach yourself gaussian processes
"""

# == Init Environment ==================================================================================================
import sys, os.path
SOURCEDIR = os.path.dirname(os.path.abspath(__file__)) # URL, dir containing source file: http://stackoverflow.com/a/7783326

def add_first_valid_dir_to_path(dirList):
    """ Add the first valid directory in 'dirList' to the system path """
    # In lieu of actually installing the library, just keep a list of all the places it could be in each environment
    loadedOne = False
    for drctry in dirList:
        if os.path.exists( drctry ):
            sys.path.append( drctry )
            print 'Loaded', str(drctry)
            loadedOne = True
            break
    if not loadedOne:
        raise ImportError("None of the specified directories were loaded") # Assume that not having this loaded is a bad thing
# List all the places where the research environment could be
add_first_valid_dir_to_path( [ '/home/jwatson/regrasp_planning/researchenv',
                               '/media/jwatson/FILEPILE/Python/ResearchEnv',
                               'F:\Python\ResearchEnv',
                               '/media/mawglin/FILEPILE/Python/ResearchEnv'] )

# ~~ Libraries ~~
# ~ Standard Libraries ~
import random
# ~ Special Libraries ~
# ~ Local Libraries ~
from ResearchEnv import * # Load the custom environment
from ResearchUtils.Plotting import *
from ResearchUtils.Vector import np_add

# == End Init ==========================================================================================================

"""
URL, Simplest Gradient Descent: http://eli.thegreenplace.net/2016/understanding-gradient-descent/

Gradient Descent is a common tool for optimizing complex functions iteratively with a computer program.
The goal is: given some arbitrary function, find a minima.
For convex functions, the local minimum is also the global minimum. 

The main premise of Gradient Descent is: Given some current location x in the search space, we ought to update x in the
direction opposite of the gradient of the function. The results are trivial for a one-dimensional convex function, but
the techniques are very similar to non-convex, high-dimensional cases.

In the univariate case, the derivative takes the place of the gradient.
"""

f = lambda x: (x - 1.0) ** 2

def function_slope( f ):
    """ Return a function that estimates the slope of 'f'  """
    # NOTE: This function assumes that 'f' is continuous and differentiable for all x
    def slope( x , delta = 0.05 ):
        # run = 2 * delta
        # rise = f(x + delta) - f(x - delta)
        return ( f(x + delta) - f(x - delta) ) / ( 2 * delta )
    return slope
    
fdx = function_slope( f )

print f(2)         # 1.0
print fdx(2)       # 2.0
print fdx(2, 0.01) # 2.0

def guess( x_0 , grad , rate):
    """ Return a guess for x_1 that is in the opposite direction of the gradient """
    #      v--- Present state
    return x_0 - rate * grad( x_0 )
# Learning rate -^      ^-- Gradient function, evaluated at the present state

state = (random.random() - 0.5) * 40 # Choose a random number [-5, 5)

for i in range(40):
    print "{0:.2}".format(state), 
    state = guess(state, fdx, 0.2)
""" Even this simple loop finds the miminum very easily
-1.7e+01 -1e+01 -5.6 -3.0 -1.4 -0.43 0.14 0.49 0.69 0.81 0.89 0.93 0.96 0.98 0.99 0.99 0.99 1.0 1.0 ... """

def function_gradient( f ):
    """ Return a function that computes the gradient at 'Xn' """
    # NOTE: The resulting function evaluates f(*Xn) twice for every dimension 
    def gradient( *Xn , **kwargs ):
        grad = []
        delta = kwargs['delta'] if 'delta' in kwargs else 0.05
        for i , x_i in enumerate(Xn):
            diff = np.zeros(len(Xn))
            diff[i] = delta
            argsHi = np.add( Xn , diff )
            argsLo = np.subtract( Xn , diff )
            # run = 2 * delta
            # rise = f(x + delta) - f(x - delta)            
            grad.append( ( f( *argsHi ) - f( *argsLo ) ) / (2 * delta) ) 
        return grad
    return gradient

def guess_nd( x_0 , grad , rate):
    """ Return a guess for x_1 that is in the opposite direction of the gradient, for multivariate functions """
    #                   v--- Present state
    return np.subtract( x_0 , np.multiply( grad( *x_0 , delta=0.01 ) , rate ) )
    #      Gradient function, evaluated at x_0 ---^                    ^--- Learning rate 

print endl 
    
f2 = lambda x,y : x**2 + y**2
f2grd = function_gradient( f2 )
        
state = [ ((random.random() - 0.5) * 400) for x in range(2) ]
for i in range(40):
    print ["{0:.2}".format(x) for x in state], 
    state = guess_nd(state, f2grd, 0.5)
""" Finds the minimum very quickly
['-5.4e+01', '-1.9e+02'] ['-1.4e-10', '-2.2e-10'] ['0.0', '-8.1e-20'] ... 
                       At "0" after 3 iterations ---^-------^              """