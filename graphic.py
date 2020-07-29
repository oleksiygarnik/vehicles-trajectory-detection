import numpy as np
import pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import datetime


class Graphic(object):
    def __init__(self, tracks_dictionary):
        self.tracks_dictionary = tracks_dictionary

class GraphicBuilder(object):
    def __init__(self, tracks_dictionary):
        self.tracks_dictionary = tracks_dictionary
        self.x = []
        self.y = []
        self.frame = []
        self.default_path = "C:\\Users\\Алёша\\source\\repos\\VehiclesDataCollection\\ClientAngular\\src\\assets\\"
        self.imagePaths = []

    def build(self):
        fig_all = plt.figure()
        ax_all = fig_all.add_subplot(111, projection='3d')

        full_path = self.generate_path()

        for track_id, value in self.tracks_dictionary.items():

            # create plot for each track
            fig_track = plt.figure()
            ax_track = fig_track.add_subplot(111, projection='3d')

            print("Track_id:", track_id);

            for frame, coordinate in value.items():
                x = coordinate[0]
                y = coordinate[1]

                print("Frame: ", frame, ", Coordinate: ", coordinate[0], coordinate[1])
                self.x.append(coordinate[0])
                self.y.append(coordinate[1])
                self.frame.append(frame)

            ax_all.plot(self.x, self.y, self.frame, label="Track_id: " + str(track_id))
            ax_track.plot(self.x, self.y, self.frame, label="Track_id: " + str(track_id))

            self.reset_configuration()

            plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                       ncol=2, mode="expand", borderaxespad=0.)

            image_path = full_path + '\\track' + str(track_id)

            self.imagePaths.append(image_path)

            fig_track.savefig(image_path)

        #plt.show()
        fig_all.savefig(full_path + '\\all_tracks')

        self.imagePaths.append(full_path + '\\all_tracks')

    def reset_configuration(self):
        self.x = []
        self.y = []
        self.frame = []

    def generate_path(self):
        now = datetime.datetime.now()
        folder_name = str(now.date()) + str(now.time()).replace(":", "_")
        full_path = self.default_path + folder_name

        try:
            os.mkdir(full_path)
        except OSError:
            print("Создать директорию %s не удалось" % full_path)
        else:
            print("Успешно создана директория %s " % full_path)

        return full_path
