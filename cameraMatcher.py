from camera import Camera
from humanDetector import Detector
from utility import Util
from pos import Positon
import imutils
import cv2

class Matcher:
    height = None
    cameras = []
    positions = []

    def __init__(self, height, cameras):
        Matcher.height = height
        Matcher.cameras = cameras

        for camera in cameras:
            p = Positon(2)
            Matcher.positions.append(p)

    @staticmethod
    def match():
        results = []

        for camera in Matcher.cameras:
            frame = camera.getFrame()
            bounds = Matcher.getRecs(frame, camera.detectionMethod)
            personPos = None

            for person in bounds:
                personPos = person #TODO DECIDE WHICH ONE IS THE CORRECT ONE

                #print(bounds)

                center, personHeight = Util.getCenterAndHumanPin(personPos, Matcher.height)

                if(len(Matcher.positions[Matcher.cameras.index(camera)].stack) == 0):
                    Matcher.positions[Matcher.cameras.index(camera)].push(center)

                centerAvg = Matcher.positions[Matcher.cameras.index(camera)].avgPos()

                if(Util.calcDistance(center, centerAvg) <= 20 or 2.0 <= Util.getAspectRatio(personPos) <= 3.5):
                    Matcher.positions[Matcher.cameras.index(camera)].push(center)
                recs = (centerAvg, personHeight, personPos)

                results.append((frame, recs))

        return results[:len(Matcher.cameras)]

    @staticmethod
    def getRecs(frame, method):
        #switch = {
        #    "dnn": Detector.detectWithDNN(frame),
        #    "motion": Detector.detectWithMotion(frame),
        #    "hog": Detector.detectWithHOG(frame),
        #    "haar": Detector.detectWithHaarCascade(frame),
        #    "blaze": Detector.detectWithBlazePose(frame)
        #}

        if(method == "dnn"):
            return Detector.detectWithDNN(frame)
        elif(method == "motion"):
            return Detector.detectWithMotion(frame)
        elif(method == "hog"):
            return Detector.detectWithHOG(frame)
        elif(method == "haar"):
            return Detector.detectWithHaarCascade(frame)
        elif(method == "blaze"):
            return Detector.detectWithBlazePose(frame)
        else:
            raise Exception("Detection method not implemented.")
