#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2017-05-30

from __future__ import division # MUST be run before all other expressions , including docstrings!

"""
tk_ctrl_test.py
James Watson , 2017 August , Written on Spyder 3 / Python 2.7
See what's up with Tk

Dependencies: SpatialVectorRobot , Pyglet
"""

# == Init ==================================================================================================================================

# ~~ Helpers ~~
def add_valid_to_path( pathList ):
    """ Add all the valid paths in 'pathList' to the Python path """
    import sys , os
    for path in pathList:
        if os.path.isdir( path ):
            sys.path.append( path )
            print "Loaded" , path

# ~~ Imports ~~
# ~ Standard ~
import os , random
from math import pi , cos , sin , degrees , radians
import time # --------- For calculating framerate
from Tkinter import * # Standard Python cross-platform GUI
# ~ Special ~
import numpy as np
import pyglet # --------- Package for OpenGL
from pyglet.gl import * #- OpenGL flags and state machine
from pyglet import clock # Animation timing
# ~ Local ~
localPaths = [ os.path.join( "C:" , os.sep , "Users" , "jwatson" , "Documents" , "Python Scripts" ) ] # List of paths to your custom modules
add_valid_to_path( localPaths )
from SpatialVectorRobot import *

# ~~ Aliases & Shortcuts ~~
infty = float('inf') # infinity
endl  = os.linesep # - Line separator (OS Specific)

# ~~ Setup ~~

# == End Init ==============================================================================================================================


# === TKinter Classes ===

# == class TKBasicApp ==
            
class TKBasicApp(object):
    """ TKinter application GUI """
    
    def __init__( self , winWidth , winHeight , updateHz = 30 , title = "DEFAULT WINDOW TITLE" ):
        # 1. Init Tkinter root
        self.winWidth       = winWidth
        self.winHeight      = winHeight
        self.updateFuncList = [ self.dummy_update ] # Should really be loaded with something before running
        self.funcProvided   = False
        self.winRunning     = False
        self.rootWin        = Tk()
        self.rootWin.wm_title( title ) 
        self.rootWin.protocol( "WM_DELETE_WINDOW" , self.callback_destroy ) # Does this even work?
        # 2. Set the minimum period between frames
        self.stepTime       = 1.0 / updateHz
        self.last           = 0
        # 3. Set up window
        self.init_controls()
        
    def set_title( self , winTitle ):
        """ Set the title for the Tkinter window """
        self.rootWin.wm_title( str( winTitle ) )

    def dummy_update( self ):
        """ This function does nothing and only serves to prevent an error if client code does not provide an update function """
        pass
    
    def add_update_func( self , *updateFunc ):
        """ Add update function(s) to the list to be executed every frame """
        if not self.funcProvided: # If the user has never provided a function , then replace the 
            self.updateFuncList = list( updateFunc )
            self.funcProvided = True
        else:
            self.updateFuncList.extend( updateFunc )
    
    def init_controls( self ):
        """ Init UI here """ 
        self.controlPanel = Frame( self.rootWin ) # A panel to hold the controls, has its own packing environment
        w = Scale( self.controlPanel , from_ = 0 , to = 100 )
        w.pack()
        self.controlPanel.pack()
        
    def callback_destroy( self ):
        """ Ask the window to self-destruct , THIS ALMOST NEVER EXITS CLEANLY """
        self.winRunning = False
        self.rootWin.destroy()
        exit()
            
    def run( self ):
        """ Execute one update cycle and stop """
        
        # Execute the per-cycle work specifed by the user
        for f in self.updateFuncList:
            f() # Please make these lightweight and pertain to UI drawing!
        
        # Update window
        self.rootWin.update_idletasks() # idk , draw or something!
        
        # Wait remainder of period
        elapsed = time.time() * 1000 - self.last
        if elapsed < self.stepTime:
            sleepTime = int( self.stepTime - elapsed ) 
        else:
            sleepTime = 0
        # 4.e. Mark beginning of next loop
        self.last = time.time() * 1000  
        self.rootWin.after( sleepTime , self.run )
        
    

# == End TKBasicApp ==

# === End TKinter ===

# == Main ==================================================================================================================================


if __name__ == "__main__":
    # Create display window , set up camera , begin main event loop
    
    
    
    # 3. Setup the UI
    ctrlWin = TKBasicApp( 600 , 200 , title = "Robot Control Panel" ) # Default refresh rate is 30 Hz
    
    
        
    # ~ Set up animation ~
    def update( ):
        """ Per-frame changes to make prior to redraw """
        pass
        
    # ~~ Run ~~
    ctrlWin.add_update_func( update )
    ctrlWin.rootWin.after( 100 , ctrlWin.run ) # Start the simulation after a 100 ms delay
    ctrlWin.rootWin.mainloop() # --------------- Show window and begin the simulation / animation

# == End Main ==============================================================================================================================

        
# == Spare Parts ===========================================================================================================================
        
#    # ~ Set up 1st cuboid to turn using matrix algebra ~
#    prism2 = Cuboid( 0.5 , 1 , 3 , [ 4 ,  0 ,  0 ] )
#    prism2.rotnByOGL = False
#    prism2.set_center( [ 0.5/2.0 , 1/2.0 , 0 ] )
#    
#    # ~ Set up 1st cuboid to turn using matrix algebra ~
#    prism3 = Cuboid( 0.5 , 1 , 3 , [ 2 ,  0 ,  0 ] )
#    prism3.rotnByOGL = False
#    prism3.set_center( [ 0.5/2.0 , 1/2.0 , 0 ] )
        
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
## ~ Set up 1st cuboid to turn using matrix algebra ~
#prism1 = Cuboid( 0.5 , 1 , 3 , [ 6 ,  0 ,  0 ] )
#prism1.rotnByOGL = False
#
## ~ Set up 2nd cuboid to turn using OGL ~
#prism2 = Cuboid( 1 , 2 , 3 , [  2 ,  0 ,  0 ] )
#prism2.rotnByOGL = True
#prism2.thetaDeg = turnDeg
#prism2.rotAxis = turnAxs
#window = OGL_App( [ CartAxes( 1 ) , prism1 , prism2 ] ) 

# == End Parts =============================================================================================================================