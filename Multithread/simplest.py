# https://pymotw.com/2/multiprocessing/communication.html

import multiprocessing # This is different from multithreading

class WorkUnit(object):
    """ Object that does a unit of work """
    
    def __init__( self , name ):
        """ Instantiate this object with a name for us to query """
        self.name = name
        
    """ This short example only passes a single message to a single worker, then the main process waits for the worker to finish. """
    def do_something(self):
        """ Identify the object and the process that spawned it """
        proc_name = multiprocessing.current_process().name
        print 'Doing something fancy in %s for %s!' % ( proc_name , self.name ) # Doing something fancy in Process-1 for Fancy Dan!


def worker( workQueue ):
    """ A worker that fetches one object from the work queue and asks it to do some work """
    obj = workQueue.get() # Fetch an object from the Queue
    obj.do_something()


if __name__ == '__main__':
	
    """ A simple way to communicate between process with multiprocessing is to use a Queue to pass messages back and forth. Any pickle-able 
    object can pass through a Queue. """
	
    queue = multiprocessing.Queue() # A Queue for multiprocess communication

    p = multiprocessing.Process( target = worker , args = ( queue , ) ) # spawn a process that runs a function 'worker' with 'args'
    
    p.start() # Call the 'target' function with 'args' inside a threaded process
    
    # Maybe the process is waiting for something to appear in the Queue?
    
    queue.put( WorkUnit('Fancy Dan') ) # Put a work unit in the queue for the process to find
    
    # Wait for the worker to finish
    queue.close() # Close the queue, I guess
    queue.join_thread() # WHAT DOES THIS MEAN
    p.join() # WHAT DOES THIS MEAN

# I guess we are done?