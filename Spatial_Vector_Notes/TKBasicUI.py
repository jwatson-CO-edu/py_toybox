#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2017-05-30

from __future__ import division # MUST be run before all other expressions , including docstrings!

"""
TKBasicUI.py
James Watson , YYYY MONTHNAME , Written on Spyder 3 / Python 2.7
A ONE LINE DESCRIPTION OF THE FILE

Dependencies: XOS_util.py
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
import os
from math import pi
from Tkinter import Tk , Scale , Frame , HORIZONTAL # Standard Python cross-platform GUI
import time
# ~ Special ~
# ~ Local ~
localPaths = [ os.path.join( "C:" , os.sep , "Users" , "jwatson" , "Documents" , "Python Scripts" ) ] # List of paths to your custom modules
add_valid_to_path( localPaths )

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
        self.setupFuncList  = [ self.dummy_ctrl_Frame ]
        self.UIProvided     = False
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
    
    def dummy_ctrl_Frame( self ):
        """ This function does nothing and only serves to prevent an error if client code does not provide an update function """
        pass
        # ~ Example ~
        # self.jnt1 = Scale( self.controlPanel , from_ = -pi , to = pi , resolution = 0.01 , length = 400 , orient = HORIZONTAL )
        # self.jnt1.pack()
        
    def add_UI_func( self , *UIFunc ):
        """ Add update function(s) to the list to be executed every frame """
        if not self.UIProvided: # If the user has never provided a function , then replace the 
            self.setupFuncList = list( UIFunc )
            self.UIProvided = True
        else:
            self.setupFuncList.extend( UIFunc )
    
    def init_controls( self ):
        """ Init UI here """ 
        self.controlPanel = Frame( self.rootWin ) # A panel to hold the controls, has its own packing environment
        for f in self.setupFuncList:
            f( )
        self.controlPanel.pack() # Remember to pack the control panel!
        
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
    pass

# == End Main ==============================================================================================================================
