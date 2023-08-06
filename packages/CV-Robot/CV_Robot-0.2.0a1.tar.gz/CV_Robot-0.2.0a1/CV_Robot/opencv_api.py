from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from CV_Robot.vision import VisionObject


import matplotlib.pyplot as plt
import numpy as np
import copy
import cv2
import os

from CV_Robot import is_Robot, is_Server

fig = None
ax = None

img_typ = np.ndarray

def load_model():
    """
    Loads Yolo v3 model (called automtically on import)
    """
    yolov3_path = os.path.dirname(__file__) + '/Models/Yolo v3/'
    try:
        with open(yolov3_path + 'yolov3.weights'):
            pass
    except FileNotFoundError:
        print("Downloading model...")
        import wget
        import sys
        def bar_custom(current, total, _): #_ = width
            sys.stdout.write("\r")
            sys.stdout.write("Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total))

        wget.download('https://pjreddie.com/media/files/yolov3.weights', yolov3_path + 'yolov3.weights', bar=bar_custom)
        print()

    net: cv2.dnn_Net = cv2.dnn.readNet(yolov3_path + "yolov3.weights", yolov3_path + "yolov3.cfg")
    with open(yolov3_path + "yolov3.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    output_layers = [layer_name for layer_name in net.getUnconnectedOutLayersNames()]
    return net, classes, output_layers

cache = []
def detect_objects(img: img_typ, net: cv2.dnn_Net, outputLayers: list):
    """
    Returns DNN outputs for finding objects in image, uses cache if possible
    """
    retval = None
    for c_img, c_outputs in cache:
        if np.array_equal(img, c_img):
            retval = c_outputs

    if retval is None:
        blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)
        retval = net.forward(outputLayers)

    if len(cache) >= 5:
        cache.pop(0)
    cache.append((img, retval))

    return retval

def get_box_dimensions(outputs: list, height: int, width: int, thresh: float = 0.3):
    """
    Returns X, Y, width, height of objects
    """
    boxes = []
    confs = []
    class_ids = []
    for output in outputs:
        for detect in output:
            scores = detect[5:]
            class_id = np.argmax(scores)
            conf = scores[class_id]
            if conf > thresh:
                center_x = int(detect[0] * width)
                center_y = int(detect[1] * height)
                w = int(detect[2] * width)
                h = int(detect[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confs.append(float(conf))
                class_ids.append(class_id)
    return boxes, confs, class_ids

def show_image(img: img_typ, pause: bool =False):
    """
    Displays Matplotlib render of image

    If on Colab - display in new figure
    If on Server - display in exisiting figure with optional pause
    If on Robot - save as "cv_robot_img.py"
    """
    global fig
    global ax

    t_img = img[:, :, ::-1]  # convert BGR (for opencv) to RGB (for matplotlib)
    if fig is None or not plt.fignum_exists(fig.number):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot()
    ax.clear()
    ax.imshow(t_img)

    if is_Robot:
        fig.savefig("cv_robot_img.png")
    elif is_Server and not pause:
        plt.draw()
        plt.pause(0.1)
    else:
        plt.show()



def draw_labels(objects: List[VisionObject], img: img_typ, thresh: float = 0.3, pause: bool = False):
    """
    Draw labeled boxes on image
    """
    global fig
    global ax

    boxes = [x.BBox for x in objects]
    confs = [x.Conf for x in objects]

    img = copy.deepcopy(img)
    indexes = cv2.dnn.NMSBoxes(boxes, confs, thresh, thresh)
    font = cv2.FONT_HERSHEY_PLAIN

    for index, obj in enumerate(objects):
        if index in indexes:
            x, y, w, h = obj.BBox
            label = str(obj.Name)
            color = (0,0,255) #red
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y - 5), font, 1, color, 1)

    show_image(img, pause=pause)


