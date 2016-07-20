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
                               'F:\Python\ResearchEnv',
                               '/media/mawglin/FILEPILE/Python/ResearchEnv'] )
from ResearchEnv import * # Load the custom environment
from ResearchUtils.Vector import *

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

def eval_to_float(tokenStr):
    """ Evaluate a token string and attempt conversion to float """
    return float( eval( tokenStr ) )

Span1 = [ 100 ,   0 , 100 ] # extent of link 1 in its own frame
Span2 = [ 100 ,   0 ,   0 ] # extent of link 2 in its own frame

Link1 = Frame( [0.0 , 0.0 , 0.0] , 
               Rotation([0,0,1],0) , 
               Segment( [ [0.0 , 0.0 , 0.0] , Span1  ] ) )
               
print Link1.objs
               
Link2 = Frame( Span1 , 
               Rotation([0,1,0],0) , 
               Segment( [ [0.0 , 0.0 , 0.0] , Span2  ] ) )
               
Link2.parent = Link1

print Link2.objs

looping = True
thetaList = [0.0 for i in range(10)] # FIXME: Maybe don't need this?

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
        angles =  tokenize_with_separator(cmd,',',eval_to_float)
        print angles
        Link1.orientation.set_theta(angles[0])
        print "Link1 theta was set to",Link1.orientation.theta # Link1 theta was set to 1.57079632679
        Link1.transform_contents()
        