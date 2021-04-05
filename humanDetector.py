import cv2
import numpy as np
from utility import util

class Detector:
    protopath = "models/MobileNetSSD_deploy.prototxt"
    modelpath = "models/MobileNetSSD_deploy.caffemodel"
    bodyCascade = cv2.CascadeClassifier("models/body.xml")

    net = cv2.dnn.readNetFromCaffe(protopath, modelpath)

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    still = None

    @staticmethod
    def detectWithDNN(frame, confidence = 0.2):
        (H, W) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

        Detector.net.setInput(blob)
        found = Detector.net.forward()

        recogs = []

        for i in range(found.shape[2]):

            conf = found[0, 0, i, 2]
            if confidence < conf:
                idx = int(found[0, 0, i, 1])

                if idx != 15: # Index of humans, in the Models list
                    continue

                bound = (found[0, 0, i, 3:7] * np.array([W, H, W, H])).astype("int")

                center, pin = util.getCenterAndPin(bound)

                recogs.append((center, pin, bound))

        return recogs

    @staticmethod
    def detectWithMotion(frame):
        if(still is None):
            raise Exception("Still image is not set, capture a still image first!")
        pass

    @staticmethod
    def setStillFrame(frame):
        Detector.still = frame

    @staticmethod
    def detectWithHOG(frame):
        found, w = Detector.hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)

        recogs = []
        if(0 < len(found)):
            for (x, y, w, h) in found:
                bound = (x, y, x + w, y + h)
                center, pin = util.getCenterAndPin(bound)

                recogs.append((center, pin, bound))
        return recogs

    @staticmethod
    def detectWithHaarCascade(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        bodies = Detector.bodyCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
        )

        recogs = []
        if(0 < len(bodies)):
            for (x, y, w, h) in bodies:
                bound = (x, y, x + w, y + h)
                center, pin = util.getCenterAndPin(bound)

                recogs.append((center, pin, bound))
        return recogs

    def __init__(self):
        pass