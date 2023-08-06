import CV_Robot.opencv_api as cv_api
from typing import List
import cv2

net, classes, output_layers = cv_api.load_model()
camera = cv2.VideoCapture()
camera_active = False
is_video = False

class Objects:
    STOP_SIGN = 'STOP_SIGN'
    BIKE = 'BIKE'
    CAR = 'CAR'
    TRAFFIC_LIGHT = "TRAFFIC_LIGHT"
    FIRE_HYDRANT = "FIRE_HYDRANT"
    PERSON = "PERSON"
    TRUCK = "TRUCK"

    map = {"stop sign": STOP_SIGN,
         "bicycle": BIKE,
         "car": CAR,
         "traffic light": TRAFFIC_LIGHT,
         "fire hydrant": FIRE_HYDRANT,
         "person": PERSON,
         "truck": TRUCK}

class VisionObject:
    """
    VisionObject - holds information about a recognized object in an image
    Name: Object - type of object
    Size: float - in square pixels
    BBox: list[float] - x, y, width, height
    X: float - center x
    Y: float - center y
    """
    def __init__(self, box: List[float], conf: float, class_id: int):
        self.Name: Objects = Objects.map[classes[class_id]]
        self.Size: float = box[2] * box[3]
        self.BBox = box #x, y, width, height
        self.Conf = conf
        self.X: float = box[0] + box[2] / 2
        self.Y: float = box[1] + box[3] / 2

        self._class_id: int = class_id
        self._class: str = classes[self._class_id]

    def __repr__(self):
        return f"VisionObject<{self.Name}> at ({self.X}, {self.Y})"

def activate_camera():
    """
    Activates the robot camera
    """
    global camera
    global camera_active
    global is_video
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera_active = True
    is_video = False

def get_camera_image(skip_frames = 5):
    """
    Retrieves current image from robot camera or video
    Returns none if the video is done or camera failed
    :param skip_frames: If playing a video, skip ahead this many frames at a time
    """
    global camera
    global camera_active
    if not camera_active:
        raise Exception("Camera is not active. Call vision.activate_camera() or vision.load_video()")
    if is_video:
        for i in range(0, skip_frames):
            camera.read()
    _, img = camera.read()
    return img


def load_image(img_path):
    """
    Loads an image file
    :param img_path: File path to image
    """
    # image loading
    with open(img_path):
        pass #Make sure image exists
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    return img

def load_video(video_path):
    """
    Loads a video file to emulate camera
    :param video_path: File path to video
    """
    global camera
    global camera_active
    global is_video
    with open(video_path):
        pass #Make sure video exists
    camera = cv2.VideoCapture(video_path)
    camera_active = True
    is_video = True

def get_object_locations(image: cv_api.img_typ, thresh: float = 0.3):
    """
    Returns a list of VisionObjects which can be used to find object location and size
    :param image: Image object (from load_image)
    :param thresh: Threshold to identify object, default is 30% (0.3)
    """
    height, width, channels = image.shape
    outputs = cv_api.detect_objects(image, net, output_layers)
    return [VisionObject(*item) for item in zip(*cv_api.get_box_dimensions(outputs, height, width, thresh=thresh))
            if classes[item[2]] in Objects.map.keys()]

def show_objects(image: cv_api.img_typ, thresh: float = 0.3, pause: bool = False):
    """
    Displays image with boxes around objects
    :param image: Image object (from load_image)
    :param thresh: Threshold to identify object, default is 30% (0.3)
    :param pause: Set to true to pause after showing image (only applies to local emulation)
    """
    cv_api.draw_labels(get_object_locations(image, thresh=thresh), image, thresh=thresh, pause=pause)

def find_objects(image: cv_api.img_typ, thresh: float = 0.3):
    """
    Runs machine learning model on image specified, returns list of identified objects
    :param image: Image object (from load_image)
    :param thresh: Threshold to identify object, default is 30% (0.3)
    """
    return list(set(obj.Name for obj in get_object_locations(image, thresh=thresh)))

def show_image(image: cv_api.img_typ, pause: bool = True):
    """
    Displays image
    :param image: Image to display
    :param pause: Set to true to pause after showing image (only applies to local emulation)
    """
    cv_api.show_image(image, pause=pause)
