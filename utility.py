import numpy as np

class util:
    stack = []

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
    def push(position):
        #global stack
        if(5 < len(util.stack)):
            util.stack.pop(0)
        
        util.stack.append(position)

    @staticmethod
    def avgHeading():
        #global stack
        xS = [x[0] for x in util.stack]
        yS = [y[1] for y in util.stack]
        return (int(sum(xS) / len(util.stack)), int(sum(yS) / len(util.stack)))

    @staticmethod
    def getCenterAndPin(bound):
        (startX, startY, endX, endY) = bound
        center = (int(startX + ((endX - startX) / 2)), (int(endY - ((endY - startY) / 2))))
        pin = round(190 / (endY - startY) * 100, 2) #TODO Change static height, now 190, should be multiplication later
        return center, pin