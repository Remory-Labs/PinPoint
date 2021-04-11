import numpy as np
from utility import Util

class Positon:
    stack = []
    precision = None

    positionOnFrame = None

    def push(self, position):
        if(self.precision < len(self.stack)):
            self.stack.pop(0)
        
        self.stack.append(position)

    def avgPos(self):
        xS = [x[0] for x in self.stack]
        yS = [y[1] for y in self.stack]
        return (int(sum(xS) / len(self.stack)), int(sum(yS) / len(self.stack)))

    def __init__(self, precision=5):
        self.precision = precision