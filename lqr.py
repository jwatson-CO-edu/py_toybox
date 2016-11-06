import numpy as np
import matplotlib.pyplot as plotter

def dlqr(A, B, Q, R, N, Q_f=None):
    '''
    A - State system matrix
    B - Input system matrix
    Q - Running cost on the state
    R - Running cost on the inputs
    N - Number of time steps to solve over
    Q_f - Final cost on the state, defaults to Q if not specified
    returns - K a list of state-feedback gain matrices
    '''
    if Q_f is None:
        Q_f = Q

    # Setup final costs and storage structures
    P = {}
    K = {}
    P[N] = Q_f

    # Solve backwards in time from N to 0
    n = N
    while n > 0:
        RB_inv = np.linalg.inv(R+B.T*P[n]*B)
        P[n-1] = Q + A.T*P[n]*A - A.T*P[n]*B*RB_inv*B.T*P[n]*A
        K[n-1] = -RB_inv*B.T*P[n]*A
        n -= 1

    return K

def compute_value(X,U,Q,R,Q_f):
    '''
    Compute the LQR value associated with the sequence of states and actions X and U
    with quadratic cost matricies Q, R, and Q_F
    '''
    N = len(X)-1
    V = np.zeros(N+1)
    V[N] = X[N].T*Q_f*X[N]
    n = N-1
    while n >= 0:
        Q_cost = X[n].T*Q*X[n]
        R_cost = U[n].T*R*U[n]
        V[n] = Q_cost + R_cost + V[n+1]
        n -= 1
    return V

def test_lqr(x0, N=20, q=2.0, r=1.0):
    '''
    x0 - initial state to simulate the system from
    N - number of time steps to solve for
    q - cost to put on states as Q = qI
    r - cost to put in controls as R = rI
    '''
    A = np.matrix([[1.0,1.0],
                   [0.0,1.0]])
    B = np.matrix([[0.0],
                   [1.0]])
    Q = q*np.matrix(np.eye(2))
    R = r*np.matrix(np.eye(1))

    # Compute feedback gains
    K = dlqr(A,B,Q,R,N)

    # Simulate system and control forward in time
    X = []
    U = []
    X.append(x0)
    for n in xrange(N):
        U.append(K[n]*X[n])
        X.append(A*X[n] + B*U[n])

    V = compute_value(X,U,Q,R,Q)

    # Convert format of U and X for easier plotting
    Y0 = []
    Y1 = []
    W = []
    for x in X:
        Y0.append(float(x[0][0]))
        Y1.append(float(x[1][0]))
    for u in U:
        W.append(float(u[0]))

    plotter.hold(True)
    plotter.plot(Y0,label='x0')
    plotter.plot(Y1,label='x1')
    plotter.plot(W,label='u')
    plotter.legend()
    plotter.title('States and Control over Time')
    plotter.figure()
    plotter.plot(V,'r')
    plotter.title('V(x,n)')
    plotter.show()
    return X,U
