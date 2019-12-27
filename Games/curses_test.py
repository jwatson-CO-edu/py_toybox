
# ~~ Imports ~~
import os , sys
from time import time , sleep
from random import randint

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN


# ~~ Path Additions ~~
SOURCEDIR = os.path.dirname( os.path.abspath( '__file__' ) ) # URL, dir containing source file: http://stackoverflow.com/a/7783326
PARENTDIR = os.path.dirname( SOURCEDIR )
sys.path.insert( 0 , PARENTDIR ) # Might need this to fetch a lib in a parent directory
from marchhare.Utils3 import HeartRate
from marchhare.Graph import TaggedObject , TaggedLookup


# ~~ Curses Window ~~
curses.initscr()
win = curses.newwin( 35 , 60 , 1 , 1 )
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

class GridWorld:
    """ Simplest Rectangular Grid World """
    
    def __init__( self , dims ):
        """ Intialize a grid with the specified dimensions """
        self.dims = np.array( dims , dtype = 'int64' )
        self.a_min = np.array( [ 0 for elem in dims ]      , dtype = 'int64' )
        self.a_max = np.array( [ elem-1 for elem in dims ] , dtype = 'int64' )
        
    def is_valid_addr( self , addr ):
        """ Return True if `addr` is within the world grid """
        for i , elem in enumerate( addr ):
            if elem > self.a_max[i]:
                return False
            if elem < self.a_min[i]:
                return False
        return True
    
    def clamp_addr( self , addr ):
        """ Return a version of `addr` that is within the world grid """
        return np.clip( addr , self.a_min , self.a_max )
            
class GridPawn( TaggedObject ):
    """ Pawn in a grid world """
    
    def __init__( self ):
        super().__init__( self )

# ~~ Init ~~   
key    = 1
t_last = time()
rateHz = HeartRate( 30 )

while key != 27:   # While Esc key is not pressed
    win.border(0)
    win.addstr(0, 2, 'Interface Window')
    
    t_now   = time()
    elapsed = t_now - t_last
    win.addstr(0, 25, 'Frame Time:' + str( elapsed ) )
    t_last  = t_now
    
    # Read keystroke
    prevKey = key  # Previous key pressed
    event = win.getch() 
    key = key if event == -1 else event
    
    sleep( 0.010 )  
    
    # Wait remainder of time
    #win.timeout( 40 ) # ms
    rateHz.sleep()
    
# ~~ Cleanup ~~
curses.endwin()