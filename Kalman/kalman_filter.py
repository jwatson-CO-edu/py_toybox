"""
SOURCE: https://towardsdatascience.com/wtf-is-sensor-fusion-part-2-the-good-old-kalman-filter-3642f321440
"""

import numpy as np

"""
(Note that the @ operator is the same as np.matmul in numpy, so A @ B is the same as np.matmul(A, B)).
This was introduced in Python 3.5, you can read more about it here under the Notes section.
"""

class KalmanFilter():
    
    def __init__( self , A , H , Q , R , x_0 , P_0 ):
        """ Set the initial state estimate and measurement """
        
        # Model parameters
        self.A = A
        self.H = H
        self.Q = Q
        self.R = R

        # Initial state
        self._x = x_0
        self._P = P_0

    def predict( self ):
        self._x = self.A @ self._x
        self._P = self.A @ self._P @ self.A.transpose() + self.Q

    def update(self, z):
        self.S = self.H @ self._P @ self.H.transpose() + self.R
        self.V = z - self.H @ self._x
        self.K = self._P @ self.H.transpose() @ np.linalg.inv(self.S)

        self._x = self._x + self.K @ self.V
        self._P = self._P - self.K @ self.S @ self.K.transpose()

    def get_state(self):
        return self._x, self._P
