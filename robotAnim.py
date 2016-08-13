#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-06-25

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
robotAnim.py , Built on Spyder for Python 2.7
James Watson, 2016 July
Display of a serial manipulator, stick robot
"""

"""
  == NOTES ==
* For now, points and segments will have persistence on the canvas and will be moved on repaint. (That is what Tkinter 
  is made for anyway) For the purposes of this stick robot, world objects will not be subject to rapid creation/distruction 
  or occlusion. Those are concerns for a more complex sim on another day!
* Will not be messing with threads until it becomes absolutely necessary. Calcs will be counted on to finish between
  frames until proven otherwise.
* Target framerate is 25fps, leaving 40ms for calcs and repaint
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
            if drctry not in sys.path:
                sys.path.append( drctry )
                print 'Loaded:', str(drctry)
            else:
                print "Already in sys.path:", str(drctry)
            loadedOne = True
            break
    if not loadedOne:
        print "None of the specified directories were loaded"
# List all the places where the research environment could be
#add_first_valid_dir_to_path( [ '/media/jwatson/FILEPILE/Python/ResearchEnv',
#                               '/home/jwatson/regrasp_planning/researchenv',
#                               'F:\Python\ResearchEnv' ] )
from ResearchEnv import * # Load the custom environment
from ResearchUtils.Vector import *
from Tkinter import *
import time

# == End Init ==========================================================================================================

# == Cheap Iso ==

"""
== Cheap Isometric Projection ==
Three dimensions are represented in a simple isomertic projection. The silhouette of a cube takes on the shape of a regular
hexagon. This is so that no scaling or complex transformations have to take place. All axes have an equal scale in this
representation. Transforming coordinates from R3 to Cheap Iso is just a matter of multiplying each of the components by
a 2D non-orthogonal "basis vector" and adding the resultants.
"""
def cheap_iso_transform(R3triple):
    """ Transform R3 coordinates into a cheap isometric projection in 2D, as described above """
    # NOTE: You will need to scale thye resulting coords according to the need of the application
    return np.multiply( cheap_iso_transform.xBasis , R3triple[0] ) + \
           np.multiply( cheap_iso_transform.yBasis , R3triple[1] ) + \
           np.multiply( cheap_iso_transform.zBasis , R3triple[2] ) # use 'np_add' if this concatenates coords

cheap_iso_transform.zBasis = [ 0.0 , 1.0 ] 
cheap_iso_transform.xBasis = polr_2_cart_0Y( [1.0 , 2.0/3 * pi] )
cheap_iso_transform.yBasis = polr_2_cart_0Y( [1.0 , 1.0/3 * pi] )

# = Rendering Helpers =

# TODO: Consider keeping this global inside the app and adding an offset coord param to the functions below
FLATORIGIN = [0,0] # Set this a handy location for your application

def coord_iso_scrn(isoPair, scale):
    """ Transform natural coordinates in the lab frame to coordinates on the screen display """
    # NOTE: For now assume to handle one pair of coords, not handling the recursive case!
    return  np.add( FLATORIGIN , np.multiply( [ isoPair[0] , -isoPair[1] ] , scale) ) 
    
def chain_iso_scrn(coordList, scale):
    """ Convert a list of coordinates in the lab frame to the screen frame """
    rtnCoords = []
    for coord in coordList:
        rtnCoords.append( coord_iso_scrn(coord, scale) )
    return rtnCoords
    
def coord_R3_scrn(R3triple, scale):
    """ Flatten an R3 triple to the isometric view and transform to screen coords """
    return coord_iso_scrn( cheap_iso_transform(R3triple), scale )
    
def chain_R3_scrn(R3chain, scale):
    """ Flatten a list of R3 triples to the isometric view and transform to screen coords """
    rtnCoords = []
    for triple in R3chain:
        rtnCoords.extend( coord_R3_scrn(triple, scale) )
    return rtnCoords # TODO: Tkinter expects coords as X1 , Y1 , X2 , Y2
    
# = End Rendering =

# == End Iso ==

# 'Segment' moved to ResearchUtils.Vector

