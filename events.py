
class StartVideoProcessingEvent(object):
    def __init__(self, user_id):
        self.userId = user_id

class FinishVideoProcessingEvent(object):
    def __init__(self, video_path, tracks_dictionary, images_path, user_id):
        self.UserId = user_id
        self.VideoPath = video_path
        self.ImagePaths = images_path
        self.tracksDictionary = tracks_dictionary
