#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Template Version: 2017-05-30

from __future__ import division # MUST be run before all other expressions , including docstrings!

"""
test04_DH_Robot.py
James Watson , 2017 August , Written on Spyder 3 / Python 2.7
Test and control N-DOF kinematics with D-H Parameters

Dependencies: SpatialVectorRobot , Pyglet
"""

"""
%% Test Sequence %%
<clip>
[ ] 3. Implement a Robot from Robot Intro , Forward Kinematics
    |Y| 3.a. Move OGL classes and functions to their own file , Move Tkinter class to its own file - COMPLETE
        !Y! Extend 'TKBasicApp' to have a slider and to retrieve [ q ] - COMPLETE
    | | 3.b. Implement a 2-link robot
        ! ! 3.b.1. Add a sub-panel class to 'TKOGLRobotCtrl'
    | | 3.c. Implement the same robot from (3.b) with DH Parameters (Hollerbach) and generalize
    | | 3.d. Position
    | | 3.e. Speed
    | | 3.f. Acceleration
<\clip>

~~~ TODO ~~~
* Consider a Spatial Geo Primitive that contains transform operations common to all spatial geometry ( WAIT until operations successfully
  implemented in a presently-useful class )

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
from Tkinter import Frame , HORIZONTAL , GROOVE , LEFT , SUNKEN , Scale , TOP , Entry
# ~ Special ~
import numpy as np
#import pyglet # --------- Package for OpenGL
#from pyglet.gl import * #- OpenGL flags and state machine
#from pyglet import clock # Animation timing
# ~ Local ~
localPaths = [ os.path.join( "C:" , os.sep , "Users" , "jwatson" , "Documents" , "Python Scripts" ) ] # List of paths to your custom modules
add_valid_to_path( localPaths )
from SpatialVectorRobot import *
from OGLshapes import *
from TKBasicUI import *

# ~~ Aliases & Shortcuts ~~
infty = float('inf') # infinity
endl  = os.linesep # - Line separator (OS Specific)

# ~~ Setup ~~

# == End Init ==============================================================================================================================


# == class OGL_Robot ==
            
class OGL_Robot( LinkModel ):
    """ Representation of a serial , branched , rigid manipulator expressed in spatial coordinates and displayed using pyglet """
    
    def __init__( self ):
        """ Constructor """
        LinkModel.__init__( self ) # Init parent class
        
    def apply_FK_all( self , qList ):
        """ Apply joint transforms associated with 'qList' to each link , transforming all graphics """
        # NOTE : This method is extremely inefficient and benefits neither from obvious recursive techniques nor elimination of 0-products
        # TODO : Fix the above issues
        for linkDex , link in enumerate( self.links ):
            # link.graphics.xform_spatl( FK( self , linkDex , qList ) )
            link.graphics.xform_homog( FK( self , linkDex , qList ) )
        
# == End OGL_Robot ==
            

# == class TKOGLRobotCtrl ==

class TKOGLRobotCtrl( TKBasicApp ):
    """ Control UI in TK for a robot rendered with Pyglet """
    
    class JointSubpanel( Frame ):
        """ Control sub-panel for manual control of one robot DOF """
        
        def __init__( self , rootApp ):
            """ Set up the subpanel within the root window """
            Frame.__init__( self , rootApp.rootWin , relief = SUNKEN )
            
            if not hasattr( rootApp , 'jntCtrls' ): # If there has been no joint control array initialized
                print "DEBUG:" , "Added joint controls!"
                rootApp.jntCtrls = [] # Create an empty joint control array
            
            # URL , Relief Styles : http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/relief.html
            self.jntScale = Scale( self , from_ = -pi , to = pi , resolution = 0.01 , length = 400 , orient = HORIZONTAL , relief = GROOVE )
            # URL , Tkinter pack geometry : http://effbot.org/tkinterbook/pack.htm
            self.jntScale.pack( side = LEFT )
            # self.value = self.jntScale.get()
            
            
            # URL , Entry Widget : http://effbot.org/tkinterbook/entry.htm
            self.jntEntry = Entry( self )
            self.jntEntry.pack( side = LEFT )
            
            self.pack( side = TOP )
            
            # TODO ,  ; ; Write Entry validation
            #         ; ; Write update callbacks for both Scale and Entry (One changes the other and always sets the overall 'value')
            
            rootApp.jntCtrls.append( self )
            
        def get_val( self ):
            """ Get the q val for this joint control """
            return self.jntScale.get()
    
    def __init__( self , winWidth , winHeight , updateHz = 30 , title = "DEFAULT WINDOW TITLE" , numJoints = 1 ):
        """ Init a the control window , This is the heartbeat of the simulation """
        TKBasicApp.__init__( self , winWidth , winHeight , updateHz , title )
        
        for jnt_i in xrange( numJoints ):
            self.JointSubpanel( self )

    def get_q( self ):
        """ Return an array of slider values corresponding to the user's demanded configuration of the robot """
        rtnArr = []
        for jnt_i in self.jntCtrls:
            rtnArr.append( jnt_i.get_val() )
    