class SegmentApp(object):
    """ An Tkinter display to be paired with simple simulations that need line segments displayed """
    
    def __init__(self):
        global FLATORIGIN
        # GUI Plan
        # 1. Init Tkinter root
        #self.staticSegments = []  # List of static segments for the simulation, drawn once and never moved again during the simulation
        #self.dynamicSegments = [] # List of dynamic segments, subject to movement throughout the simulation
        self.winWidth = 500
        self.winHeight = 500
        #self.orgnScale = min( self.winHeight , self.winWidth ) * 2/3.0
        #self.renderScale = 1/2.0
        self.rootWin = Tk()
        self.rootWin.wm_title("Simple Robot Sim")
        self.rootWin.protocol("WM_DELETE_WINDOW", self.callback_destroy)
        self.calcFunc = None # Should really be loaded with something before running
        self.winRunning = False
        # 2. Set up window
        self.canvas = Canvas(self.rootWin, width=self.winWidth, height = self.winHeight)
        self.canvas.config(background='black')
        #self.FLATORIGIN = [30, self.orgnScale]
        self.FLATORIGIN = [self.winWidth/2, self.winHeight/2]
        FLATORIGIN = self.FLATORIGIN
        self.set_stage()
        # 3. Pack window
        self.canvas.grid(row=1, column=1)
        # 3.a. Pack controls
        self.init_controls()

    def set_stage(self): # TODO: Consider making this general for any sort of display simulation, only if needed
        """ Set up the canvas with line segments that will not change throughout the simulation """
        orgnVecs = [ [1,0,0] , [0,1,0] , [0,0,1] ]
        scaledVecs = [ np.multiply( vec , self.orgnScale ) for vec in orgnVecs]
        c = ['red','green','blue']
        for vecDex , vector in enumerate(scaledVecs):
            self.staticSegments.append( Segment( [0,0,0] , vector , TKcanvas=self.canvas, color=c[vecDex]) )
            
    def init_controls(self):
        """ Control sliders """ 
        self.controlPanel = Frame(self.rootWin) # A panel to hold the controls, has its own packing environment
        # Control Sliders
        self.j1_sldr = Scale(self.controlPanel, from_=-170, to=170, orient=HORIZONTAL) #Theta1 > 170 or Theta1 < -170:
        self.j2_sldr = Scale(self.controlPanel, from_=-190, to= 45, orient=HORIZONTAL) #Theta2 >  45 or Theta2 < -190:
        self.j3_sldr = Scale(self.controlPanel, from_=-120, to=156, orient=HORIZONTAL) #Theta3 > 156 or Theta3 < -120:
        self.j4_sldr = Scale(self.controlPanel, from_=-185, to=185, orient=HORIZONTAL) #Theta4 > 185 or Theta4 < -185:
        self.j5_sldr = Scale(self.controlPanel, from_=-120, to=120, orient=HORIZONTAL) #Theta5 > 120 or Theta5 < -120:
        self.j6_sldr = Scale(self.controlPanel, from_=-350, to=350, orient=HORIZONTAL) #Theta6 > 350 or Theta5 < -350:
        # Control Labels
        self.j1_labl = Label(self.controlPanel, text="Joint 1")
        self.j2_labl = Label(self.controlPanel, text="Joint 2")
        self.j3_labl = Label(self.controlPanel, text="Joint 3")
        self.j4_labl = Label(self.controlPanel, text="Joint 4")
        self.j5_labl = Label(self.controlPanel, text="Joint 5")
        self.j6_labl = Label(self.controlPanel, text="Joint 6")
        # Pack all widgets
        self.j1_sldr.grid(row=2, column=1); self.j2_sldr.grid(row=2, column=2); self.j3_sldr.grid(row=2, column=3); # Joint controls 1-3
        self.j1_labl.grid(row=3, column=1); self.j2_labl.grid(row=3, column=2); self.j3_labl.grid(row=3, column=3); # Slider labels  1-3
        self.j4_sldr.grid(row=4, column=1); self.j5_sldr.grid(row=4, column=2); self.j6_sldr.grid(row=4, column=3); # Joint controls 4-6 
        self.j4_labl.grid(row=5, column=1); self.j5_labl.grid(row=5, column=2); self.j6_labl.grid(row=5, column=3); # Slider labels  4-6
        # Init slider values
        self.j1_sldr.set(0); self.j2_sldr.set(-90); self.j3_sldr.set(0);
        self.j4_sldr.set(0); self.j5_sldr.set(0); self.j6_sldr.set(0);
        self.controlPanel.grid(row=1,column=2) # Pack the control panel
    
    def get_sliders_as_list(self):
        """ Return a list of all slider values from j1 to j6 """ 
        return [ self.j1_sldr.get() , self.j2_sldr.get() , self.j3_sldr.get() , self.j4_sldr.get() , self.j5_sldr.get() , self.j6_sldr.get() ]
        
    def callback_destroy(self):
        self.winRunning = False
        self.rootWin.destroy()
        exit()
        
    def run(self):
        # 4. Loop function
        #self.rootWin.mainloop()
        last = -infty
        self.winRunning = True
        while self.winRunning:
            # 4.a. Calc geometry
            self.calcFunc( self.get_sliders_as_list() )
            # 4.b. Send new coords to segments
            # 4.c. Take input from widgets
            # 4.d. Wait remainder of 40ms
            elapsed = time.time() * 1000 - last
            if elapsed < 40:
                time.sleep( (40 - elapsed) / 1000.0 )
            # 4.e. Mark beginning of next loop
            last = time.time() * 1000
            # 4.f. Update window
            if not self.winRunning: # This does not solve the problem of continuing to run after 
                # break
                return # What if I return instead? # TODO: Try this in FrameApp
            self.canvas.update() # don't know how to prevent these from being called again after the window is destroyed
            self.rootWin.update()
    

