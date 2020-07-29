from track import Track
import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.linalg import block_diag


class Tracker(object):
    def __init__(self, dist_thresh, max_frames_to_skip, max_trace_length):
        self.dist_thresh = dist_thresh
        self.max_frames_to_skip = max_frames_to_skip
        self.max_trace_length = max_trace_length
        self.tracks = []
        self.track_id_count = 1

    def update(self, detection_centers):
        # create tracks for initilize
        if len(self.tracks) == 0 :
            for i in range(len(detection_centers)):
                track = Track(detection_centers[i], self.track_id_count)
                self.track_id_count += 1
                self.tracks.append(track)

        # Calculate cost using sum of square distance between
        # predicted vs detected centroids
        N = len(self.tracks)
        M = len(detection_centers)
        cost = np.zeros(shape=(N, M))  # Cost matrix

        # Эвклидовое расстояние почитать
        #diff = self.tracks[0].prediction - detection_centers[0]

        for i in range(len(self.tracks)):
            for j in range(len(detection_centers)):
                try:
                    diff = self.tracks[i].prediction - detection_centers[j]
                    distance = np.sqrt(diff[0][0]*diff[0][0] +
                                       diff[1][0]*diff[1][0])
                    cost[i][j] = distance
                except:
                    pass
        # Let's average the squared ERROR
        cost = (0.5) * cost

        # Using Hungarian Algorithm assign the correct detected measurements
        # to predicted tracks
        assignment = []
        for _ in range(N):
            assignment.append(-1)

        row_ind, col_ind = linear_sum_assignment(cost)

        for i in range(len(row_ind)):
            assignment[row_ind[i]] = col_ind[i]

        # Identify tracks with no assignment, if any
        un_assigned_tracks = []
        for i in range(len(assignment)):
            if (assignment[i] != -1):
                # check for cost distance threshold.
                # If cost is very high then un_assign (delete) the track
                if (cost[i][assignment[i]] > self.dist_thresh):
                    assignment[i] = -1
                    un_assigned_tracks.append(i)
                pass
            else:
                self.tracks[i].skipped_frames += 1

        # If tracks are not detected for long time, remove them
        del_tracks = []
        for i in range(len(self.tracks)):
            if (self.tracks[i].skipped_frames > self.max_frames_to_skip):
                del_tracks.append(i)

        if len(del_tracks) > 0:  # only when skipped frame exceeds max
            for id in del_tracks:
                if id < len(self.tracks):
                    del self.tracks[id]
                    del assignment[id]
                else:
                    print("ERROR: id is greater than length of tracks")

        # Now look for un_assigned detects
        un_assigned_detects = []
        for i in range(len(detection_centers)):
            if i not in assignment:
                un_assigned_detects.append(i)

        # Start new tracks
        if(len(un_assigned_detects) != 0):
            for i in range(len(un_assigned_detects)):
                track = Track(detection_centers[un_assigned_detects[i]], self.track_id_count)
                self.track_id_count += 1
                self.tracks.append(track)

        # Update KalmanFilter state, lastResults and tracks trace
        for i in range(len(assignment)):

            self.tracks[i].KF.KF.predict()

            if(assignment[i] != -1):
                self.tracks[i].skipped_frames = 0
                print("Detection_centers: ", np.array(detection_centers[assignment[i]]))
                print("Detection_centers: ", detection_centers[assignment[i]][0][0])
                coordinate_xy = np.array([ detection_centers[assignment[i]][0][0], detection_centers[assignment[i]][1][0]])
                print(coordinate_xy)

                self.tracks[i].KF.KF.update(coordinate_xy)
                #self.tracks[i].prediction = self.tracks[i].KF.correct(detection_centers[assignment[i]], 1)
            #else:
            #    self.tracks[i].KF.correct()
            #    self.tracks[i].prediction = self.tracks[i].KF.correct(np.array([0, 0]), 0)

            #if(len(self.tracks[i].trace) > self.max_trace_length):
            #    for j in range(len(self.tracks[i].trace) - self.max_trace_length):
            #        del self.tracks[i].trace[j]

            self.tracks[i].prediction = np.array([[self.tracks[i].KF.KF.x[0]], [self.tracks[i].KF.KF.x[1]]])

            self.tracks[i].trace.append(np.array([self.tracks[i].KF.KF.x[0], self.tracks[i].KF.KF.x[1]]))

            #self.tracks[i].trace.append([self.tracks[i].KF.KF.x[0], self.tracks[i].KF.KF.x[1]])
