import numpy as np

class Util:

    @staticmethod
    def calcDistance(p1, p2):
        (p1x, p1y) = p1
        (p2x, p2y) = p2
        x = np.power((p2x - p1x), 2) + np.power((p2y - p1y), 2)
        return np.sqrt(x)

    @staticmethod
    def mapVals(x, xMin, xMax, yMin, yMax):
        return int((x - xMin) * (yMax - yMin) / (xMax - xMin) + yMin)

    @staticmethod
    def getCenterAndHumanPin(bound, height):
        if(bound is None):
            return (0, 0), 0
        (startX, startY, endX, endY) = bound
        center = (int(startX + ((endX - startX) / 2)), (int(endY - ((endY - startY) / 2))))
        pin = round(height / (endY - startY) * 100, 2)
        return center, pin

    @staticmethod
    def getAspectRatio(bound):
        h, w = Util.getHW(bound)
        return h / w

    @staticmethod
    def getArea(bound):
        h, w = Util.getHW(bound)
        return h * w

    @staticmethod
    def getHW(bound):
        (startX, startY, endX, endY) = bound
        w = Util.calcDistance((startX, startY), (endX, startY))
        h = Util.calcDistance((startX, startY), (startX, endY))
        return h, w

    @staticmethod
    def vectorHeading(p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        x = int((x2 - x1) / 2)
        y = int((y2 - y1) / 2)
        return (x, y)

    @staticmethod
    def addVectorToPoint(vector, point):
        return tuple(map(lambda a, b: a + b, vector, point))

    @staticmethod
    def avgPos(array):
        xS = [x[0] for x in array]
        yS = [y[1] for y in array]
        return (int(sum(xS) / len(array)), int(sum(yS) / len(array)))