class FrameApp(object):
    """ A Tkinter display to display a new Frame/link-based robot model """
    
    def __init__(self):
        global FLATORIGIN
        # GUI Plan
        # 1. Init Tkinter root
        #self.staticSegments = []  # List of static segments for the simulation, drawn once and never moved again during the simulation
        #self.dynamicSegments = [] # List of dynamic segments, subject to movement throughout the simulation
        self.winWidth = 500
        self.winHeight = 500
        self.orgnScale = min( self.winHeight , self.winWidth ) * 2/3.0
        self.renderScale = 1/2.0
        self.rootWin = Tk()
        self.rootWin.wm_title("Simple Robot Sim")
        self.rootWin.protocol("WM_DELETE_WINDOW", self.callback_destroy)
        self.calcFunc = None # Should really be loaded with something before running
        self.winRunning = False
        self.simFrame = None # The reference frame that contains all simulated objects
        # 2. Set up window
        self.canvas = Canvas(self.rootWin, width=self.winWidth, height = self.winHeight)
        self.canvas.config(background='black')
        self.FLATORIGIN = [self.winWidth/2, self.winHeight/2]
        FLATORIGIN = self.FLATORIGIN
        self.set_stage()
        # 3. Pack window
        self.canvas.grid(row=1, column=1)
        self.init_controls()
                

    def set_stage(self): # TODO: Consider making this general for any sort of display simulation, only if needed
        """ Set up the canvas with line segments that will not change throughout the simulation """
        orgnVecs = [ [1,0,0] , [0,1,0] , [0,0,1] ] # Orthonormal bases
        scaledVecs = [ np.multiply( vec , self.orgnScale ) for vec in orgnVecs] # Scale the bases for good UI
        c = ['red','green','blue']
        self.staticSegments = []
        print "FrameApp.canvas" , self.canvas , self.canvas.__class__
        for vecDex , vector in enumerate(scaledVecs):
            self.staticSegments.append( Segment( [ [0,0,0] , vector ] , TKcanvas=self.canvas, color=c[vecDex]) )
            
    def init_controls(self):
        """ Control sliders """ 
        self.controlPanel = Frame(self.rootWin) # A panel to hold the controls, has its own packing environment
        # Control Sliders
        self.j1_sldr = Scale(self.controlPanel, from_=-pi, to= pi, orient=HORIZONTAL, resolution=0.05) 
        self.j2_sldr = Scale(self.controlPanel, from_=-pi, to= pi, orient=HORIZONTAL, resolution=0.05) 
        # Control Labels
        self.j1_labl = Label(self.controlPanel, text="Joint 1")
        self.j2_labl = Label(self.controlPanel, text="Joint 2")
        # Pack all widgets
        self.j1_sldr.grid(row=2, column=1); self.j2_sldr.grid(row=2, column=2); # pack sliders
        self.j1_labl.grid(row=3, column=1); self.j2_labl.grid(row=3, column=2); # pack labels
        # Init slider values
        self.j1_sldr.set(0); self.j2_sldr.set(0); 
        self.controlPanel.grid(row=1,column=2) # Pack the control panel
        self.last = -infty

    def get_sliders_as_list(self):
        """ Return a list of all slider values from j1 to j6 """ 
        return [ self.j1_sldr.get() , self.j2_sldr.get() ]
        
    def callback_destroy(self):
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
                
    def report_segments(self, currFrame):
        """ Print the relative and lab poses of each of the serial Segments in the simulation """
        print "Rel:" , currFrame.objs[0].coords
        print "Lab:" , currFrame.objs[0].labCoords
        if len(currFrame.subFrames) < 1:
            print
        else:
            for frame in currFrame.subFrames:
                self.report_frames( frame )

    def run(self):
        # 4. Draw world axes
        for segment in self.staticSegments:
            segment.update()        
        # 4. Loop function
        
        print "Running!"
        
        #pass
        # 4.a. Calc geometry
        self.calcFunc( self.get_sliders_as_list() )
        # 4.b. Send new coords to segments
        self.simFrame.transform_contents() # one of these contains the redundant update
        self.update_Frames( self.simFrame ) # Is this the redundant update?
        # 4.c. Take input from widgets
        
        # 4.f. Update window
        # if not self.winRunning: # This does not solve the problem of continuing to run after 
        #    return # What if I return instead? - SOmetimes still tries to call 'update', but never updates cleanly
        self.canvas.update() # don't know how to prevent these from being called again after the window is destroyed
        self.rootWin.update_idletasks()
        # self.rootWin.update()
        # self.report_frames( self.simFrame ) # List all the Frame states to diagnose transforms
        self.report_segments( self.simFrame ) # List all the Segment states to diagnose transforms
        # 4.d. Wait remainder of 40ms
        elapsed = time.time() * 1000 - self.last
        if elapsed < 40:
            # time.sleep( (40 - elapsed) / 1000.0 )
            sleepTime = int(40 - elapsed) # / 1000.0
        else:
            sleepTime = 0
        # 4.e. Mark beginning of next loop
        self.last = time.time() * 1000    
        print "Sleeping for",sleepTime,"ms"
        self.rootWin.after( sleepTime , self.run )
        # self.rootWin.after( 40 , self.run )

