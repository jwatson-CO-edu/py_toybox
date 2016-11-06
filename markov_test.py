import numpy as np
import matplotlib.pyplot as plotter

T = np.matrix([[0.5, 0.2, 0.0, 0.0],
               [0.4, 0.1, 0.9, 0.0],
               [0.0, 0.6, 0.0, 0.0],
               [0.1, 0.1, 0.1, 1.0]])

X_LABELS = ['Hungry', 'Got Food', 'Full', 'Dead']

def display_prob(p, t=None):
    '''
    p - probability distribution to
    t - Optional title for the plot
    '''
    xs = range(len(p))
    plotter.bar(xs, p)
    plotter.ylim([0.0,1.0])
    plotter.xlabel(X_LABELS)
    if t is not None:
        plotter.title(t)
    plotter.show()

def run_markov(p0, K = 10):
    '''
    Simulate the Markov chain for K time steps
    Display the distribution over states at each time
    p0 - the initial distribution over states
    K - the number of time steps to run (defaults to 10)
    '''
    p = p0[:]
    Ps = []
    for i in xrange(K):
        display_prob(p,'t='+str(i))
        pn = T*p
        Ps.append(pn)
        p = pn[:]
    display_prob(pn,'t='+str(K))
