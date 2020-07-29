from figures import Point
from memento import PointContainerMemento
from memento import PlotHistory
import cv2
import copy
from collections import deque
import numpy as np

#drawing = False # true if mouse is pressed
#point = Point(0, 0, 0)
#pointContainer = PointContainerMemento()
#plot = PlotHistory()
#radius = 10
#img = 0








class DrawingMode(object):
    def __init__(self):
        self.point = Point(0, 0, 0)
        self.drawing = False
        self.pointContainer = PointContainerMemento()
        self.radius = 10
        self.plot = PlotHistory()
        self.img = np.zeros((384, 384, 3), np.uint8)

    def draw_circle(self, x, y):
        cv2.circle(self.img, (x, y), self.radius, (0, 0, 255), -1)

    def draw_point(self, event, x, y, flags, param):

        #global point, drawing, pointContainer, radius, plot

        if event == cv2.EVENT_LBUTTONDOWN:
            # set drawing mode
            self.drawing = True

            # create point and point container to append them to history for memento design pattern
            self.point = Point(x, y, self.radius)
            self.pointContainer.points.append(self.point)
            self.plot.history.append(copy.deepcopy(self.pointContainer))

        elif event == cv2.EVENT_MOUSEMOVE:

            if self.drawing == True:
                self.point = Point(x, y, self.radius)
                self.pointContainer.points.append(self.point)
                self.plot.history.append(copy.deepcopy(self.pointContainer))
                self.draw_circle(self.point.x, self.point.y)

        elif event == cv2.EVENT_MOUSEWHEEL:

            if flags > 0:
                self.radius += 2
            else:
                # prevent issues with < 0
                if self.radius > 5:
                    self.radius -= 2

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False

    def draw(self, video_path):

        #global point, drawing, pointContainer, radius, plot, img

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.draw_point)

        cap = cv2.VideoCapture(video_path)
        ret, self.img = cap.read()

        text = 'Press Ctrl+Z to cancel last action'
        cv2.putText(self.img, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        text = 'Use your mousewheel to change radius'
        cv2.putText(self.img, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        text = 'Press E when you finish your drawing'
        cv2.putText(self.img, text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        orig_img = copy.copy(self.img)
        #orig_img = cv2.resize(orig_img, (1250, 750))



        while True:

            cv2.imshow('image', self.img)

            k = cv2.waitKey(1) & 0xFF

            if k == 26:  # ctrl+z
                count = len(self.plot.history) if len(self.plot.history) < 30 else 30

                while count > 0:
                    self.plot.history.pop()
                    count -= 1

                if len(self.plot.history) != 0:
                    current_container = self.plot.history.pop()
                    self.pointContainer = current_container
                    self.img = copy.copy(orig_img)
                    for i in range(len(current_container.points)):
                        cv2.circle(self.img, (current_container.points[i].x, current_container.points[i].y),
                                   current_container.points[i].radius, (0, 0, 255), -1)
                else:
                    self.plot.history = deque()
                    self.img = copy.copy(orig_img)
                    self.pointContainer = PointContainerMemento()
                # orig_img = copy.copy(img)
            elif k == ord('e'):
                break

        cv2.destroyAllWindows()

        return self.plot.history[-1].points


if __name__ == '__main__':
    drawing = DrawingMode()
    points = drawing.draw("videos/videoplayback_cut.mp4")
    print(points)




