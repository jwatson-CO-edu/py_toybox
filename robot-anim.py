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
                               '/media/jwatson/FILEPILE/Python/ResearchEnv' ] )
from ResearchEnv import * # Load the custom environment
from ResearchUtils.Vector import *
from Tkinter import *
import time

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

def lab_to_screen_transform(labFrameCoords):
    """ Transform natural coordinates in the lab frame to coordinates on the screen display """
    # NOTE: For now assume to handle one pair of coords, not handling the recursive case!
    return [ labFrameCoords[0] , -labFrameCoords[1] ]
    
def lad_coord_chain_to_screen(coordList):
    """ Convert a list of coordinates in the lab frame to the screen frame """
    rtnCoords = []
    for coord in coordList:
        rtnCoords.append( lab_to_screen_transform(coord) )
    return rtnCoords

# = End Rendering =

# == End Iso ==

class Segment(object):
    """ A line segment to be displayed on a Tkinter canvas """
    def __init__(self,bgnPnt,endPnt,TKcanvas=None):
        """ Assign vars and conditionally create the canvas object 'self.drawHandle' """
        self.bgn = bgnPnt
        self.end = endPnt
        if TKcanvas: # If canvas is available at instantiation, go ahead and create the widget
            self.drawHandle = TKcanvas.create_line( bgnPnt[0] , bgnPnt[1] , endPnt[0] , endPnt[1] )
            self.canvas = TKcanvas
    def set_pnts(self,bgnPnt,endPnt):
        """ Set the endpoints as two-element iterables """
        self.bgn = bgnPnt
        self.end = endPnt
    def attach_to_canvas(self, TKcanvas):
        """ Given a 'TKcanvas', create the graphics widget and attach it to the that canvas """
        self.drawHandle = TKcanvas.create_line( bgnPnt[0] , bgnPnt[1] , endPnt[0] , endPnt[1] )
        self.canvas = TKcanvas
    def draw(self):
        """ Update the position of the segment on the canvas """
        self.canvas.coords( self.drawHandle , bgnPnt[0] , bgnPnt[1] , endPnt[0] , endPnt[1] )
        
staticSegments = []  # List of static segments for the simulation, drawn once and never moved again during the simulation
dynamicSegments = [] # List of dynamic segments, subject to movement throughout the simulation

winTitle = 'Robot Sim'
winHeight = 500
winWidth = 500   

# GUI Plan
# 1. Init Tkinter root
rootWin = Tk()
# 2. Set up window
canvas = Canvas(rootWin, width=winWidth, height = winHeight)
# 3. Pack window
canvas.pack()
# 4. Loop function
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