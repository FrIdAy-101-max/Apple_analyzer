import cv2

from Utils.inferencev2 import AppleDetection
from Utils.publisher import publisher
from time import sleep

if __name__ == '__main__':
    detection = AppleDetection()

    cap = cv2.VideoCapture("Dataset/video_1.mp4")

    while True:
        ret, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        detection_results = detection.loadDetections(frame, fps)
        publisher(detection_results)
        sleep(.25)
