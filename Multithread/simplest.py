# https://pymotw.com/2/multiprocessing/communication.html

import multiprocessing # This is different from multithreading

class MyFancyClass(object):
    
    def __init__(self, name):
        self.name = name
        
    """ This short example only passes a single message to a single worker, then the main process waits for the worker to finish. """
    def do_something(self):
        proc_name = multiprocessing.current_process().name
        print 'Doing something fancy in %s for %s!' % (proc_name, self.name)


def worker( workQueue ):
	"""  """
    obj = workQueue.get() # Fetch an object from the Queue
    obj.do_something()


if __name__ == '__main__':
	
	""" A simple way to communicate between process with multiprocessing is to use a Queue to pass messages back and forth. Any pickle-able 
	object can pass through a Queue. """
	
    queue = multiprocessing.Queue() # A Queue for multiprocess communication

    p = multiprocessing.Process( target = worker , args = ( queue , ) )
    
    p.start()
    
    queue.put( MyFancyClass('Fancy Dan') )
    
    # Wait for the worker to finish
    queue.close()
    queue.join_thread()
    p.join()