# == End TKOGLRobotCtrl ==


# == Main ==================================================================================================================================

if __name__ == "__main__":
    # Create display window , set up camera , begin main event loop
    
    updateHz = 30.0 # Target frame rate
    updatePeriodSec = 1.0 / updateHz 

    # 1. Set up one link with a rotational joint
    # ~ Set up 1st cuboid to turn using matrix algebra ~
    prism1 = Cuboid( 0.5 , 1 , 3 , [ 6 ,  0 ,  0 ] )
    prism1.rotnByOGL = False
    prism1.set_center( [ 0.5/2.0 , 1/2.0 , 0 ] )
    
    link1 = LinkSpatial( "link1" , 0 ) # This link is attached to the world by a rotational joint
    # link1 = LinkSpatial( "link1" , infty ) # This link is attached to the world by a prismatic joint
    # link1 = LinkSpatial( "link1" , 0.1 ) # This link is attached to the world by a rotational joint
    
    link1.xform = homog_xfrom( np.eye( 3 ) , np.multiply( prism1.center , -1 ) )
    link1.graphics = prism1
    q = 0
    # 1.A. Set up a robot that contains the one link 
    robot = OGL_Robot()
    robot.add_and_attach( link1 ) # Add 'link1' as the base link
    robot.set_q( [ q ] )
    
    
    # 3. Setup the UI
    ctrlWin = TKOGLRobotCtrl( 600 , 200 , title = "Robot Control Panel" ) # Default refresh rate is 30 Hz
    
    # 4. Render!

    window = OGL_App( [ CartAxes( 1 ) , prism1 ] , caption = "1DOF Robot" ) 
    
    # ~ Begin animation ~
    
    # Create a loop with 'schedule_interval'
    # http://nullege.com/codes/show/src%40c%40h%40chemshapes-HEAD%40host%40pygletHG%40contrib%40layout%40examples%40interpreter.py/116/pyglet.clock.schedule_interval/python
    
    # clock.schedule_interval( update , updatePeriodSec ) # update at target frame rate # THIS IS BEING DRIVEN BY TKINTER
    window.set_visible()
    
    # multiprocess sockets   , https://stackoverflow.com/a/6921402/893511
    # twisted python sockets , http://twistedmatrix.com/documents/current/core/examples/#auto0
        
    # ~ Set up animation ~
    def update( ):
        """ Per-frame changes to make prior to redraw """
        global q
        # 1. Update q
        q += pi / 60.0
        # 2. Set q
        robot.set_q( ctrlWin.get_q() )
        # 3. Perform FK
        robot.apply_FK_all( ctrlWin.get_q() )
        
        if not window.has_exit: # TODO : TRY DRIVING THESE INSIDE TKINTER INSTEAD OF THE OTHER WAY AROUND
            window.dispatch_events() # Handle window events
            # clock.tick() # Call the update function
            # glClear( GL_COLOR_BUFFER_BIT )
            window.on_draw() # Redraw the scene
            window.flip()
        
    # ~~ Run ~~
    ctrlWin.add_update_func( update )
    ctrlWin.rootWin.after( 100 , ctrlWin.run ) # Start the simulation after a 100 ms delay
    ctrlWin.rootWin.mainloop() # --------------- Show window and begin the simulation / animation

# == End Main ==============================================================================================================================

        
# == Spare Parts ===========================================================================================================================
        
#    print "Homog Xform:    " , endl , homog_ang_axs( 0 , [ 1 , 0 , 0 ] , [ 0 , 0 , 4 ] )
#    print "Homog Vector:   " , endl , [ 4 , 0 , 0 , 1 ]
#    print "Mult. Homog:    " , endl , np.dot( homog_ang_axs( 0 , [ 1 , 0 , 0 ] , [ 0 , 0 , 4 ] ) , [ 4 , 0 , 0 , 1 ] )
#    print
#    print "Spatial Translation:    " , endl , sp_trn_xfrm( [ 0 , 0 , 4 ] )
#    print "Translate test 1  " , endl , np.dot( sp_trn_xfrm( [ 0 , 0 , 4 ] ) , [ 0 , 0 , 0 , 4 , 0 , 0 ] )
#    print "Translate test 2  " , endl , np.dot( sp_trn_xfrm( [ 0 , 0 , 4 ] ) , [ 4 , 0 , 0 , 0 , 0 , 0 ] )
#    print "Translate test 3  " , endl , np.dot( [ 0 , 0 , 0 , 4 , 0 , 0 ] , sp_trn_xfrm( [ 0 , 0 , 4 ] ) )
#    print "Translate test 4  " , endl , np.dot( [ 4 , 0 , 0 , 0 , 0 , 0 ] , sp_trn_xfrm( [ 0 , 0 , 4 ] ) )

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
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