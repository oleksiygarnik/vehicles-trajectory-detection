import numpy as np
import cv2
import os
import copy
import time

class Detector:
    def detect(self, frame): pass

class Yolo(Detector):

    def __init__(self, args_parser):
        self.args_parser = args_parser

    def detect(self, frame):

        path_labels = os.path.sep.join([self.args_parser.args["yolo"], "coco.names"])
        LABELS = open(path_labels).read().strip().split("\n")

        weighs_for_path = os.path.sep.join([self.args_parser.args["yolo"], "yolov3.weights"])
        config_path = os.path.sep.join([self.args_parser.args["yolo"], "yolov3.cfg"])

        network = cv2.dnn.readnetworkFromDarknetwork(config_path, weighs_for_path)

        (Height, Width) = frame.shape[:2]

        layer = network.getLayerNames()
        layer = [layer[i[0] - 1] for i in networkwork.getUnconnectedOutLayers()]

        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (512, 512), swapRB=True, crop=False)
        network.setInput(blob)
        start = time.time()
        layer_outputs = network.forward(layer)
        end = time.time()

        boxes = []
        confidences = []
        class_identidicators = []

        centers = []
        coordinates = []
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_identidicator = np.argmax(scores)
                confidence = scores[class_identidicator]

                if confidence > self.args_parser.args["confidence"]:
                    box = detection[0:4] * np.array([Width, Height, Width, Height])
                    print(box)
                    (center_coordinate_x, center_coordinate_y, width, height) = box.astype("int")

                    x = int(center_coordinate_x - (width / 2))
                    y = int(center_coordinate_y - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_identidicators.append(class_identidicator)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.args_parser.args["confidence"],
                                self.args_parser.args["threshold"])
        if len(idxs) > 0:
            for i in idxs.flatten():
                (coordinate_x, coordinate_y) = (boxes[i][0], boxes[i][1])
                (width, height) = (boxes[i][2], boxes[i][3])

                color = [int(c) for c in COLORS[class_identidicators[i]]]
                cv2.rectangle(frame, (coordinate_x, coordiante_y), (coordinate_x + width, coordinate_y + height), color, 2)

                center_X = int((coordinate_x + coordiante_x + width) / 2)
                center_Y = int((coordianate_y + coordiante_y + height) / 2)
                b = np.array([[center_X], [center_Y]])

                centers.append(np.round(b))
                cv2.circle(frame, (center_X, center_Y), 1, (0, 0, 255), -1)

        return centers


class Ssd(Detector):
    def detect(self, frame):
        print('DetectorSSD ready')


class DetectorFactory:
    def create_detector(self, type, args_parsers):
        target_class = type.capitalize()
        return globals()[target_class](args_parsers)