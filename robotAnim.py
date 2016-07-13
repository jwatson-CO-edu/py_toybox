#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-06-25

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
robot-anim.py , Built on Spyder for Python 2.7
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
from ResearchUtils.Vector import *
from Tkinter import *
#import time

# == End Init ==========================================================================================================

def polr_2_cart(polarCoords): # TODO: Send this to the Vector module
    """ Convert polar coordinates [radius , angle (radians)] to cartesian [x , y]. Theta = 0 is UP = Y+ """
    return [ polarCoords[0] * sin(polarCoords[1]) , polarCoords[0] * cos(polarCoords[1]) ]
    # TODO : Look into imaginary number transformation and perform a benchmark
    
def cart_2_polr(cartCoords): # TODO: Send this to the Vector module
    """ Convert cartesian coordinates [x , y] to polar coordinates [radius , angle (radians)]. Theta = 0 is UP = Y+ """
    return [ vec_mag(cartCoords) , atan2(-cartCoords[0], cartCoords[1]) ]

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
           np.multiply( cheap_iso_transform.zBasis , R3triple[2] ) # Do I need to use 'np_add'?

cheap_iso_transform.zBasis = [ 0.0 , 1.0 ] 
cheap_iso_transform.xBasis = polr_2_cart( [1.0 , 2.0/3 * pi] )
cheap_iso_transform.yBasis = polr_2_cart( [1.0 , 1.0/3 * pi] )

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
        rtnCoords.append( coord_R3_scrn(R3triple, scale) )
    return rtnCoords
    
# = End Rendering =

# == End Iso ==

class Segment(object):
    """ A line segment to be displayed on a Tkinter canvas """
    def __init__(self,bgnPnt,endPnt,TKcanvas=None, color=None):
        """ Assign vars and conditionally create the canvas object 'self.drawHandle' """
        self.transform = coord_R3_scrn # Optionally change this for a different rendering engine
        self.displayScale = 1/4.0
        self.bgn = self.transform(bgnPnt, self.displayScale)
        self.end = self.transform(endPnt, self.displayScale)
        print self.bgn , self.end
        if TKcanvas: # If canvas is available at instantiation, go ahead and create the widget
            self.canvas = TKcanvas
            self.drawHandle = TKcanvas.create_line( self.bgn[0] , self.bgn[1] , self.end[0] , self.end[1]) 
            print "Item",self.drawHandle,"created on canvas"
            if color:
                self.canvas.itemconfig(self.drawHandle,fill=color)
                print "Item",self.drawHandle,"has color", color
            
    def set_pnts(self,bgnPnt,endPnt):
        """ Set the endpoints as two-element iterables """
        self.bgn = self.transform(bgnPnt, self.displayScale)
        self.end = self.transform(endPnt, self.displayScale)
    def set_color(self, color):
        """ Set the 'color' of the line """
        self.canvas.itemconfig(self.drawHandle,fill=color)
    def attach_to_canvas(self, TKcanvas):
        """ Given a 'TKcanvas', create the graphics widget and attach it to the that canvas """
        self.drawHandle = TKcanvas.create_line( bgnPnt[0] , bgnPnt[1] , endPnt[0] , endPnt[1] ) 
        self.canvas = TKcanvas
    def update(self):
        """ Update the position of the segment on the canvas """
        self.canvas.coords( self.drawHandle , bgnPnt[0] , bgnPnt[1] , endPnt[0] , endPnt[1] )
  

class SegmentApp(object):
    """ An Tkinter display to be paired with simple simulations that need line segments displayed """
    
    def __init__(self):
        global FLATORIGIN
        # GUI Plan
        # 1. Init Tkinter root
        self.staticSegments = []  # List of static segments for the simulation, drawn once and never moved again during the simulation
        self.dynamicSegments = [] # List of dynamic segments, subject to movement throughout the simulation
        self.winWidth = 500
        self.winHeight = 500
        self.orgnScale = min( self.winHeight , self.winWidth ) * 2/3.0
        self.renderScale = 1/2.0
        self.rootWin = Tk()
        self.rootWin.wm_title("Simple Robot Sim")
        # 2. Set up window
        self.canvas = Canvas(self.rootWin, width=self.winWidth, height = self.winHeight)
        self.canvas.config(background='black')
        #self.FLATORIGIN = [30, self.orgnScale]
        self.FLATORIGIN = [self.winWidth/2, self.winHeight/2]
        FLATORIGIN = self.FLATORIGIN
        self.set_stage()
        # 3. Pack window
        self.canvas.pack()

    def set_stage(self): # TODO: Consider making this general for any sort of display simulation, only if needed
        """ Set up the canvas with line segments that will not change throughout the simulation """
        orgnVecs = [ [1,0,0] , [0,1,0] , [0,0,1] ]
        scaledVecs = [ np.multiply( vec , self.orgnScale ) for vec in orgnVecs]
        c = ['red','green','blue']
        for vecDex,vector in enumerate(scaledVecs):
            self.staticSegments.append( Segment( [0,0,0] , vector , TKcanvas=self.canvas, color=c[vecDex]) )
            
    def run(self):
        # 4. Loop function
        self.rootWin.mainloop()
            # 4.a. Calc geometry
            # 4.b. Send new coords to segments
            # 4.c. Take input from widgets
            # 4.d. Wait remainder of 40ms
            # 4.e. Mark beginning of next loop
            # 4.f. Update window
    








"""
import Tkinter

topWin = Tkinter.Tk()

canvas = Tkinter.Canvas(topWin, bg='blue', height=250, width=300)
coord = (10,50,240,210)
arc = canvas.create_arc(coord,start=0,extent=150,fill='red')

canvas.pack()
topWin.mainloop()
"""

"""
class SimApp(object):
     def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=400, height = 400)
        self.canvas.pack()
        self.alien1 = self.canvas.create_oval(20, 260, 120, 360, outline='blue') #,         fill='blue')
        self.alien2 = self.canvas.create_oval(2, 2, 40, 40, outline='red') #, fill='red')
        self.canvas.pack()
        self.root.after(0, self.animation)
        self.root.mainloop()

     def animation(self):
        track = 0
        while True:
            x = 5
            y = 0
            if track == 0:
               for i in range(0,51):
                    time.sleep(0.025)
                    self.canvas.move(self.alien1, x, y)
                    self.canvas.move(self.alien2, x, y)
                    self.canvas.update()
               track = 1
               print "check"

            else:
               for i in range(0,51):
                    time.sleep(0.025)
                    self.canvas.move(self.alien1, -x, y)
                    self.canvas.move(self.alien2, -x, y)
                    self.canvas.update()
               track = 0
            print track

#alien()
"""