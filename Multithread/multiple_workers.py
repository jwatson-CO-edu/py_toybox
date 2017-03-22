# https://pymotw.com/2/multiprocessing/communication.html

import multiprocessing
import time
import random

""" A more complex example shows how to manage several workers consuming data from a JoinableQueue and passing results back to the parent process. 
The poison pill technique is used to stop the workers. After setting up the real tasks, the main program adds one value per worker to 
the job queue. When a worker encounters the special value, it breaks out of its processing loop. The main process uses the task join() 
method to wait for all of the tasks to finish before processin the results. """

class Consumer(multiprocessing.Process):
    """ This is a Process """
    
    def __init__(self, task_queue, result_queue):
        """ Set up the process with Queues for input and output """
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run( self ):
        """ Do the work """
        proc_name = self.name # Get the name of this process
        while True: # Infinite loop
            next_task = self.task_queue.get() # Fetch a task from the Queue
            if next_task is None: # 'None' is the special Poison pill signal thats means shutdown
                print '%s: Exiting' % proc_name # Notify the user that this process is exiting
                self.task_queue.task_done() # Tell the input queue that this task is done
                break # exit the infinite loop
            print '%s: %s' % ( proc_name , next_task ) # else the task was not the poison pill , tell the user what the next task is
            answer = next_task() # Invoke the next task
            self.task_queue.task_done() # Tell the input queue that this task has been completed
            self.result_queue.put(answer) # 
        return


class Task(object):
    """ Represents busywork for a task consumer to do """
    
    def __init__( self , a , b ):
        """ Store the operands received """
        self.a = a
        self.b = b
        
    def __call__( self ):
        """ Wait for a random time , then multiply the operands """
        time.sleep( 0.3 * random.random() ) # pretend to take some time to do the work , random waits --> random return times
        return '%s * %s = %s' % ( self.a , self.b , self.a * self.b )
    
    def __str__( self ):
        """ Return a representation of the math operationg being performed """
        return '%s * %s' % ( self.a , self.b )


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue() # This is the input queue
    results = multiprocessing.Queue() # ----- This is the output queue
    
    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2 # Assume that there are two possible threads per core
    print 'Creating %d consumers' % num_consumers
    # Create numCores*2 consumers and connect them to the input and output queues
    consumers = [ Consumer( tasks , results ) for i in xrange( num_consumers ) ]
    
    # Start all the consumers
    for w in consumers:
        w.start()
    # Note that we start the consumers (workers) , not the tasks. As soon as we push the tasks onto the queue , started workers will begin
    # consuming the work.
    
    # The input and outpu queue are separate , and the enqueued tasks must not depend on each other
    
    # Enqueue jobs
    num_jobs = 10
    for i in xrange( num_jobs ): # For each of the jobs we want to start
        tasks.put( Task( i , i ) ) # Create a task to square the index , this will make it easy to tell if the results arrive out of order
    
    # Add a poison pill for each consumer
    for i in xrange( num_consumers ): # After all the tasks have been consumed , each worker will consume its pill in turn and die
        tasks.put( None ) 

    # Wait for all of the tasks to finish
    tasks.join()
    
    # Start printing results
    while num_jobs:
        result = results.get()
        print 'Result:', result
        num_jobs -= 1
 
# Program printout , note that the jobs were completed out of order       
"""
Creating 8 consumersConsumer-7: 5 * 5
Consumer-7: 6 * 6
Consumer-7: 9 * 9
Consumer-7: Exiting
Consumer-1: 1 * 1
Consumer-1: Exiting
Consumer-4: 3 * 3
Consumer-4: Exiting
Consumer-3: 2 * 2
Consumer-3: Exiting
Consumer-6: 0 * 0
Consumer-6: Exiting
Consumer-5: 7 * 7
Consumer-5: Exiting
Consumer-8: 8 * 8
Consumer-8: Exiting

Result: 5 * 5 = 25
Result: 6 * 6 = 36
Result: 9 * 9 = 81
Result: 3 * 3 = 9
Result: 1 * 1 = 1
Result: 2 * 2 = 4
Result: 0 * 0 = 0
Result: 7 * 7 = 49
Result: 8 * 8 = 64
Result: 4 * 4 = 16
Consumer-2: 4 * 4
Consumer-2: Exiting
"""