#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

"""
PolyWorldApp.py , Built on Spyder for Python 2.7
Erik Lindstrom , Adam Sperry , James Watson, 2016 November
Tkinter simulation environment for 2D polygons

== LOG ==


== TODO ==

"""

# ~ Standard Libraries ~
import time # --------- For calculating framerate
from Tkinter import * # Standard Python cross-platform GUI
# ~ Special Libraries ~
import numpy as np
# ~ Local Libraries ~
from Vector2D import SimFrame2D , Segment , Poly2D

# ~~ Constants , Shortcuts , Aliases ~~


# == Poly2D Tkinter App ==

class Poly2DApp(object):
    """ A Tkinter display to display 2D polygon worlds """
    
    def __init__( self , winWidth , winHeight ):
        global FLATORIGIN
        # 1. Init Tkinter root
        self.winWidth = winWidth
        self.winHeight = winHeight
        self.orgnScale = min( self.winHeight , self.winWidth ) * 2/3.0
        self.renderScale = 1 # 1/2.0
        self.rootWin = Tk()
        # self.rootWin.wm_title("Polygon Playground") # No default title
        self.rootWin.protocol("WM_DELETE_WINDOW", self.callback_destroy)
        self.calcFunc = [ self.dummy_calculation ] # Should really be loaded with something before running
        self.winRunning = False
        self.simFrame = SimFrame2D( [ [ -self.winWidth/2 , -self.winHeight/2 ] , [ self.winWidth/2 , self.winHeight/2 ] ] ) 
        self.simFrame.name = "simFrame" # Just in case someone asks
        # 2. Set up window
        self.canvas = Canvas(self.rootWin, width=self.winWidth, height = self.winHeight)
        self.canvas.config(background='black')
        self.FLATORIGIN = [self.winWidth/2, self.winHeight/2]
        FLATORIGIN = self.FLATORIGIN
        self.set_stage()
        # 3. Pack window
        self.canvas.grid(row=1, column=1)
        # self.init_controls()
        self.last = -infty # Init animation loop timer
        self.stepTime = 80 # Number of ms between frames

    def set_title( self , winTitle ):
        """ Set the title for the Tkinter window """
        self.rootWin.wm_title( str( winTitle ) )

    def dummy_calculation(self):
        pass

    def offset_transform(self):
	""" Return the default transformation function to the lab frame """
        def offset(pntList, scale): 
            #print "called offset"
            rtnList = []
            for pnt in pntList:
                rtnList.append( np.add( [ pnt[0] , -pnt[1] ] , self.FLATORIGIN ) )
            #print rtnList
            return rtnList # no actual transformation done to coords
        return offset
                
    def set_stage(self): 
        """ Set up the canvas with line segments that will not change throughout the simulation """
        orgnVecs = [ [1,0] , [0,1] ] # Orthonormal bases
        scaledVecs = [ np.multiply( vec , self.orgnScale ) for vec in orgnVecs] # Scale the bases for good UI
        c = ['red','green']
        self.staticSegments = []
        # dbgLog(-1, "LinkFrameApp.canvas" , self.canvas , self.canvas.__class__)
        for vecDex , vector in enumerate(scaledVecs):
            self.staticSegments.append( Segment( [ [0,0] , vector ] , TKcanvas=self.canvas, color=c[vecDex]) )
            
    def init_controls(self):
        """ Init UI here """ 
        #self.controlPanel = Frame(self.rootWin) # A panel to hold the controls, has its own packing environment
        pass
        
    def callback_destroy(self):
        """ Ask the window to self-destruct """
        self.winRunning = False
        self.rootWin.destroy()
        exit()
    
    def update_Frames(self , currFrame):
        for obj in currFrame.objs:
            obj.update()
        for frame in currFrame.subFrames:
            self.update_Frames( frame )

    def report_frames(self, currFrame):
        """ Print the relative and lab poses of each of the serial frames in the simulation """
        print "Rel:",str(currFrame)
        print "Lab:",str(currFrame.labPose)
        if len(currFrame.subFrames) < 1:
            print
        else:
            for frame in currFrame.subFrames:
                self.report_frames( frame )
    
    def attach_to_canvas( self , drawable ):
        """ Attach a 'drawable' object that is derived from Frame2D to the canvas """
        for obj in drawable.objs: # For each canvas element, assign to the app canvas
            obj.transform = self.offset_transform()
            obj.attach_to_canvas( self.canvas )		
        for subFrm in drawable.subFrames:
            self.attach_to_canvas( subFrm )
    
    def attach_drawables( self , *drawables ):
        """ Attach a 'drawable' object that is derived from Frame2D """
        for drawable in drawables:
            self.simFrame.attach_sub( drawable ) # Attach the Frame2D
            self.attach_to_canvas( drawable )
    	
    def update_all( self ):
        """ Recalc all frames and objects for repainting the window or otherwise obtaining geometric info """
        # 4.a. Calc geometry
        for f in self.calcFunc:
            f(  )
        # 4.b. Send new coords to segments
        self.simFrame.transform_contents() # --- Updates the lab coordinates of all the sub frames
        self.update_Frames( self.simFrame ) # Updates the segments of the updated subframes     
     
    def color_all( self , pColor , rootFrame = None ):
        """ Traverse geometry from the root frame to the all subframes, recursively, setting all graphics to 'pColor' """
        if rootFrame == None: 
            rootFrame = self.simFrame
        if 'colorize' in rootFrame.__dict__:
            rootFrame.colorize(pColor)
        else:
            for obj in rootFrame.objs:
                obj.set_color( pColor )   
        for frame in rootFrame.subFrames:
            self.color_all( pColor , frame )    
	
    def run(self):