class LinkFrameApp(object):
    """ A Tkinter display to display a new FrameLink-based DH robot model """
    
    def __init__(self):
        global FLATORIGIN
        # 1. Init Tkinter root
        self.winWidth = 500
        self.winHeight = 500
        self.orgnScale = min( self.winHeight , self.winWidth ) * 2/3.0
        self.renderScale = 1/2.0
        self.rootWin = Tk()
        self.rootWin.wm_title("Simple Robot Sim")
        self.rootWin.protocol("WM_DELETE_WINDOW", self.callback_destroy)
        self.calcFunc = None # Should really be loaded with something before running
        self.winRunning = False
        self.simFrame = None # The reference frame that contains all simulated objects
        # 2. Set up window
        self.canvas = Canvas(self.rootWin, width=self.winWidth, height = self.winHeight)
        self.canvas.config(background='black')
        self.FLATORIGIN = [self.winWidth/2, self.winHeight/2]
        FLATORIGIN = self.FLATORIGIN
        self.set_stage()
        # 3. Pack window
        self.canvas.grid(row=1, column=1)
        self.init_controls()
                
    def set_stage(self): # TODO: Consider making this general for any sort of display simulation, only if needed
        """ Set up the canvas with line segments that will not change throughout the simulation """
        orgnVecs = [ [1,0,0] , [0,1,0] , [0,0,1] ] # Orthonormal bases
        scaledVecs = [ np.multiply( vec , self.orgnScale ) for vec in orgnVecs] # Scale the bases for good UI
        c = ['red','green','blue']
        self.staticSegments = []
        dbgLog(-1, "LinkFrameApp.canvas" , self.canvas , self.canvas.__class__)
        for vecDex , vector in enumerate(scaledVecs):
            self.staticSegments.append( Segment( [ [0,0,0] , vector ] , TKcanvas=self.canvas, color=c[vecDex]) )
            
    def init_controls(self):
        """ Control sliders """ 
        self.controlPanel = Frame(self.rootWin) # A panel to hold the controls, has its own packing environment
        # Control Sliders
        self.j1_sldr = Scale(self.controlPanel, from_=-170, to=170, orient=HORIZONTAL) #Theta1 > 170 or Theta1 < -170:
        self.j2_sldr = Scale(self.controlPanel, from_=-190, to= 45, orient=HORIZONTAL) #Theta2 >  45 or Theta2 < -190:
        self.j3_sldr = Scale(self.controlPanel, from_=-120, to=156, orient=HORIZONTAL) #Theta3 > 156 or Theta3 < -120:
        self.j4_sldr = Scale(self.controlPanel, from_=-185, to=185, orient=HORIZONTAL) #Theta4 > 185 or Theta4 < -185:
        self.j5_sldr = Scale(self.controlPanel, from_=-120, to=120, orient=HORIZONTAL) #Theta5 > 120 or Theta5 < -120:
        self.j6_sldr = Scale(self.controlPanel, from_=-350, to=350, orient=HORIZONTAL) #Theta6 > 350 or Theta5 < -350:
        # Control Labels
        self.j1_labl = Label(self.controlPanel, text="Joint 1")
        self.j2_labl = Label(self.controlPanel, text="Joint 2")
        self.j3_labl = Label(self.controlPanel, text="Joint 3")
        self.j4_labl = Label(self.controlPanel, text="Joint 4")
        self.j5_labl = Label(self.controlPanel, text="Joint 5")
        self.j6_labl = Label(self.controlPanel, text="Joint 6")
        # Pack all widgets
        self.j1_sldr.grid(row=2, column=1); self.j2_sldr.grid(row=2, column=2); self.j3_sldr.grid(row=2, column=3); # Joint controls 1-3
        self.j1_labl.grid(row=3, column=1); self.j2_labl.grid(row=3, column=2); self.j3_labl.grid(row=3, column=3); # Slider labels  1-3
        self.j4_sldr.grid(row=4, column=1); self.j5_sldr.grid(row=4, column=2); self.j6_sldr.grid(row=4, column=3); # Joint controls 4-6 
        self.j4_labl.grid(row=5, column=1); self.j5_labl.grid(row=5, column=2); self.j6_labl.grid(row=5, column=3); # Slider labels  4-6
        # Init slider values
        self.j1_sldr.set(0); self.j2_sldr.set(-90); self.j3_sldr.set(0);
        self.j4_sldr.set(0); self.j5_sldr.set(0); self.j6_sldr.set(0);
        self.controlPanel.grid(row=1,column=2) # Pack the control panel
        # Init animation loop timer
        self.last = -infty

    def get_sliders_as_list(self):
        """ Return a list of all slider values from j1 to j6 """ # TODO: ITERATIVE TROUBLESHOOTING
        return [ radians( self.j1_sldr.get() ) , radians( self.j2_sldr.get() ) , radians( self.j3_sldr.get() )  ,
                 radians( self.j4_sldr.get() ) , radians( self.j5_sldr.get() ) , radians( self.j6_sldr.get() ) ]
        
    def callback_destroy(self):
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
                
    def report_segments(self, currFrame):
        """ Print the relative and lab poses of each of the serial Segments in the simulation """
        for obj in currFrame.objs:
            print "Rel:" , obj.coords
            print "Lab:" , obj.labCoords
        if len(currFrame.subFrames) < 1:
            print
        else:
            for frame in currFrame.subFrames:
                self.report_frames( frame )

    def run(self):
        # 4. Draw world axes
        for segment in self.staticSegments:
            segment.update() # TODO: These will never change, draw them safely at the beginning
        # 4. Loop function
        # 4.a. Calc geometry
        self.calcFunc( self.get_sliders_as_list() )
        # 4.b. Send new coords to segments
        self.simFrame.transform_contents() # one of these contains the redundant update
        self.update_Frames( self.simFrame ) # Is this the redundant update?
        # 4.c. Take input from widgets
        
        # 4.f. Update window
        self.canvas.update() 
        self.rootWin.update_idletasks()
        if get_dbg_lvl() == -1:
            self.report_segments( self.simFrame ) # List all the Segment states to diagnose transforms
        # 4.d. Wait remainder of 40ms
        elapsed = time.time() * 1000 - self.last
        if elapsed < 40:
            sleepTime = int(40 - elapsed) 
        else:
            sleepTime = 0
        # 4.e. Mark beginning of next loop
        self.last = time.time() * 1000  
        if get_dbg_lvl() == -1:
            print "Sleeping for",sleepTime,"ms"
        self.rootWin.after( sleepTime , self.run )