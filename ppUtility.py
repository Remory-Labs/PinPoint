import numpy as np

def calcDistance(p1, p2):
    (p1x, p1y) = p1
    (p2x, p2y) = p2
    x = np.power((p2x - p1x), 2) + np.power((p2y - p1y), 2)
    return np.sqrt(x)

def mapVals(x, xMin, xMax, yMin, yMax):
    return int((x - xMin) * (yMax - yMin) / (xMax - xMin) + yMin)

def __init__(self):
    return "Succesfully created PinPoint Utility"