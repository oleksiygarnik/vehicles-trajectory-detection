from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter
from filterpy.kalman import UnscentedKalmanFilter
from filterpy.kalman import MerweScaledSigmaPoints
import numpy as np

# Track for single vehicle
class Track(object):
    def __init__(self, prediction, trackId):
        self.track_id = trackId  # identification of each track object
        self.KF = self.filter('UKF')
        self.prediction = prediction
        self.skipped_frames = 0
        self.trace = []

    def filter(self, type):
        switcher = {
            'KF': KalmanFilterCustom(),
            'UKF': UnscentedKalmanFilterCustom()
        }
        return switcher.get(type, 'Invalid filter')


class UnscentedKalmanFilterCustom(object):
    def __init__(self):
        sigmas = MerweScaledSigmaPoints(4, alpha=.1, beta=2., kappa=1.)
        self.KF = UnscentedKalmanFilter(dim_x=4, dim_z=2, fx=self.f_cv, hx=self.h_cv, dt=1, points=sigmas)
        self.KF.x = np.array([0., 0., 0., 0.])
        self.KF.R = np.diag([0.09, 0.09])
        dt = 1.0
        R_std = 0.35
        Q_std = 0.04
        q = Q_discrete_white_noise(dim=2, dt=dt, var=Q_std ** 2)
        self.KF.Q[0, 0] = q[0, 0]
        self.KF.Q[1, 1] = q[0, 0]
        self.KF.Q[2, 2] = q[1, 1]
        self.KF.Q[3, 3] = q[1, 1]
        self.KF.Q[0, 2] = q[0, 1]
        self.KF.Q[2, 0] = q[0, 1]
        self.KF.Q[1, 3] = q[0, 1]
        self.KF.Q[3, 1] = q[0, 1]
        self.KF.P = np.eye(4) * 500

    def f_cv(self, x, dt):
        F = np.array([[1, 0, dt, 0],
                      [0, 1, 0, dt],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

        return np.dot(F, x)

    def h_cv(self, x):
        return x[[0, 1]]


class KalmanFilterCustom(object):
    def __init__(self):
        self.KF = KalmanFilter(dim_x=4, dim_z=2)
        self.KF.F = np.array([[1, 0, 1, 0],
                              [0, 1, 0, 1],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])

        self.KF.H = np.array([[1, 0, 0, 0],
                              [0, 1, 0, 0]])

        self.KF.R = np.eye(2) * 0.35 ** 2
        q = Q_discrete_white_noise(dim=2, dt=1, var=0.04 ** 2)
        self.KF.Q[0, 0] = q[0, 0]
        self.KF.Q[1, 1] = q[0, 0]
        self.KF.Q[2, 2] = q[1, 1]
        self.KF.Q[3, 3] = q[1, 1]
        self.KF.Q[0, 2] = q[0, 1]
        self.KF.Q[2, 0] = q[0, 1]
        self.KF.Q[1, 3] = q[0, 1]
        self.KF.Q[3, 1] = q[0, 1]

        self.KF.x = np.array([[0, 0, 0, 0]]).T
        self.KF.P = np.eye(4) * 500.

