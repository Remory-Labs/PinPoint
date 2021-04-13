import cv2
import numpy as np
import mediapipe as mp
mpPose = mp.solutions.pose

class Detector:
    protopath = "models/MobileNetSSD_deploy.prototxt"
    modelpath = "models/MobileNetSSD_deploy.caffemodel"
    bodyCascade = cv2.CascadeClassifier("models/body.xml")

    net = cv2.dnn.readNetFromCaffe(protopath, modelpath)
    pose =  mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, smooth_landmarks=True) 

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
                recogs.append(bound)

        return recogs

    @staticmethod
    def detectWithMotion(frame):
        #if(Detector.still is None):
        #    raise Exception("Still image is not set, capture a still image first!")
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

                recogs.append(bound)
        return recogs

    @staticmethod
    def detectWithHaarCascade(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        bodies = Detector.bodyCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
        )

        recogs = []
        if(0 < len(bodies)):
            for (x, y, w, h) in bodies:
                bound = (x, y, x + w, y + h)

                recogs.append(bound)
        return recogs

    @staticmethod
    def detectWithBlazePose(frame, showPose=False):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        results = Detector.pose.process(frame)
        
        try:
            h, w = frame.shape[:2]

            converted = []

            for id, landmark in enumerate(results.pose_landmarks.landmark):
                converted.append((int(landmark.x * w), int(landmark.y * h)))

            topX = min(map(lambda a: a[0], converted))
            topY = min(map(lambda a: a[1], converted))
            bottomX = max(map(lambda a: a[0], converted))
            bottomY = max(map(lambda a: a[1], converted))

            return [(topX, topY, bottomX, bottomY)]
        except:
            return []

    def __init__(self):
        pass