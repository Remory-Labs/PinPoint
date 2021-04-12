from camera import Camera
from humanDetector import Detector
from utility import Util
from pos import Positon

class Matcher:
    height = None
    cameras = []
    positions = []

    def __init__(self, height, cameras):
        Matcher.height = height
        Matcher.cameras = cameras

        for camera in cameras:
            p = Positon(8)
            Matcher.positions.append(p)

    @staticmethod
    def calcPosition():
        results = []

        for i in range(len(Matcher.cameras)):
            frame = Matcher.cameras[i].getFrame(500)
            bounds = Matcher.getRecs(frame, Matcher.cameras[i].detectionMethod)

            if(len(bounds) == 0):
                if(Matcher.positions[i].vector != None):
                    results.append((frame, (Matcher.positions[i].positionOnFrame, Matcher.positions[i].heightOnFrame, [])))
                    continue
                else:
                    results.append((frame, -1))
                    continue

            area = max(map(lambda a: Util.getArea(a), bounds))
            filter(lambda a: Util.getArea(a) == area, bounds)

            personPos = bounds[0]

            center, personHeight = Util.getCenterAndHumanPin(personPos, Matcher.height)
            Matcher.positions[i].heightOnFrame = personHeight

            Matcher.positions[i].push(center)

            centerAvg = Util.avgPos(Matcher.positions[i].stack)

            calcPos = []

            for pos in range(len(Matcher.positions[i].stack)):
                x1 = Matcher.positions[i].stack[pos]
                x2 = Matcher.positions[i].stack[pos - 1]
                if(Util.calcDistance(x1, x2) <= 20 and 2.5 < Util.getAspectRatio(personPos) <= 3.5):
                    calcPos.append(Matcher.positions[i].stack[pos])

            if(len(calcPos) == 0):
                calcPos = Matcher.positions[i].stack

            calcAvg = Util.avgPos(calcPos)

            vector = Util.vectorHeading(calcPos[0], calcPos[-1])
            Matcher.positions[i].vector = vector

            newPos = Util.addVectorToPoint(vector, calcAvg)
            Matcher.positions[i].positionOnFrame = newPos

            recs = (newPos, personHeight, personPos)

            results.append((frame, recs))

        return results[:len(Matcher.cameras)]

    @staticmethod
    def matchPositions():
        for i in range(len(Matcher.cameras)):
            #print(Matcher.cameras[i].heading)
            pass

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
