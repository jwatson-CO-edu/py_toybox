#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__progname__ = "ROM_scaper.py"
__version__  = "2020.11"
__desc__     = "Nicely scrape ROMs from a friendly website"
"""
James Watson , Template Version: 2018-05-14
Built on Wing 101 IDE for Python 3.6

Dependencies: numpy
"""


"""  
~~~ Developmnent Plan ~~~
[ ] Filter ROM files
    [Y] Find out what files Retro-Arch takes: ZIP and other
[ ] Build full URL paths
[ ] Decide Consoles
    [Y] NES
    [Y] SNES
    [ ] N64
    [ ] Game Boy
    [ ] Genesis
    [ ] Game Gear
    [ ] Dreamcast
    [ ] PS1
    [ ] Arcade
[ ] Create a GENTLE download strategy
"""

##### Init Environment #####################################################################################################################
# ~~~ Prepare Paths ~~~
import sys, os.path
SOURCEDIR = os.path.dirname( os.path.abspath( __file__ ) ) # URL, dir containing source file: http://stackoverflow.com/a/7783326
PARENTDIR = os.path.dirname( SOURCEDIR )
# ~~ Path Utilities ~~
def prepend_dir_to_path( pathName ): sys.path.insert( 0 , pathName ) # Might need this to fetch a lib in a parent directory

# ~~~ Imports ~~~
# ~~ Standard ~~
from math import pi , sqrt
import urllib.request
import re
# ~~ Special ~~
import numpy as np
from bs4 import BeautifulSoup
    
# ~~ Local ~~

# ~~ Constants , Shortcuts , Aliases ~~
EPSILON = 1e-7
infty   = 1e309 # URL: http://stackoverflow.com/questions/1628026/python-infinity-any-caveats#comment31860436_1628026
endl    = os.linesep

# ~~ Script Signature ~~
def __prog_signature__(): return __progname__ + " , Version " + __version__ + ', ' + __desc__ # Return a string representing program



##### Program Functions #####

def ext( fName , CAPS = 1 ):
    """ Return the extension of the path or filename """
    if CAPS:
        return fName.split('.')[-1].upper()
    else:
        return fName.split('.')[-1]
    
def has_ext( fName , extLst ):
    """ Return True if the `fName` has an extension in `extLst`, otherwise return False """
    extUPR = [ ext.upper() for ext in extLst ]
    if ext( fName , CAPS = 1 ) in extUPR:
        return True
    else:
        return False

def recurse_file_page( URL , depth = 0 , ROMlst = [] , acceptExt = [] , _DEBUG = 0 ):
    """ Fetch all files of certain types from `URL` and all subdirectories """
    
    html_page = urllib.request.urlopen( URL )
    soup      = BeautifulSoup( html_page , 'html.parser' )
    fileFiltr = len( acceptExt ) > 0
    
    folders = []
    
    for link in soup.find_all( "a" ):
        currLink = link.get( 'href' )
        if _DEBUG:  
            prefix = '\t' * depth
            print( prefix + currLink )    
        if '..' not in currLink:
            if '.' in currLink:
                if _DEBUG:  print( prefix + "Found file:" , currLink )
                if fileFiltr:
                    if has_ext( currLink , acceptExt ):
                        ROMlst.append( currLink )
                else:
                    ROMlst.append( currLink )
            else:
                if _DEBUG:  print( prefix + "Found file:" , currLink )
                folders.append( currLink )

    if _DEBUG:                
        print( prefix + "Folders:" , folders ) 
        print( prefix + "Files:  " , ROMlst   ) 

    for elem in folders:
        subURL = URL + "/" + elem
        recurse_file_page( subURL , depth+1 , ROMlst , acceptExt = acceptExt )
        
    if depth == 0:
        if _DEBUG:  
            print( "ALL FILES:" , ROMlst )
        print( "Found" , len( ROMlst ) , "files!" )
        if _DEBUG:
            typs = set([])
            for f in ROMlst:
                typs.add( f.split('.')[-1] )
            print( typs )
        return ROMlst
    else:
        print( '.' , end = '' , flush = 1 )
        return None

def format_URL( URL ):
    return URL.replace( ' ' , '%20' )

def gentle_DL( URL_lst , dstDir ):
    """ Download every resource in `URL_lst` and store in `dstDir`, but GENTLY """
    pass

##### Program Classes #####



##### Main Application #####################################################################################################################

##### Program Vars #####
BASEURL  = "https://yomiko.bytex64.net/media/games/"

if __name__ == "__main__":
    print( __prog_signature__() )
    termArgs = sys.argv[1:] # Terminal arguments , if they exist
        
    if 0:
        # 1. Fetch NES ROMs
        ROMURL  = BASEURL + "NES/"    
        NESROMs = recurse_file_page( ROMURL , acceptExt = [ 'nes', 'zip' ] )

    if 1:    
        # 1. Fetch SNES ROMs
        ROMURL  = format_URL( BASEURL + "GoodSNES 204/" )   
        NESROMs = recurse_file_page( ROMURL , acceptExt = [ '7z' ] , _DEBUG = 0 )    




##### Spare Parts ##########################################################################################################################


