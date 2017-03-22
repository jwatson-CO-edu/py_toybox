import numpy as np
import matplotlib.pyplot as plotter
from scipy.spatial import KDTree

def draw_split_dims_recurse(node, mins, maxes):
    '''
    Currently only works for 2D plots
    '''
    if type(node) is KDTree.leafnode:
        return None
    else:
        l_mins = np.copy(mins) # mins will stay the same for lesser
        l_maxes = np.copy(maxes)
        l_maxes[node.split_dim] = node.split
        g_mins = np.copy(mins)
        g_mins[node.split_dim] = node.split
        g_maxes = np.copy(maxes) # Maxes will stay the same for greater
        if node.split_dim == 0:
            xs = [node.split,node.split]
            ys = [mins[1],maxes[1]]
            color_str = 'b-'
        else:
            xs = [mins[0],maxes[0]]
            ys = [node.split,node.split]
            color_str = 'r-'
        plotter.plot(xs,ys,color_str)
        # print xs, ys, color_str

        l_split = draw_split_dims_recurse(node.less, l_mins, l_maxes)
        g_split = draw_split_dims_recurse(node.greater, g_mins, g_maxes)

def draw_split_dims(kd):
    node = kd.tree
    plotter.scatter(kd.data[:,0],kd.data[:,1])
    plotter.xlim((kd.mins[0],kd.maxes[0]))
    plotter.ylim((kd.mins[1],kd.maxes[1]))
    plotter.hold(True)
    mins = np.copy(kd.mins)
    maxes = np.copy(kd.maxes)
    draw_split_dims_recurse(node, mins, maxes)
    plotter.show()


def kd_test(n=30, eps=0, X_max=100, X_min = -100, d=2, k=1, leafsize=1):
    '''
    Simple test method to demonstrate a KD-Tree
    '''

    # Generate n samples of d-dimension, uniformly randomly between X_min and X_max
    X_range = X_max - X_min
    X = np.random.rand(n,d)*X_range + X_min
    # print X

    # Construct the KD-Tree from X
    kd = KDTree(X,leafsize=leafsize)

    # Generate a single sample from the same distribution as X
    y = np.random.rand(d)*X_max + X_min
    print 'y =',y
    # Find the exact nearest neighbor in the KD-Tree
    Q = kd.query(y)
    print Q[1]
    Z = X[Q[1],:]

    # Find the approximate nearest neighbor in the KD-Tree, within a distance eps of the query point
    Q_hat = kd.query(y,k,eps=eps)
    Z_hat = X[Q_hat[1],:]

    # Display the query responses and associated data points
    print 'Q exact =', Q
    print 'Z exact =',Z
    print 'Q_hat =', Q_hat
    print 'Z_hat =',Z_hat

    # Visualize the distribution along the first 2 dimensions
    plotter.scatter(X[:,0],X[:,1])
    plotter.hold(True)
    plotter.plot(y[0],y[1],'yo',label='q')
    plotter.plot(Z[0],Z[1], 'go',label='Z')


    if k == 1:
        plotter.plot(Z_hat[0],Z_hat[1], 'rx',label='Z_hat')
    else:
        for i, z in enumerate(Z_hat):
            if i == 1:
                plotter.plot(z[0],z[1], 'rx',label='Z_hat')
            else:
                plotter.plot(z[0],z[1], 'rx')
    plotter.legend()
    plotter.show()
    draw_split_dims(kd)
    return kd
