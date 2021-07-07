import re
from numpy import empty
from numpy.core.fromnumeric import size
from camera import Camera
from humanDetector import Detector
from utility import Util

class Matcher:
    height = None
    cameras = []
    single = True

    def __init__(self, height, cameras, single=True):
        Matcher.height = height
        Matcher.cameras = cameras
        Matcher.single = single

    @staticmethod
    def calcPosition(cameraIndex=-1):
        results = []
        if(cameraIndex != -1):
            results.append(Matcher.atFrameCalc(cameraIndex))
        else:
            for i in range(len(Matcher.cameras)): #Finds, and calculates Human body position for every camera.
                results.append(Matcher.atFrameCalc(i))
        return results

    @staticmethod
    def atFrameCalc(camId):
        frame = Matcher.cameras[camId].getFrame()
        idx = Matcher.cameras[camId].index = camId
        bounds = Matcher.getRecs(frame, Matcher.cameras[camId].detectionMethod)

        if(len(bounds) == 0): #If no body is found, return -1
            return ((frame, -1))

        if(1 < len(bounds) and Matcher.single is True):
            maxArea = max(map(lambda area: Util.getArea(area), bounds))  #Find the biggest area of detections
            filter(lambda area: Util.getArea(area) == maxArea, bounds) #For filtering out smaller, accidental detections
            poses = [bounds[0]]
        else:
            poses = bounds

        camHeights = []
        camCenters = []
        camHeadings = []

        for person in poses:
            center, personHeight = Util.getCenterAndHumanPin(person, Matcher.height)
            camCenters.append(center)
            camHeights.append(personHeight)
            camHeadings.append(Matcher.cameras[camId].heading)

        recs = (camCenters, camHeights, camHeadings, poses, idx)          

        return((frame, recs))

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
            return(abs(100 - x), y)

        elif(side == "left"):
            return(y, x)
        
        elif(side == "back"):
            return(x, abs(100 - y))

        else:
            return(y, x)

    @staticmethod
    def skinify(results):
        skiny = []
        if(results == 0):
            return -1
        for x in results:
            skiny.append(x[1])
        return skiny

    LOW = 0
    HIGH = 100
    @staticmethod
    def matchIt(results):
        local = []

        try:
            for data in Matcher.skinify(results):
                position, height, heading, poses, idx = data

                if(Matcher.LOW == 0):
                    Matcher.LOW = height[0] / 2
                    Matcher.HIGH = height[0] * 2

                #print(Matcher.LOW, Matcher.HIGH)

                x = Util.mapVals(position[0][0], 0, Camera.WIDTH, 0, 100)
                y = Util.mapVals(height[0], Matcher.LOW, Matcher.HIGH, 0, 100)

                a, b = Matcher.computeForCamera(heading[0], (x, y))    

                local.append([(a, b), heading[0]])

            if(len(local) == 1):
                return(local[0][0][0] * 3, local[0][0][1] * 3)

            elif(len(local) == 2):
                sides = [s[1] for s in local]

                front = sides.count("front")
                left = sides.count("left")
                back = sides.count("back")
                right = sides.count("right")

                x, y = 0, 0

                if((front == 1 or back == 1)):
                    a = local[0] #Height [0] xPos [1]
                    b = local[1]

                    if(front + back == 1):
                        #Front xor back is in

                        if(a[1] == "left" or a[1] == "right"): #A camera is side camera
                            x = b[0][0]
                            y = a[0][1]
                        else:
                            x = a[0][0]
                            y = b[0][1]

                        return (x * 3, y * 3)
                    else:
                        if(a[1] == "front"):
                            return(a[0][0] * 3, a[0][1] * 3)
                        else:
                            print(3)
                            return(b[0][1] * 3, b[0][0] * 3)

                else:
                    if(left + right == 1):
                        #Left or Right is in
                        1 + 1
                    else:
                        #Left and Right cams are set
                        1 + 1

                    
            else:
                pass
        except:
            return(-1, -1)


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
