#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2017-01-09

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
open_ldb_test01.py , Built on Spyder for Python 2.7
James Watson, YYYY MONTHNAME
A ONE LINE DESCRIPTION OF THE FILE
"""

# == Init Environment ========================================================================================================== 140 char ==
import sys, os.path # To make changes to the PATH

def first_valid_dir(dirList):
    """ Return the first valid directory in 'dirList', otherwise return False if no valid directories exist in the list """
    rtnDir = False
    for drctry in dirList:
        if os.path.exists( drctry ):
			rtnDir = drctry 
			break
    return rtnDir
        
def add_first_valid_dir_to_path(dirList):
    """ Add the first valid directory in 'dirList' to the system path """
    # In lieu of actually installing the library, just keep a list of all the places it could be in each environment
    validDir = first_valid_dir(dirList)
    print __file__ , "is attempting to load a path ...",
    if validDir:
        if validDir in sys.path:
            print "Already in sys.path:", validDir
        else:
            sys.path.append( validDir )
            print 'Loaded:', str(validDir)
    else:
        raise ImportError("None of the specified directories were loaded") # Assume that not having this loaded is a bad thing
# List all the places where the research environment could be
add_first_valid_dir_to_path( [ '/media/jwatson/FILEPILE/ME-6225_Motion-Planning/Assembly_Planner/ResearchEnv',
                               'E:\ME-6225_Motion-Planning\Assembly_Planner\ResearchEnv',
                               '/home/jwatson/regrasp_planning/src/researchenv',
                               '/media/jwatson/FILEPILE/Python/ResearchEnv',
                               'F:\Python\ResearchEnv',
                               'E:\Python\ResearchEnv',
                               '/media/mawglin/FILEPILE/Python/ResearchEnv' ] )

# ~~ Libraries ~~
# ~ Standard Libraries ~
# ~ Special Libraries ~
import leveldb
# ~ Local Libraries ~
from ResearchEnv import * # Load the custom environment, this also loads UCBerkeleyUtil

# Source names must be set AFTER imports!
SOURCEDIR = os.path.dirname( os.path.abspath( __file__ ) ) # URL, dir containing source file: http://stackoverflow.com/a/7783326
SOURCENAM = os.path.split( __file__ )[1]

def rel_to_abs_path( relativePath ):
    """ Return an absolute path , given the 'relativePath' """
    return os.path.join( SOURCEDIR , relativePath )

# == End Init ================================================================================================================== 140 char ==


if __name__ == "__main__":
    # 1. Open the DB
    db = leveldb.LevelDB( "000050.ldb" )





# == Abandoned Code ==
        
"""

"""

# == End Abandoned ==
