from args_parser import ArgsParser
import cv2
import copy
from detector import DetectorFactory
from tracker import Tracker
import numpy as np
from graphic import GraphicBuilder
from events import FinishVideoProcessingEvent
from event_bus import EventBus
import pika
import pickle
import json


class Analyzer(object):
    def __init__(self, object_detector, object_tracker):
        self.object_detector = object_detector
        self.object_tracker = object_tracker

    def analyze(self, video_path, output_video_path, user_id):

        # Create opencv video capture object
        cap = cv2.VideoCapture(video_path)
        writer = None

        # Variables initialization
        skip_frame_count = 0
        track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                        (0, 255, 255), (255, 0, 255), (255, 127, 255),
                        (127, 0, 255), (127, 0, 127)]

        tracks_dictionary = {}

        frame_count = 0
        # Infinite loop to process video frames
        while (True):
            # Capture frame-by-frame
            ret, frame = cap.read()

            if frame is None:
                break

            # necessary to create dictionary
            frame_count += 1

            # Make copy of original frame
            orig_frame = copy.copy(frame)

            # ???????????
            # Skip initial frames that display logo
            if (skip_frame_count < 15):
                skip_frame_count += 1
                continue

            # Detect and return centeroids of the objects in the frame
            centers = self.object_detector.detect(frame)

            # If centroids are detected then track them
            if (len(centers) > 0):

                # Track object using Kalman Filter
                self.object_tracker.update(centers)

                # For identified object tracks draw tracking line
                # Use various colors to indicate different track_id
                for i in range(len(self.object_tracker.tracks)):

                    # check if track is in my dictionary or need to add it
                    if self.object_tracker.tracks[i].track_id not in tracks_dictionary:
                        tracks_dictionary[self.object_tracker.tracks[i].track_id] = {}

                    if (len(self.object_tracker.tracks[i].trace) > 1):
                        # Add frame and coordinates this track on this frame
                        # For Unscented Kalman Filter
                        tracks_dictionary[self.object_tracker.tracks[i].track_id][frame_count] = [
                            self.object_tracker.tracks[i].trace[len(self.object_tracker.tracks[i].trace) - 1][0],
                            self.object_tracker.tracks[i].trace[len(self.object_tracker.tracks[i].trace) - 1][1]]

                        for j in range(len(self.object_tracker.tracks[i].trace) - 1, 1, -1):
                            # For Unscented Kalman Filter
                            x1 = self.object_tracker.tracks[i].trace[j][0]
                            y1 = self.object_tracker.tracks[i].trace[j][1]
                            x2 = self.object_tracker.tracks[i].trace[j - 1][0]
                            y2 = self.object_tracker.tracks[i].trace[j - 1][1]
                            clr = self.object_tracker.tracks[i].track_id % 9
                            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), track_colors[clr], 2)

                            text = "{}".format(self.object_tracker.tracks[i].track_id)
                            cv2.putText(frame, text, (int(self.object_tracker.tracks[i].trace[len(self.object_tracker.tracks[i].trace) - 1][0]),
                                                      int(self.object_tracker.tracks[i].trace[len(self.object_tracker.tracks[i].trace) - 1][
                                                              1] + 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                frame = cv2.resize(frame, (1250, 750))
                cv2.imshow('Tracking', frame)
                # check if the video writer is None
                if writer is None:
                    # initialize our video writer
                    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                    writer = cv2.VideoWriter(output_video_path, fourcc, 30, (frame.shape[1], frame.shape[0]),
                                             True)

                # write the output frame to disk
                writer.write(frame)

            #cv2.waitKey(50)

            # Check for key strokes
            #k = cv2.waitKey(50) & 0xff
            #if k == 27:  # 'esc' key has been pressed, exit program.
            #    break
            #if k == 112:  # 'p' has been pressed. this will pause/resume the code.
            #    pause = not pause
            #    if (pause is True):
            #        print("Code is paused. Press 'p' to resume..")
            #        while (pause is True):
            #            # stay in this loop until
            #            key = cv2.waitKey(30) & 0xff
            #            if key == 112:
            #                pause = False
            #                print("Resume code..!!")
            #                break

        graphic_builder = GraphicBuilder(tracks_dictionary)
        graphic_builder.build()

        finish_video_processing_event = FinishVideoProcessingEvent(output_video_path, graphic_builder.tracks_dictionary, graphic_builder.imagePaths, user_id)

        event_bus = EventBus(finish_video_processing_event)
        event_bus.publish()

        cap.release()
        writer.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    args_parser = ArgsParser()
    args_parser.parse()

    # Create Object Detector
    detectorFactory = DetectorFactory()
    object_detector = detectorFactory.create_detector('yolo', args_parser)

    # Create Object Tracker
    object_tracker = Tracker(100, 5, 5)

    analyzer = Analyzer(object_detector, object_tracker)
    analyzer.analyze('videos/test_occlusion_short_1second.mp4', 'output/readyForRabbit.avi')