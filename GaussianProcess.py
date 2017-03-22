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
                        
------------------------------------------------------------------------------------------------                        
                        
    ^ A multivariate distribution is Gaussian if any linear combination of its components is Gaussian.
      Probability along a line drawn through the space will be a univariate Gaussian
    ^ X ~ N(\mu,C) , X is a Gaussian (random vector) with E[x_i] = \mu_i , E[] : expected value of
                     Covariance(x_i,x_j) = C_ij
                     C is positive semi-definite - all eigenvalues \lambda_i >= 0
    ^ A multivariate Gaussian is degenerate if det(C) == 0, has no width in one direction
      
    ^ The simplest Gaussian has independent components
      [ x_1 , ... , x_n ], each is a univariate Gaussian with its own mean and variance, so C = diag( [ \sigma_1 , ... , \sigma_n ] )
      Contours of prob density are axis-aligned because there is no co-variance, one var has no influence on any other
      x_i and x_j are independent IFF Cov(x_i , x_j) == 0 , aka no correlation, this holds for Gaussians but not necessarily other distributions
      This does not imply
    ^ A Gaussian X ~ N(\mu,C) has a density IFF it is non-degenerate, det(C) != 0
    ^ Density function for a multivariate Gaussian
      f(X) = (1 / sqrt( det( 2 * pi * C ) ) ) * exp( -0.5 * transpose(X - \mu) * inverse( C ) * (X - \mu) )
      ^_ C is invertible by the assumption that det(C) != 0
    ^ Any affine transformation on a multivariate Gaussian is Gaussian
    ^ Ax + \mu ~ N( \mu , C ) , where x is [x_1 , ... , x_n] ~ N(0,I_n)
    ^ A * transpose(A) = C # FIXME: HOW TO FIND A?
    
* geometric intuition for eignevalues: 
  ^ Let X ~ N(0,I_d), let C be the covariance matrix
    ^ A covariance matrix is always symmetric and always positive semi-definite
    ^ Any symmetric matrix can be diagonalized C = U * \Lambda * transpose(U)
      ^_ U is the matrix [u_1 , ... , u_n] of unit eigenvectors, it is orthogonal
      ^_ \Lambda = diag( [\lambda_1 , ... , \lambda_n] ) , the diagonal matrix of eigenvlaues of C, eigenvalues are non-degative for positive semi-definite matrix
    ^ C = U * \Lambda * transpose(U) = U * \Lambda^{1/2} * \Lambda^{1/2} * transpose(U) = (U * \Lambda^{1/2}) * transpose(U * \Lambda^{1/2}) = A * transpose(A)
      U * \Lambda^{1/2} = A
      THIS IS THE A WE NEEDED TO SAMPLE FROM THE GAUSSIAN DISTRIBUTION
      ^_ The major axes of the ellipsoid will be scaled by the square root of the associated eigenvalue, sqrt(\lambda_i) is the standard deviation along dimension i
      ^_ U is a rotation of the ellipsoid, showing the degree to which variance in one dimension affects the other(s), the eigenvectors are the basis vectors for for the
         distribution --> the major axes of the ellipsoid are aligned with the eigenvectors
    ^ Y = A*X + \mu , Y ~ N( \mu , C )
      ^_ \mu is an offset from the origin, the center of the distribution in Rn

* Marginalization
  Let X ~ N(\mu , C), x_a = [x_1 , ... , x_k], x_b = [x_{k+1} , ... , x_n]
  ^ \mu = [ \mu_a , \mu_b ]
  ^ C = [ [C_aa , C_ab] ,
          [C_ba , C_bb] ]
  ^ C_aa = [ [C_11 , ... , C_1k ] ,      And X_a ~ N( \mu_a , C_aa )      
             [ ... , C_ij , ... ] ,    
             [C_k1 , ... , C_kk ] ] 

* Addition: Gaussian properties are preserved under addition of independent Gaussians
  ^ X ~ N(\mu_x , C_x) , Y ~ (\mu_y , C_y) , X+Y = ( \mu_x + \mu_y , C_x + C_y )
             
* Conditional distribution
  ^ The distribution of X_1 given that X_2 takes a certain value ( X_1 | X_2 = x_2) is a Gaussian, this is essentially
    a cross-section of the bivariate Gaussian at X_2 = x_2, which is a univariate Gaussian
  ^ ( X_a | X_b = x_b) ~ N(m,D) , where
    m = \mu_a + C_ab * inverse(C_bb)( x_b - \mu_b )
    D = C_aa - C_ab * inverse(C_bb) * C_ba
      
* Quadratic Form in X
  transpose(X) * A * X , the level sets of a quadratic form are ellipsoids, when A is symmetric positive semi-definite
  ^ Positive definite means the eigenvalues are positive
  ^ transpose(x - \mu) * inverse(c) * (x - \mu) = transpose(x - \mu) * U * inverse(\Lambda) * transpose(U) * (x - \mu)
