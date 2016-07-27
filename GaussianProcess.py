#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-07-21

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

# == End Init ==========================================================================================================

"""
* Normal/Gaussian Distribution
    ^ Mainstay of statistics
    ^ Standard Normal: Z ~ N(0,1) , Distribution with mean (\mu) = 0 and standard deviation (\sigma) = 1
    ^ Shift and scale the standard normal to model any phenomenon that is represented by a normal random variable
      X = \mu + \sigma * Z  : \mu shifts the center , \sigma scales the spread

* Gaussian Multivariate Distribtution - A multidimensional distribution , each random variable is a dimension
    ^ The individual random variables are indexed by their positions in the vector
    ^ An infinite-dimensional object, but we only work with dimensions that interest us
    ^ The multivariate normal distribution is often the assumed distribution underlying data samples and 
      it is widely used in pattern recognition and classifcation
    ^ Generate a random vector
        1. Generate n random values x_1 to x_n
        2. Assemble the variables into a 1 X n vector, this vector has a distribution N(0,I_d) where I_d is the identity matrix
            a. The covariance matrix has no off-diagonal terms because the random variables have no influence on each other
        3. Transform x such that x ~ N( \mu , \Sigma )
            b. \Sigma = [[\sigma_11 , ... , \sigma_1d ],    \sigma_ij = E[ (x_i - \mu_i)(x_j - \mu_j) ]
                        [    ... , sigma_ij , ...    ],     The expectation of the the product of each element's deviation
                        [\sigma_d1 , ... , \sigma_dd ]]     from the corresponding mean

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
              
Variable   |  x :      Vector of random variables        f(x) : Valud of the stochastic function at x
"""

def normal_dist_ratio_method():
    """ Return a number X with standard normal distribution \mu = 0, \sigma = 1, using the ratio method """
    # URL, generate a normal distribution of numbers: https://en.wikipedia.org/wiki/Normal_distribution#Generating_values_from_normal_distribution
    # This is just one of a number of ways to generate numbers on a normal distribution, or use 'numpy.random.normal'
    while True:
        U = random.random() # Algo requires two independent, uniformly distributed random numbers
        V = random.random()
        X = sqrt( 8 / e ) * (V - 0.5) / U # candidate number
        if X ** 2 <= 5 - 4 * e ** 0.25 * U:
            return X # accept
        if X ** 2 >= 4 * e ** -1.35 / U + 1.4:
            continue # reject
        if X ** 2 <= -4 * log(U):
            return X # accept
        # else not accepted, generate new and check
        
def normal_std_vec(dim):
    """ Return a vector sampled from the standard normal in 'dim' dimensions , Z~N(0,I_d) """
    rtnVec = [ normal_dist_ratio_method() for n in xrange(dim) ]
    return np.transpose( np.matrix( rtnVec ) ) # 'np.transpose' does not perform as expected on a vanilla array, must convert to np.matrix first
     
if False: # Set to true to verify the effectiveness of the normal random number generator, above
    data = [ normal_dist_ratio_method() for n in range(50000) ] # Gen 50k nums on a standard normal distribution
    
    # URL, histogram of a normally distributed random variable: http://matplotlib.org/1.2.1/examples/pylab_examples/histogram_demo.html
    
    # the histogram of the data
    n, bins, patches = plt.hist(data, 50, normed=1, facecolor='green', alpha=0.75)
    
    # add a 'best fit' line
    import matplotlib.mlab as mlab
    y = mlab.normpdf( bins, 0, 1)
    plt.plot(bins, y, 'r--', linewidth=1)
    
    plt.xlabel('X')
    plt.ylabel('Probability')
    plt.title(r'$\mathrm{Histogram\ of\ X:}\ \mu=0,\ \sigma=1$')
    plt.axis([-4, 4, 0, 1])
    plt.grid(True)
    
    plt.show() # Result: Generated numbers fit a normal distribution very well!
    
# Generate a bivariate distribution
if True: # Set to true to generate and display random vectors from a bivariate Gaussian distribution
    """ 
    == Section 5.2 , Generating Random Vectors from the Multivariate Normal Distribution , Art Owen , "Ch-randvectors.pdf"  ==
    
    Objective: To obtain random vector from the Gaussian distribution N( \mu , \Sigma )
    \mu = [ [1] ,      \Sigma = [ [ 1.0 , 0.3 ] ,
            [2] ]                 [ 0.3 , 0.6] ]
    
    To sample N( \mu , \Sigma ), we find a matrix C such that C * transpose(C) == \Sigma, then we set
    X = \mu + C*Z   ,   where Z~N(0,I_d) , the standard normal in d dimensions
    """
    
    mu = [ [ 1.0 ] , 
           [ 2.0 ] ]                 
    Sigma = [ [ 1.0 , 0.3 ] , 
              [ 0.3 , 0.6 ] ]
    
    def eigenvals_2D( Sigma ): # Forget this, just use "numpy". DIY eigendecomposition is a project for another day!
        """ Calc the eigenvalues of the 2x2 matrix sigma and return as a row vector """
        b = -Sigma[0][0] - Sigma[1][1]
        c = (-Sigma[0][0]) * (-Sigma[1][1]) - (-Sigma[0][1]) * (-Sigma[1][0])
        return quadroots( 1 , b , c )
    
    # eigens = eigenvals_2D( Sigma )
    # print eigens
    
    #Lambda = np.multiply( np.eye(2) , np.transpose( [eigens] ) )
    #print Lambda
    
    eigVals , eigVecs = np.linalg.eig( Sigma )
    print eigVals
    print eigVecs
    
    P = np.matrix( np.transpose(eigVecs) )
    LambdaOneHalf = np.matrix(np.diag( [sqrt(eigen) for eigen in eigVals] ) )
    print P
    print LambdaOneHalf
    
    def mat_mult(*matrices): # This function turned out to be unnecessary, as numpy automatically handles the currect order
        """ Multiply matrices in the correct order """
        if len(matrices) == 2:
            return np.dot( matrices[0] , matrices[1] )
        elif len(matrices) > 2:
            return np.dot( matrices[0] , mat_mult( *matrices[1:] ) )
        else:
            raise Exception("mat_mult: Bad number of args " + str(len(matrices)) + " , args: " + str(matrices))
        
    #result1 = mat_mult( P , LambdaOneHalf , np.transpose(P) )
    #result2 = P * LambdaOneHalf * np.transpose(P)
    
    #print result1 == result2
    #print result1 
    #print result2
    
    C = P * LambdaOneHalf * np.transpose(P) # easy!
    print C
    
    N = 50000
    data = [ mu + C * normal_std_vec(2) for i in xrange(N) ]
    
    # FIXME: START HERE
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram2d.html
    # http://jpktd.blogspot.com/2012/01/distributions-with-matplotlib-in-3d.html