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
    |Y| 3.b. Implement a 2-link robot - COMPLETE
        !Y! 3.b.1. Add a sub-panel class to 'TKOGLRobotCtrl' - COMPLETE , Resolved conflicts with the previous UI design , Although the text
        !Y! Rewrite Cuboid to inherit OGLDrawable - COMPLETE
        !Y! Rewrite CartAxes to inherit OGLDrawable , Such that it can be transformed ( Move with links ) - COMPLETE
        !N! Add axes labels to CartAxes - CANCELLED , Placing text in a 3D world doesn't add anything to the display
        !Y! Develop a way to affix CartAxes to any pose on any link - COMPLETE , See above
        !Y! Compare the analytical sol'n of a 2 link end effector pose to the numerical sol'n
        !L! Test OGL rendering - DEFERRED , This does not currently meet any project goals
        !Y! Repair FK function - COMPLETE , Construction of the transformation matrix was incorrect , constructed the entire sequence of 
            transforms before multiplying
        !Y! Implement an effector frame - COMPLETE
    |L| 3.c. Implement the same robot from (3.b) with DH Parameters (Hollerbach) and generalize - LATER
    |Y| 3.d. Position - COMPLETE , Note that this is done in homogeneous 3D coords , however
    | | 3.e. Speed
        !Y! Consider a Spatial Geo Primitive that contains transform operations common to all spatial geometry - COMPLETE , virtual class OGLDrawable
        ! ! Instantiate a robot , set it in a configuration , and calculate the task-space velocity of the end effector
        ISSUE : THE SIZE OF THE COORDINATE TRANSFORM MATRICES IS INCORRECT (4X4) , IT MUST BE 6X6
            ;Y; Restore the coordinate transforms that were previously written to transform coordinates. These are coordinate transforms 
                for Plucker bases , not positions - COMPLETE , Obtained clarification of formulae and notation from [5] that was less clear in
                [1] and [2] , 2017-09-02 : UNTESTED
            ;Y; Write a function to be called on 'LinkSpatial.__init__' that automatically computes the homogeneous , spatial velocity , 
                and spatial force transforms for the link - COMPLETE , Still unsure if they are correct
        ! ! Compare to analytical sol'n from Intro to Robot (Image 96)
    | | 3.f. Acceleration
        ! ! Instantiate a robot , set it in a configuration and angular velocity , and calculate the task-space acceleration of the end effector
        ! ! Compare to analytical sol'n from Intro to Robot
<\clip>

~~~ TODO ~~~

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

# == class TKOGLRobotCtrl ==

class TKOGLRobotCtrl( TKBasicApp ):
    """ Control UI in TK for a robot rendered with Pyglet """
    
    class JointSubpanel( Frame ):
        """ Control sub-panel for manual control of one robot DOF """
        
        def __init__( self , rootApp ):
            """ Set up the subpanel within the root window """
            Frame.__init__( self , rootApp.rootWin , relief = SUNKEN )
            
            if not hasattr( rootApp , 'jntCtrls' ): # If there has been no joint control array initialized
                # print "DEBUG:" , "Added joint controls!"
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
        # print "DEBUG:" , "There are" , len( self.jntCtrls ) , "joints in the list"
        for jnt_i in self.jntCtrls:
            rtnArr.append( jnt_i.get_val() )
        return rtnArr
    
# == End TKOGLRobotCtrl ==
        
# == class OGL_Robot ==
            
