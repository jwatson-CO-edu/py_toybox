#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2017-02-09

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
toyGA.py , Built on Wing 101 for Python 2.7
Kanrun Huang & James Watson, 2017 April
Test GA in the simplest case before moving on to Voxelyze
"""

# == Init Environment ======================================================================================================================
import sys, os.path
SOURCEDIR = os.path.dirname( os.path.abspath( __file__ ) ) # URL, dir containing source file: http://stackoverflow.com/a/7783326

# ~~~ Imports ~~~
# ~~ Standard ~~
from math import pi , sqrt
from random import random , choice , randrange
from copy import deepcopy
# ~~ Special ~~
import numpy as np
# ~~ Local ~~

# ~~ Constants , Shortcuts , Aliases ~~
import __builtin__ # URL, add global vars across modules: http://stackoverflow.com/a/15959638/893511
__builtin__.EPSILON = 1e-7
__builtin__.infty = 1e309 # URL: http://stackoverflow.com/questions/1628026/python-infinity-any-caveats#comment31860436_1628026
__builtin__.endl = os.linesep

# == End Init ==============================================================================================================================

# Each Gene defines a list of moves that an agent can take , the goal of the creature is to always move north
POSSIBLE_CODONS = [ "NT" , "ES" , "SO" , "WE" ]

class Gene(object):
    """ The smallest heritable unit """
    codonLen = 4
    
    def __init__( self , codonList ):
        """ Store the parts of the Gene as a list """
        self.codons = codonList[:] # The smallest meaningful component of a gene is called a codon
    
    @classmethod
    def random_Gene( clss ):
        """ Return a gene with a random list of codons """
        return Gene( [ choice( POSSIBLE_CODONS ) for codon in xrange( clss.codonLen ) ] )
    
    def __str__( self ):
        """ String representation of codon list """
        return str( self.codons )
      
class Creature(object):
    """ Simplest creature possible """
    numGenes = 16 # -- The number of genes each creature should have
    mutateProb = 0.3 # The probability of an offspring having a mutation
    
    def __init__( self , genes = None ):
        if genes == None:
            self.genes = [ Gene.random_Gene() for gene in xrange( self.__class__.numGenes ) ]
        else:
            self.genes = deepcopy( genes )
            
    def __str__( self ):
        """ String representation of all the genes in the creature """
        rtnStr = ""
        for gene in self.genes:
            rtnStr += "| " + str( gene ) + " |"
        return rtnStr
    
    def mutate( self ):
        """ Mutate with a chance of 'mutateProb' """
        if random() <= self.__class__.mutateProb: # Random chance to mutate
            self.genes[ randrange( len( self.genes ) ) ] = Gene.random_Gene() # If mutation happens, randonly select a gene to replace with
            #                                                                   a randomized gene
    
    def breed( self , othr ):
        """ Create 2 new Creatures from the genes of this creature and that of 'othr' """
        # NOTE: This function assumes that each genes list has at least 2 elements
        cut1 = randrange( len( self.genes ) - 1 ) # Where cuts will be made for crossover
        cut2 = randrange( cut1 + 1 , len( self.genes ) )
        # Gene crossover for individuals A and B
        geneListA = self.genes[ : cut1 ] + othr.genes[ cut1 : cut2 ] + self.genes[ cut2 : ]
        geneListB = othr.genes[ : cut1 ] + self.genes[ cut1 : cut2 ] + othr.genes[ cut2 : ]
        # Instantiate new individuals A and B
        indA = Creature( geneListA )
        indB = Creature( geneListB )
        # Mutate
        indA.mutate()
        indB.mutate()
        # Individuals are ready to be released into the wild!
        return indA , indB
        
class Population(object):
    """ Manages the evolution of a group of creatures """
    
    def __init__( self , initPop ):
        """ Initialize the population with a list of Creatures 'initPop' """
        assert len( initPop ) % 2 == 0 , "Initial population must have an even number of individuals!"
        self.creatures = initPop # ---- List of all the creatures in the population
        self.popSize = len( initPop ) # The nominal number of creatures in the population
        self.keepFraction = 0.6 # Keep the top 60% every generation
        
    def evaluate_fitness( self , creature ):
        """ Compute a fitness score for one creature """
        cScore = 0
        for gene in creature.genes:
            for codon in gene.codons:
                if codon == "NT":
                    cScore += 1
        creature.score = cScore
        
    def evaluate_all( self ):
        """ Calculate fitness for the entire population """
        for creature in self.creatures:
            self.evaluate_fitness( creature )
            
    def select( self ):
        """ Sort population and remove the least fit creatures """
        self.creatures.sort( key = lambda crtr: crtr.score , reverse = True ) # Sort the creatures according to their fitness score , greatest first
        keepNum = int( self.popSize * self.keepFraction )
        if keepNum % 2 != 0: keepNum -= 1 # Keep the number of individuals even for simplicity
        self.creatures = self.creatures[ : keepNum ] # Erase all but the top 'keepNum' creatures
        
    def repopulate( self ):
        """ Breed the most fit creatures until the original population is restored """
        deficit = self.popSize - len( self.creatures ) # Get the number of creature that have died , they must be replaced!
        print deficit , "creatures have died!"
        for i in xrange( int( deficit / 2 ) ): # For each two missing individuals
            partner1 , partner2 = choice( self.creatures ) , choice( self.creatures ) # Randomly choose two servivors to breed
            while partner1 == partner2: # The two partners should not be the same
                partner2 = choice( self.creatures )
            self.creatures.extend( list( partner1.breed( partner2 ) ) ) # Add two offspring to the population
            
    def generation( self ):
        """ Simulate one generation """
        
        self.evaluate_all() # Measure the performance of the lifetime of each of the creatures
        
        # Print info about the current population
        fitList = [ crtr.score for crtr in self.creatures ] # Fetch a list of all the scores
        totalScore = sum( fitList )
        print
        print "Population:    " , len( self.creatures )
        print "Total Fitness: " , totalScore
        print "Avg. Fitness:  " , totalScore / len( self.creatures )
        
        self.select() # --- Eliminate the least fit creatures
        self.repopulate() # Breed new creatures to replace those that died
        return totalScore / len( self.creatures )

# == Main Application ======================================================================================================================
if __name__ == "__main__":
    # Print a Gene
    foo = Gene.random_Gene()
    print foo.codons
    # Print a genome
    thing = Creature()
    print thing
    
    # Run a simulation
    N = 100 # Number of generations to simulate
    P = 100 # Population size
    pond = Population( [ Creature() for i in xrange( P ) ] ) # Initialize population with 'P' creatures having completely random genomes
    minAvg = 1e20
    maxAvg = 0
    for gen in xrange( N ): # Simulate N generations
        genAvg = pond.generation()
        minAvg = min( minAvg , genAvg )
        maxAvg = max( maxAvg , genAvg )
    print
    print "Simulated" , N , "generations with" , P , "individuals"
    print "Minimum Average:" , minAvg , ", Maximum Average:" , maxAvg

# == End Main ==============================================================================================================================


# == Spare Parts ==



# == End Spare ==