#        for segment in self.staticSegments: # Draw world axes
#            segment.update() # These will never change, draw them safely at the beginning
            
        # 4. Loop function
        # 4.a. Calc geometry
        for f in self.calcFunc:
            f()
        # 4.b. Send new coords to segments
        self.simFrame.transform_contents() # one of these contains the redundant update
        self.update_Frames( self.simFrame ) # Is this the redundant update?
        # 4.c. Take input from widgets
        
        # 4.f. Update window
        self.canvas.update() 
        self.rootWin.update_idletasks()
        # 4.d. Wait remainder of 40ms
        elapsed = time.time() * 1000 - self.last
        if elapsed < self.stepTime:
            sleepTime = int( self.stepTime - elapsed ) 
        else:
            sleepTime = 0
        # 4.e. Mark beginning of next loop
        self.last = time.time() * 1000  
        self.rootWin.after( sleepTime , self.run )
	#print "looping"


# === USAGE GUIDE ===

if __name__ == "__main__":
    # File that runs the poly sim should import this library
    # from PolyWorldApp import *

    # Create objects to add to the simulation
    hept = Poly2D.regular( 7 , 200 , [0,0] , np.pi / 17 )
    
    # Write function(s) for stuff to do each frame of the simulation
    def update_shape():
        """ Spin the heptagon, yeah! """
        hept.rotate( -np.pi / 128 )
    
    # ~~ Instantiation ~~
    foo = Poly2DApp( 650 , 500 ) # ----- Create the sim display with a black canvas ( xWidth , yHeight ) pixels
    foo.set_title( "Sim Window Test" ) # This will appear in the top bar of the simulation window
    
    # ~~ Setup ~~
    foo.calcFunc = update_shape # ------ Give the app work to do each frame
    foo.attach_drawables( hept ) # ----- Add Frame2D/Poly objects to the world so that they can be drawn
    foo.color_all( 'green' ) # --------- Default segment color is black 
                                         # TODO: Make a new default color!
    
    # ~~ Run ~~
    foo.update_all( ) # ---------------- Update once before starting the sim so that everything gets placed at the proper lab coordinates
    foo.rootWin.after( 100 , foo.run ) # Start the simulation after a 100 ms delay
    foo.rootWin.mainloop() # ----------- Show window and begin the simulation / animation

# === END GUIDE ===


# == Abandoned Code ==



# == End Abandoned ==