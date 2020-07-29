from flask import Flask
from flask import render_template
from flask import request, redirect
from werkzeug.utils import secure_filename
from events import StartVideoProcessingEvent
from events import FinishVideoProcessingEvent
from args_parser import ArgsParser
from analyzer import Analyzer
from detector import DetectorFactory
from tracker import Tracker
from event_bus import EventBus
from drawing_mode import DrawingMode
import numpy as np
import pika
import pickle
import json
from flask import render_template
from flask import request, redirect

import os

app = Flask(__name__)


def allowed_video(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    extension = ["JPEG", "JPG", "PNG", "GIF", "MP4"]

    if ext.upper() in extension:
        return True
    else:
        return False


@app.route("/upload-video/<user_id>/<option>", methods=["GET", "POST"])
def upload_image(user_id, option):

    if request.method == "POST":
        if request.files:
            video = request.files["video"]

        if video.filename == "":
            print("No filename")
            return redirect(request.url)

        if allowed_video(video.filename):

            filename = secure_filename(video.filename)
            video.save(os.path.join("C:\\Users\\Алёша\\source\\repos\\VehiclesDataCollection\\ClientAngular\\src\\assets\\", filename))
            #video.save(os.path.join("D:\\StealLog\\", filename))

            #option = request.form["option"]

            #if bool(option) == True:

                #drawing = DrawingMode()
                # need to transfer this points like limitation for smth
                #drawing.draw("C:\\Users\\Алёша\\source\\repos\\VehiclesDataCollection\\ClientAngular\\src\\assets\\" + filename)

            start_video_processing_event = StartVideoProcessingEvent(user_id)
			#body = json.dumps(start_video_processing_event.__dict__)

            #connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            #channel = connection.channel()

            #print(type(self.event))
            #channel.queue_declare(queue='StartVideoProcessingEvent', durable=True)

            #channel.basic_publish(exchange='',
            #                  routing_key='StartVideoProcessingEvent',
            #                  body=body)

            #connection.close()
            event_bus = EventBus(start_video_processing_event)
            event_bus.publish()

            # start analyze stage
            args_parser = ArgsParser()
            args_parser.parse()

            # Create Object Detector
            detector_factory = DetectorFactory()
            object_detector = detector_factory.create_detector('yolo', args_parser)

            # Create Object Tracker
            object_tracker = Tracker(100, 5, 5)

            analyzer = Analyzer(object_detector, object_tracker)
            # analyzer.analyze('videos/test_occlusion_short_1second.mp4', 'output/readyForRabbit.avi', user_id)
            analyzer.analyze("C:\\Users\\Алёша\\source\\repos\\VehiclesDataCollection\\ClientAngular\\src\\assets\\" + filename,
                             "C:\\Users\\Алёша\\source\\repos\\VehiclesDataCollection\\ClientAngular\\src\\assets\\output\\" + filename, user_id)

            print("Video saved")
        else:
            print("That file extension is not allowed")
            return redirect(request.url)

    return "OK"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
