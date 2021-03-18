import numpy as np

stack = []

def calcDistance(p1, p2):
    (p1x, p1y) = p1
    (p2x, p2y) = p2
    x = np.power((p2x - p1x), 2) + np.power((p2y - p1y), 2)
    return np.sqrt(x)

def mapVals(x, xMin, xMax, yMin, yMax):
    return int((x - xMin) * (yMax - yMin) / (xMax - xMin) + yMin)

def push(position):
    global stack
    if(5 < len(stack)):
        stack.pop(0)
    
    stack.append(position)

def avgHeading():
    global stack
    xS = [x[0] for x in stack]
    yS = [y[1] for y in stack]
    return (int(sum(xS) / len(stack)), int(sum(yS) / len(stack)))