class OGL_Robot( LinkModel ):
    """ Representation of a serial , branched , rigid manipulator expressed in spatial coordinates and displayed using pyglet """
    
    def __init__( self ):
        """ Constructor """
        LinkModel.__init__( self ) # Init parent class
        self.OGLDrawables = [] # --- List of all render models of class OGLDrawable 
        
    def add_link_w_graphics( self , link , graphics , parentName = None ):
        """ Set up the kinematic chain relationship and store the associated graphics """
        # 1. Set up the kinematic chain relationship
        LinkModel.add_and_attach( self , link , parentName )
        # 2. Store the associated graphics
        self.OGLDrawables.append( graphics )
        link.graphics = graphics
        # 3. Create the coordinate axes that this link rotates in
        axes = CartAxes( 1 ) # Default at the origin , Transformation will occur when the link's parent is examined
        self.OGLDrawables.append( axes ) # Add the axes to the list of models
        link.axes = axes # Associate the axes with this link
        # 4. Create an empty container for markers associated with this link
        link.markers = [] # This will hold things like effector frame bases , etc
        
    def create_add_link_w_graphics( self , pName , pPitch , E , r , graphics , parentName = None ):
        """ Create a link , and Set up the kinematic chain relationship and store the associated graphics """
        link = LinkSpatial( pName , pPitch , E , r ) # ----------- 1. Create the link
        self.add_link_w_graphics( link , graphics , parentName ) # 2. Add the link
        
    # TODO : Figure out how to handle the effector frame!
    def add_marker_w_transform( self , linkName , marker , transform ):
        """ Add a OGLDrawable 'marker' to 'linkName' with a relative 'transform' such that it moves with link with an offset """
        link = self.link_ref_by_name( linkName )
        marker.xform = transform
        link.markers.append( marker )
        self.OGLDrawables.append( marker )
        
    def get_graphics_list( self ):
        """ Return a copy of references to all drawables """
        return self.OGLDrawables[:] # This is a shallow copy and intentionally so
    
    def apply_FK_all( self , qList ):
        """ Apply joint transforms associated with 'qList' to each link , transforming all graphics """
        # NOTE : This method is extremely inefficient and benefits neither from obvious recursive techniques nor elimination of 0-products
        # TODO : Fix the above issues
        for linkDex , link in enumerate( self.links ):
            # 1. Apply transform to the link
            linkXform = FK( self , linkDex , qList )
            link.graphics.xform_homog( linkXform )
            # 2. Apply transform to the parent axes # How to do this without rewriting the function
            if link.parent:
                link.axes.xform_homog( np.dot( FK( self , link.parent.linkIndex , qList ) , link.xform ) )
            # 3. If there are markers , apply the transform to the markers
            for mrkr in link.markers:
                mrkr.xform_homog( np.dot( linkXform , mrkr.xform ) )
        
# == End OGL_Robot ==

# == Test Functions ==
    
def analytic_test_04( q , qDot , d1 , a2 , a3 ):
    """ Return the 6DOF task space velocity for the end effector of the robot on Image 96 of Intro to Robotics """
    # FIXME : NEED TO TRANSLATE THE MIDFRAME EVALUATION INTO THE TASK SPACE
    
# == End Test ==

# == Main ==================================================================================================================================

if __name__ == "__main__":
    # Create display window , set up camera , begin main event loop
    
    # ~~ 1. Create robot ~~
    # Robot for the velocity example will be Image 96 / pg. 94 of Intro to Robot Notes
    d1 = a2 = a3 = 2.0 # Create 3 links , all of the same size
    edge = 0.25
    
    robot = OGL_Robot()
    # ~~ 2. Add links ~~
    
    # ~ Link 1 ~
    temp = Cuboid( edge , edge , d1 , [ 0 , 0 , 0 ] )
    temp.add_vertex_offset( [ -edge/2.0 , -edge/2.0 , 0.0 ] )
    # pName , pPitch , E , r , graphics , parentName
    robot.create_add_link_w_graphics( "link1" , 0.0 , 
                                      np.eye( 3 ) , [ 0 , 0 , 0 ] , 
                                      temp , None )
    # ~ Link 2 ~
    temp = Cuboid( a2  , edge , edge , [ 0 , 0 , 0 ] )
    temp.add_vertex_offset( [ 0.0 , -edge/2.0 , -edge/2.0 ] )
    robot.create_add_link_w_graphics( "link2" , 0.0 , 
                                       x_trn( pi/2 ) , [ 0 , 0 , 2 ] , 
                                      temp , "link1" )
    
    # ~ Link 3 ~
    temp = Cuboid( a3  , edge , edge , [ 0 , 0 , 0 ] )
    temp.add_vertex_offset( [ 0.0 , -edge/2.0 , -edge/2.0 ] )
    robot.create_add_link_w_graphics( "link3" , 0.0 , 
                                      np.eye( 3 ) , [ 2 , 0 , 0 ] , 
                                      temp , "link2" )
    
    # ~ Effector Frame ~
    robot.add_marker_w_transform( "link3" , CartAxes( unitLen = 1.0 ) , homog_xfrom( x_trn( -pi/2 ) , [ 2 , 0 , 0 ] ) )
    
    if 0: # Set to 1 to check links and connections
        print robot.link_ref_by_name( "link1" ) , "has parent" , robot.link_ref_by_name( "link1" ).parent
        print robot.link_ref_by_name( "link2" ) , "has parent" , robot.link_ref_by_name( "link2" ).parent
        print robot.link_ref_by_name( "link1" ) == robot.link_ref_by_name( "link2" ).parent
        link1 = robot.link_ref_by_name( "link1" )
        link2 = robot.link_ref_by_name( "link2" )
        print "Link 1 xform" , endl , link1.xform
        print "Link 2 xform" , endl , link2.xform
        print "Link 2 Markers" , link2.markers
    elif 1:
        qTest = [ pi/4 , pi/4 , pi/4 ] # Specify a test config
        qDot  = [ 2.0  , 2.0  , 2.0  ]
        manipJacob = jacobn_manip( robot , 2 , qTest )
        print "Manipulator Jacobian for" , qTest , endl , manipJacob
        print "Effector Velocity for   " , qDot , endl , np.dot( manipJacob , qDot )
    
    # 4. Render!
    # window = OGL_App( [ link1 , link1axis , link2 , effectorAxis , CartAxes( 1 ) ] , caption = "Transformation Test" ) 
    window = OGL_App( robot.get_graphics_list() , caption = "Transformation Test" ) 
    window.set_camera( [ 4 , 4 , 4 ] , [ 0 , 0 , 0 ] , [ 0 , 0 , 1 ] )
    
    # ~ Begin animation ~
    window.set_visible()
    
    # ~ Set up animation ~
    def update( ):
        """ Per-frame changes to make prior to redraw """
        q = ctrlWin.get_q()
        robot.apply_FK_all( q )
        if not window.has_exit: 
            window.dispatch_events() # Handle window events
            window.on_draw() # Redraw the scene
            window.flip()
        
    ctrlWin = TKOGLRobotCtrl( 600 , 200 , title = "Transform Test" , numJoints = 3 ) # Default refresh rate is 30 Hz
        
    # ~~ Run ~~
    ctrlWin.add_update_func( update )
    ctrlWin.rootWin.after( 100 , ctrlWin.run ) # Start the simulation after a 100 ms delay
    ctrlWin.rootWin.mainloop() # --------------- Show window and begin the simulation / animation