------------------------------------------------------------------------------------------------------------------------------------------------

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
 
def density_at(x , mu , sigma):
    # Return the probability density at 'x' of a Gaussian distribution with mean 'mu' and variance 'sigma'
    return (1 / sqrt( 2 * pi * sigma ** 2 ) ) * exp( -1 / (2 *  sigma ** 2) * (x - mu) ** 2 )
 
if True: # Set to true to demonstrate a univariate Gaussian
    pass
    
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
if False: # Set to true to generate and display random vectors from a bivariate Gaussian distribution
    """ 
    == Section 5.2 , Generating Random Vectors from the Multivariate Normal Distribution , Art Owen , "Ch-randvectors.pdf"  ==
    
    Objective: To obtain random vector from the Gaussian distribution N( \mu , \Sigma )
    \mu = [ [1] ,      \Sigma = [ [ 1.0 , 0.3 ] ,
            [2] ]                 [ 0.3 , 0.6] ]
    
    To sample N( \mu , \Sigma ), we find a matrix C such that C * transpose(C) == \Sigma, then we set
    X = \mu + C*Z   ,   where Z~N(0,I_d) , the standard normal in d dimensions
    """
    
    # NOTE: The distribution matches the shape of the example, but one paper defines a new \hat{\mu} while the other
    #       just uses \mu as an offset, and I'm not sure why
    
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
    """ The normalized (unit “length”) eigenvectors, such that the column v[:,i] is the eigenvector corresponding to the eigenvalue w[i] 
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.eig.html """
    print eigVals
    print eigVecs
    
    P = np.matrix( eigVecs )
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
    
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram2d.html
    # http://jpktd.blogspot.com/2012/01/distributions-with-matplotlib-in-3d.html
    
    # Split the data for plotting
    Xs = []
    Ys = []
    for datDex , datum in enumerate(data):
        Xs.append( float(datum[0][0]) ) # Individual elements will also be matrices unless you recast them
        Ys.append( float(datum[1][0]) )
        
    axisDivs = 50
    
    # Set up the X and Y edges of the histogram bins
    xEdges = np.linspace( float(mu[0][0]) - 3.0 , float(mu[0][0]) + 3.0 , axisDivs + 1 )
    yEdges = np.linspace( float(mu[1][0]) - 3.0 , float(mu[1][0]) + 3.0 , axisDivs + 1 )
    
    H, xedges, yedges = np.histogram2d(Ys, Xs, bins=(xEdges, yEdges))
    
    if True:
        fig = plt.figure()
        ax = fig.add_subplot(132)
        ax.set_title('pcolormesh: exact bin edges')
        X, Y = np.meshgrid(xedges, yedges)
        ax.pcolormesh(X, Y, H)
        ax.set_aspect('equal') 
        plt.show() 
    
    if True:
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111, projection='3d')
        # x, y = np.random.rand(2, 100) * 4
        # hist, xedges, yedges = np.histogram2d(x, y, bins=4)
        
        elements = (len(xEdges) - 1) * (len(yEdges) - 1)
        # xpos, ypos = np.meshgrid(xEdges[:-1] + 0.25, yEdges[:-1] + 0.25)
        xpos, ypos = np.meshgrid(xEdges[:-1] , yEdges[:-1] )
        
        xpos = xpos.flatten() # Why?
        ypos = ypos.flatten()
        zpos = np.zeros(elements)
        dx = 0.25 * np.ones_like(zpos)
        dy = dx.copy()
        dz = H.flatten()
        
        ax2.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')
        
        plt.show() 
        
