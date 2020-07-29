import argparse


# ArgsParser where push all necessary config files
class ArgsParser:

    def __init__(self):
        self.args = []

    def display_info(self):
        print(self.args)

    def parse(self):
        argument_parser = argparse.ArgumentParser()

        argument_parser.add_argument("-im", "--image", required=False,
                                     help="path to input image")
        argument_parser.add_argument("-i", "--input", required=False, default="videos/test_occlusion_short_1second.mp4",
                                     help="path to input video")
        argument_parser.add_argument("-o", "--output", required=False, default="output/readyForRabbit.avi",
                                     help="path to output video")
        argument_parser.add_argument("-y", "--yolo", required=False, default="yolo-coco",
                                     help="base path to YOLO directory")
        argument_parser.add_argument("-c", "--confidence", type=float, default=0.6,
                                     help="minimum probability to filter weak detections")
        argument_parser.add_argument("-t", "--threshold", type=float, default=0.3,
                                     help="threshold when applying non-maximum suppression")
        argument_parser.add_argument("-p", "--prototxt", required=False,
                                     help="path to Caffe 'deploy' prototxt file")
        argument_parser.add_argument("-m", "--model", required=False,
                                     help="path to Caffe pre-trained model")
        # construct arguments in dictionary
        self.args = vars(argument_parser.parse_args())


if __name__ == "__main__":
    args_parser = ArgsParser()
    args_parser.parse()