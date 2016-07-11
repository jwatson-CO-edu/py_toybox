#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2016-06-25

# ~~ Future First ~~
from __future__ import division # Future imports must be called before everything else, including triple-quote docs!

"""
robot-anim.py , Built on Spyder for Python 2.7
James Watson, 2016 July
Simple graphics for a simple stick-figure robot
"""

"""
  == NOTES ==
* For now, points and segments will have persistence on the canvas and will be moved on repaint. (That is what Tkinter 
  is made for anyway) For the purposes of this stick robot, world objects will not be subject to rapid creation/distruction 
  or occlusion. Those are concerns for a more complex sim on another day!

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

# == End Init ==========================================================================================================

def lab_to_screen_transform(*labFrameCoords):
    """ Transform natural coordinates in the lab frame to coordinates on the screen display """
    if len(labFrameCoords) == 1:
        pass # FIXME: complete this function
    else:
        for coord in labFrameCoords:
            pass
    return None

def polr_2_cart(polarCoords):
    """ Convert polar coordinates [radius , angle (radians)] to cartesian [x , y]. Theta = 0 is UP = Y+ """
    return [ polarCoords[0] * sin(polarCoords[1]) , polarCoords[0] * cos(polarCoords[1]) ]
    # TODO : Look into imaginary number transformation and perform a benchmark
    
def cart_2_polr(cartCoords):
    """ Convert cartesian coordinates [x , y] to polar coordinates [radius , angle (radians)]. Theta = 0 is UP = Y+ """
    return [ vec_mag(cartCoords) , atan2(-cartCoords[0], cartCoords[1]) ]

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

class Segment(object):
    """ A line segment to be displayed on a Tkinter canvas """
    def __init__(self,bgnPnt,endPnt,TKcanvas):
        """ Assign vars and create the canvas object 'self.drawHandle' """
        self.bgn = bgnPnt
        self.end = endPnt
        self.drawHandle = TKcanvas.create_line( bgnPnt[0] , bgnPnt[1] , endPnt[0] , endPnt[1] )
        self.canvas = TKcanvas
    def set_pnts(self,bgnPnt,endPnt):
        """ Set the endpoints as two-element iterables """
        self.bgn = bgnPnt
        self.end = endPnt
    def draw(self):
        """ Update the position of the segment on the canvas """
        self.canvas.coords( self.drawHandle , bgnPnt[0] , bgnPnt[1] , endPnt[0] , endPnt[1] )
        
staticSegments = []  # List of static segments for the simulation, drawn once and never moved again during the simulation
dynamicSegments = [] # List of dynamic segments, subject to movement throughout the simulation

"""
class Application:
    def __initGUI(self, win):
        ## Window ##
        self.win = win

        ## Initialize Frame ##
        win.grid()
        self.dec = -.5
        self.inc = .5
        self.tickTime = 0.1
        
        ## Canvas ##
        self.canvas = Tkinter.Canvas(root, height=200, width=1000)
        self.canvas.grid(row=2,columnspan=10)
        
    def __init__(self, win):

        self.ep = 0
        self.ga = 2
        self.al = 2
        self.stepCount = 0
        ## Init Gui

        self.__initGUI(win)
        
        # Start GUI
        self.running = True
        self.stopped = False
        self.stepsToSkip = 0
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        
    def exit(self):
        self.running = False
        for i in range(5):
            if not self.stopped:
                time.sleep(0.1)
        try:
            self.win.destroy()
        except:
            pass
        sys.exit(0)
        
    def step(self):

        self.stepCount += 1
        
    def run(self):
        self.stepCount = 0
        self.learner.startEpisode()
        while True:
            minSleep = .01
            tm = max(minSleep, self.tickTime)
            time.sleep(tm)
            self.stepsToSkip = int(tm / self.tickTime) - 1

            if not self.running:
                self.stopped = True
                return
            for i in range(self.stepsToSkip):
                self.step()
            self.stepsToSkip = 0
            self.step()
#          self.robot.draw()
        self.learner.stopEpisode()

    def start(self):
        self.win.mainloop()
        
def run():
    global root
    root = Tkinter.Tk()
    root.title( 'Crawler GUI' )
    root.resizable( 0, 0 )

#  root.mainloop()


    app = Application(root)
    def update_gui():
        app.robot.draw(app.stepCount, app.tickTime)
        root.after(10, update_gui)
    update_gui()

    root.protocol( 'WM_DELETE_WINDOW', app.exit)
    try:
        app.start()
    except:
        app.exit()

"""