if False: # Set to true to demonstrate a simple Gaussian Process
    """ Gaussian processes (GPs) extend multivariate Gaussian distributions to infinite dimensionality. Formally, a 
    Gaussian process generates data located throughout some domain such that any finite subset of the range follows a 
    multivariate Gaussian distribution. 
    
    The n observations on an arbitrary dataset y = { y_1 , ... , y_n } can be imagined as a single point sampled from 
    some n-variate Gaussian distribution, so the dataset is partnered with a Gaussian Process. 
        * Very often, it is assumed that the mean of the GP is zero everywhere. In this case, only the covariance function
          relates one observation to another
        * The choice of covariance function depends on the problem, 
        * The Squared Exponential is a popular covariance function:
          k( x , x' ) = \sigma_f ** 2 * exp( -1 * (x-x') ** 2 / ( 2 * l ** 2 ) ), where
              ^_ \sigma_f ** 2 : maximum allowable covariance, 
                  ^__ When x ~ x' then k(x,x') approaches this maximum, meaning f(x) is nearly perfectly correlated 
                      with f(x'). In order for there to be a smooth function neighbors should be alike
                  ^__ When x is distant from x' then k(x,x') ~ 0 instead, the two points have little influence over each 
                      other. The effect of this separation depends on the length parameter l
        * Each observation y can be thought of as related to an underlying system model function f(x) plus a Gaussian noise model
          y = f(x) + N( 0 , \sigma_n ** 2 )
          
        * !!---> Regression is the search for f(x) <---!!
          
    Given n observations, our objective is to predict y_star, not the actual f_star.
    
    To prepare for Guassian Process Regression, we calculate the covariance function, among all possible combinations of points,
    summarizing out findings in 3 matrices: 
    
    K = [ [ k(x1,x1) , k(x1,x2) , ... , k(x1,xn) ] ,
                             ...
          [ k(xn,x1) , k(xn,x2) , ... , k(xn,xn) ] ]
    
    K_star = [ k(x_star,x1) , k(x_star,x2) , ... , k(x_star,xn) ]
    
    K_starstar = k( x_star , x_star )
    
    x_star : estimated state
    
    The diagonal elements of K are \sigma_f ** 2 + \sigma_n ** 2, and the extreme diagonals of K tend to 0 when x spans
    a large enough domain.
    
    Since the key assumption in GP modelling is that our data can be represented as a sample from a multivariate Gaussian
    distribution, we have that
    
    [[y     ],   ~   N(  0  ,  [[ K      , transpose(K_star) ]    )
     [y_star]]                  [ K_star , K_starstar        ]]
     
    The probability of a prediction y_star given an observation follows a Gaussian distribution. (Explained slowly in Appendix of M. Ebden, "GPtutorial.pdf")
    p( y_star | y ) = N(   K_star * inverse(K) * y   ,   K_starstar - K_star * inverse(K) * transpose(K_star)   )
                           ^-- Mean, Best estimate       ^-- Covariance, Uncertainty in estimate
                           
                    
    """
    
    #Code from: https://www.youtube.com/watch?v=clMbOOz6yR0
    #% Choose a kernel (covariance function)  
    kernelChoice = 1
    kernels = {
        #case 1; k =@(x,y) 1*x'*y; % Linear      
        1: lambda x,y: 1 * np.dot( x , y ), # Linear
        #case 2; k =@(x,y) 1*min(x,y); % Brownian
        2: lambda x,y: 1 * np.minimum( x , y ), # Brownian
        #                     ^-- Return the lesser of the two vectors
        #case 3; k =@(x,y) exp(-1013*(x-y)'*(x-y)) % Squared exponential     
        3: lambda x,y: exp( -1013 * np.dot( np.subtract(x,y) , np.subtract(x,y) ) ), # Squared exponential     
        #case 4; k =@(x,y) exp(-1*sqrt((x-y)'*(x-y)))     
        4: lambda x,y: exp( -1 * sqrt( np.dot( np.subtract(x,y) , np.subtract(x,y) ) ) ),
        #case 5; k =@(x,y) exp(-1*sin(50*pi*(x-y))^2) % Periodic
        5: lambda x,y: exp( -1 * sin( 50 * pi * np.subtract(x,y) ) ** 2 ),
        #case 6; k =@(x,y) exp(-100*min(abs(x-y), abs(x+y))^2)
        6: lambda x,y: exp( -100 * np.minimum( np.absolute( np.subtract(x,y) ), np.absolute( np.add(x,y) )) ** 2 )
        #                                         ^-- Return a vector where each element is the abs of the corresponding element in the arg
    }     
     
    #% Choose points at which to sample 15 
    #x= (0:.5:1);  
    x = np.arange(0,1.5,0.5)  
    n = len(x);  
     
    #% Construct the covariance matrix  
    C = np.zeros( (n,n) ); 
    #for i = 1:n      
        #for j = 1:n          
            #C(i,j)= k(x(i),x(j));     
        #end 
    #end 
    """ C =
    [ [ k( 0.0 , 0.0 ) , k( 0.0 , 0.5 ) , k( 0.0 , 1.0 ) ] ,
      [ k( 0.5 , 0.0 ) , k( 0.5 , 0.5 ) , k( 0.5 , 1.0 ) ] ,
      [ k( 1.0 , 0.0 ) , k( 1.0 , 0.5 ) , k( 1.0 , 1.0 ) ] ]
    """
    for i in xrange(n):
            for j in xrange(n):
                #C(i,j)= k(x(i),x(j));
                C[i][j] = kernels[kernelChoice]( x[i] , x[j] )    
    
    #% Sample from the Gaussian process at these  
    u = np.random.randn(n,1); # sample u ~ N(0, I_d) , d = 3 , Column vector 3x1
    #[A,S, B] = svd(C); % factor C = ASB' % Singular Value Decomposition
    A,S,B = np.linalg.svd( C )
    #print A
    #print S
    #print B
    #print u
    
    #z = A*np.sqrt(S)*u; % z = A S^.5 u  
    z = np.multiply(A , np.sqrt(S)) * u # z = A S^.5 u  # Sample from the process
    print z
    
    #% Plot  
    #figure(2); 
    #hold on; 
    #clf plot(x,z,'.-') 
    #axis([0, 1, -2, 2])﻿
    