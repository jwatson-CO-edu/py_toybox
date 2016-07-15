#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-06-25

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
FrameTest.py , Built on Spyder for Python 2.7
James Watson, 2016 July
Testing representation of reference frames in the simplest implementation possible, find out what is going wrong
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
                               '/media/jwatson/FILEPILE/Python/ResearchEnv',
                               'F:\Python\ResearchEnv' ] )
from ResearchEnv import * # Load the custom environment

# == End Init ==========================================================================================================

def tokenize_with_separator(rawStr,separator,evalFunc=str):
    """ Return a list of tokens taken from 'rawStr' that is partitioned with 'separator', transforming each token with 'evalFunc' """
    tokens = [] # list of tokens to return
    currToken = '' # the current token, built a character at a time
    for char in rawStr: # for each character of the input string
        if not char.isspace(): # if the current char is not whitespace, process
            if not char == separator: # if the character is not a separator, then
                currToken += char # accumulate the char onto the current token
            else: # else the character is a separator, process the previous token
                tokens.append( evalFunc( currToken ) ) # transform token and append to the token list
                currToken = '' # reset the current token
        # else is whitespace, ignore
    if currToken: # If there is data in 'currToken', process it
        tokens.append( evalFunc( currToken ) ) # transform token and append to the token list
    return tokens

Link1 = [ 100 ,   0 , 100 ]
Link2 = [ 100 ,   0 ,   0 ]




looping = True
thetaList = [0.0 for i in range(10)]

while looping:
    cmd = raw_input('Angles or Command: ')
    if cmd == 'q':
        print "Quit"
        looping = False
    elif cmd[0] == 'e':
        try:
            print eval(cmd[2:])
        except BaseException as err:
            print "Your command was not understood!:" , err
    else:
        print tokenize_with_separator(cmd,',',float)