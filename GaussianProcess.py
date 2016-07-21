#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-06-25

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
FILENAME.py , Built on Spyder for Python 2.7
James Watson, YYYY MONTHNAME
A ONE LINE DESCRIPTION OF THE FILE
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
        print "None of the specified directories were loaded"
# List all the places where the research environment could be
add_first_valid_dir_to_path( [ '/home/jwatson/regrasp_planning/researchenv',
                               '/media/jwatson/FILEPILE/Python/ResearchEnv' ] )
from ResearchEnv import * # Load the custom environment
from ResearchUtils.Vector import *

# == End Init ==========================================================================================================

"""
* Gaussian Distribtution - A multidimensional distribution , each random variable is a dimension
    ^ The individual random variables are indexed by their positions in the vector
    ^ An infinite-dimensional object, but we only work with dimensions that interest us

* A Gaussian process is full specified by its mean function and covariance function
    ^ A Gaussian Distribution is over vectors
    ^ A Gaussian process is over functions
    ^ An infinite-dimensional object, but we only work with dimensions that interest us, draw samples from the function f
        + Request the value of f at a distinct number 'n' locations
    
              Gaussian Distribution                      Gaussian Process
              ---------------------                      ----------------
Mean       |  \mu :    Vector Average                    m : "Averaging" function (not necessarily mean)
              \mu = [\mu_1 , ... , \mu_n  ]
Covariance |  \Sigma : Covariance matrix                 k : Covariance function
              \Sigma = [[\sigma_11 , ... , \sigma_1d ],
                        [    ... , sigma_ij , ...    ],
                        [\sigma_d1 , ... , \sigma_dd ]]
Variable   |  x :      Vector of random variables        f(x) : Valud of the stochastic function at x
"""