# == End Main ==============================================================================================================================
    

        
# == Spare Parts ===========================================================================================================================

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#def analytic_test_B( q , d1 , a2 ):
#    """ Return the analytic transform for the effector frame for comparision to the numerical solution """
#    th1 = q[0]; th2 = q[1]
#    return [ [  cos( th1 ) * cos( th2 ) , -cos( th1 ) * sin( th2 ) ,  sin( th1 ) , a2 * cos( th1 ) * cos( th2 ) ] , 
#             [  sin( th1 ) * cos( th2 ) , -sin( th1 ) * sin( th2 ) , -cos( th1 ) , a2 * sin( th1 ) * cos( th2 ) ] , 
#             [  sin( th2 )              , cos( th2 )              ,  0          , d1 + a2 * sin( th2 )         ] , 
#             [  0                       , 0                       ,  0          , 1                            ] ]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#    def transform_Points( q ):
#        """ Apply the appropriate transformations to the links , In the future this will be taken care of by FK """
#        global link1pts , link2pts
#        xform1 = homog_xfrom( z_trn( q[0] ) , [ 0 , 0 , 0 ] )
#        jtXfrm = homog_xfrom( x_trn( pi/2 ) , [ 0 , 0 , 2 ] )
#        xform2 = homog_xfrom( z_trn( q[1] ) , [ 0 , 0 , 0 ] )
#        efXfrm = homog_xfrom( np.eye( 3 )   , [ 2 , 0 , 0 ] )
#        # combined = np.dot( xform1 , xform2 )
#        combined1 = np_dot( xform1 , jtXfrm )
#        combined2 = np_dot( xform1 , jtXfrm , xform2 )
#        combined3 = np_dot( xform1 , jtXfrm , xform2 , efXfrm )
#        link1.xform_homog( xform1 )
#        link1axis.xform_homog( combined1 )
#        link2.xform_homog( combined2 )
#        effectorAxis.xform_homog( combined3 )
#        print np.sum( np.subtract( combined3 , analytic_test_B( q , 2.0 , 2.0 ) ) )

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create a loop with 'schedule_interval'
# http://nullege.com/codes/show/src%40c%40h%40chemshapes-HEAD%40host%40pygletHG%40contrib%40layout%40examples%40interpreter.py/116/pyglet.clock.schedule_interval/python

# clock.tick() # Call the update function
# glClear( GL_COLOR_BUFFER_BIT )
    
# clock.schedule_interval( update , updatePeriodSec ) # update at target frame rate # THIS IS BEING DRIVEN BY TKINTER
    
# multiprocess sockets   , https://stackoverflow.com/a/6921402/893511
# twisted python sockets , http://twistedmatrix.com/documents/current/core/examples/#auto0
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
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