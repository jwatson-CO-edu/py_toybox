# -*- coding: utf-8 -*-
"""
iterative_implicit.py
James Watson, 2015 October
Iteratively apply a function to tighter ranges of input variable until either the result is within 
the required margin of the specified target or the iteration limit is reached 

== USAGE ==

# Search Vars
MARGIN = 1e-5
TARGET = 0.5
DIVS = 20
INITSPAN = [0,pi/2]
FUNC = cos

print implicit_solve(FUNC,TARGET,INITSPAN)

== TODO ==
* write functions to allow the user to define the margin, iteration limit, and divs used by the solver
* Iterate according to convergence rules rather than a set limit?

== LOG ==
2015-10-21: Wrote a generalized wrapper function

== REFERENCES ==
1. URL: http://stackoverflow.com/questions/394809/does-python-have-a-ternary-conditional-operator
"""

# Standard Libraries
from math import *
# Special Libraries
import matplotlib.pyplot as plt
import numpy as np

#iterate = True

# == Helper Functions ==

def arange_clsd(start,end,step):
    """ closed interval 'numpy.arange' """
    rtnList = np.linspace(start,end, ceil((end-start)/float(step)) + 1)
    return rtnList

# == End Helper ==

class IterRange(object):
    """ Bookkeepping for a single range to search for solutions """
    margin = 1e-4
    # arguments given to the class instantiation operator are 
    #passed on to __init__()
    def __init__(self, evalFunc, funcTarget, spanStart, spanEnd, iLim = 5, count = 0):
        self.func = evalFunc # ----------- Function to evaluate at each point in span
        self.target = funcTarget # ------- The value that the function evaluated at solution should take
        self.span = [spanStart, spanEnd] # the span for this solution search
        self.active = True # ------------- whether or not this iteration is active
        self.solnDex = [] # -------------- indices of solutions found within 'results'
        self.solns = [] # ---------------- values of solutions
        self.minima = [] # --------------- indices of error minima in 'diffs'
        self.iterCount = count # --------- Current iteration level
        self.iterLimit = iLim # ---------- Limit of total iterations before stopping
        self.nuSpans = [] # -------------- span for new searches for the next iteration
        
    def check_satisfied(self):
        sat = False
        if( self.iterCount >= self.iterLimit ):
            sat = True
        elif( len(self.solns) > 0 ):
            sat = True
        else:
            for i in self.minima:
                nuStart = 0 if i == 0 else i - 1
                nuEnd   = len(self.diffs) - 1 if i == len(self.diffs) - 1 else i + 1
                self.nuSpans.append( [ self.space[nuStart] , self.space[nuEnd] ] )
        return sat
            
    def iterate(self):
        self.space = arange_clsd( self.span[0] , self.span[1] , (self.span[1] - self.span[0])/(1.0 * DIVS) )
        self.results = map(self.func,self.space)
        self.diffs = map(lambda x: abs(x - self.target), self.results)
        
        # scan for solutions
        for i in range(len(self.diffs)): # For each index of 'diffs'
            # If the error is less than the margin, then
            if self.diffs[i] <= IterRange.margin:
                self.solnDex.append(i) # Append index to solution list
                
        # store solutions
        for dex in self.solnDex:
            self.solns.append( self.space[dex] )
            
        # Find minima
        for i in range(len(self.diffs)):
            if ((i == 0) and (self.diffs[i+1] - self.diffs[i] > 0)):
                self.minima.append(i)
            elif (self.diffs[i-1] - self.diffs[i] > 0) and (self.diffs[i+1] - self.diffs[i] > 0):
                self.minima.append(i)
            elif ((i == len(self.diffs) - 1) and (self.diffs[i-1] - self.diffs[i] > 0)):
                self.minima.append(i)
        
        self.active = not self.check_satisfied() # if stop conditions are satisfied, inactivate
        
    def is_active(self):
        return self.active
        
    def spawn_sub_searches(self):
        rtnRanges = []
        for pair in self.nuSpans:
            rtnRanges.append( IterRange(self.func, self.target, pair[0], pair[1], self.iterLimit, self.iterCount + 1 ) )
        self.active = False
        return rtnRanges
        
    def get_solns(self):
        return self.solns


def implicit_solve(iFunc, iTarget, initSpan, iterLimit = 10, margin = 1e-4):
    IterRange.margin = margin
    searches = [ IterRange(iFunc, iTarget, initSpan[0], initSpan[1], iterLimit) ]
    allSearchesComplete = False
    allSolns = []
    
    while not allSearchesComplete:
        allSearchesComplete = True
        tempSearches = None
        for search in searches:
            if search.is_active():
                allSearchesComplete = False
                search.iterate()
                allSolns.extend(search.get_solns())
                if search.is_active():
                    tempSearches = search.spawn_sub_searches()
                    #print 'extended searches'
        if tempSearches:
            searches.extend(tempSearches)
            
        finalSoln = None
 
    if allSolns:
        allDiffs = map(lambda x: abs(iFunc(x) - iTarget), allSolns)
        finalSoln = allSolns[np.argmin(allDiffs)]
        print "Found solution "+ str(finalSoln) +" with value f(soln) = " + str(iFunc(finalSoln)) + ", and error " + str( allDiffs[np.argmin(allDiffs)] )
    else:
        print "No solutions found"
        
    return finalSoln


# == Abandoned Code ==

#searches = [ IterRange(FUNC, TARGET, initSpan[0], initSpan[1], ITERLIMIT) ]
#allSearchesComplete = False
#allSolns = []
#
#while not allSearchesComplete:
#    allSearchesComplete = True
#    tempSearches = None
#    for search in searches:
#        if search.is_active():
#            allSearchesComplete = False
#            search.iterate()
#            allSolns.extend(search.get_solns())
#            if search.is_active():
#                tempSearches = search.spawn_sub_searches()
#                #print 'extended searches'
#    if tempSearches:
#        searches.extend(tempSearches)
# 
#finalSoln = None
# 
#if allSolns:
#    allDiffs = map(lambda x: abs(FUNC(x) - TARGET), allSolns)
#    finalSoln = allSolns[np.argmin(allDiffs)]
#    print "Found solution "+ str(finalSoln) +" with value f(soln) = " + str(FUNC(finalSoln)) + ", and error " + str( allDiffs[np.argmin(allDiffs)] )
#else:
#    print "No solutions found"

# == End Abandoned ==