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

        for i in range(len(Matcher.cameras)): #Finds, and calculates Human body position for every camera.
            frame = Matcher.cameras[i].getFrame(1280)
            bounds = Matcher.getRecs(frame, Matcher.cameras[i].detectionMethod)

            if(len(bounds) == 0): #If no body is found, try to return last position, otherwise -1
                if(Matcher.positions[i].vector != None):
                    results.append((frame, (Matcher.positions[i].positionOnFrame, Matcher.positions[i].heightOnFrame, [])))
                    continue
                else:
                    results.append((frame, -1))
                    continue

            if(1 < len(bounds)):
                maxArea = max(map(lambda area: Util.getArea(area), bounds))  #Find the biggest area of detections
                filter(lambda area: Util.getArea(area) == maxArea, bounds) #For filtering out smaller, accidental detections

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

            recs = (center, personHeight, personPos) #TODO Currently person avg center calculation is bypassed completely. Cause: centerAvg calculation is leaking

            results.append((frame, recs))

        return results[:len(Matcher.cameras)]

    @staticmethod
    def matchPositions():
        results = []

        for i in range(len(Matcher.cameras)): #Calculate Human position for every camera
            pos = Matcher.positions[i].positionOnFrame
            height = Matcher.positions[i].heightOnFrame
            side = Matcher.cameras[i].heading

            x = Util.mapVals(pos[0], 0, Matcher.cameras[i].w, 0, 100)
            y = Util.mapVals(height, 60, 200, 0, 100)

            results.append((side, (x, y)))

        if(len(results) == 1):
            side, (x, y) = results[0]

            return Matcher.computeForCamera(side, (x, y))

        else:
            sides = [s[0] for s in results]
            positions = [pos[1] for pos in results]

            front = sides.count("front")
            left = sides.count("left")
            back = sides.count("back")
            right = sides.count("right")

            if(len(results) == 2):
                array = []
                xS = 0
                yS = 0
                for side, pos in zip(sides, positions):
                    (x, y) = Matcher.computeForCamera(side, pos)
                    if(side == "left" or "right"):
                        xS = x
                    if(side == "back" or "front"):
                        xY = x

                return (xS, xY)

    @staticmethod
    def computeForCamera(side, pos):
        (x, y) = pos

        if(side == "front"):
            return(x, abs(100 - y))

        elif(side == "left"):
            return(y, x)
        
        elif(side == "back"):
            return(x, y)

        else:
            return(abs(100 - y), abs(100 - x))


    @staticmethod
    def getRecs(frame, method):

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
