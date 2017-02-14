import multiprocessing
import time

def wait_for_event( e ):
    """Wait for the event to be set before doing anything"""
    print 'wait_for_event: starting'
    e.wait() # ask event 'e' to wait
    print 'wait_for_event: e.is_set()->', e.is_set() # After the waiting is done , query whether the event 'e' is set

def wait_for_event_timeout( e , t ):
    """Wait t seconds and then timeout"""
    print 'wait_for_event_timeout: starting'
    e.wait( t )
    print 'wait_for_event_timeout: e.is_set()->', e.is_set()


if __name__ == '__main__':
    
    e = multiprocessing.Event() # Create an event
    
    # Create a process that calls 'wait_for_event'
    w1 = multiprocessing.Process( name = 'block' , 
                                  target = wait_for_event ,
                                  args = ( e , ) ) 
    w1.start()

    # Create a process that calls 'wait_for_event_timeout'
    w2 = multiprocessing.Process( name = 'non-block' , 
                                  target = wait_for_event_timeout , 
                                  args = ( e , 2 ) )
    w2.start()

    print 'main: waiting before calling Event.set()'
    time.sleep( 3 )
    e.set()
    print 'main: event is set'