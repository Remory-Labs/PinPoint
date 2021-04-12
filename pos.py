class Positon:
    stack = []
    precision = None

    positionOnFrame = None
    heightOnFrame = None
    vector = None

    def push(self, position):
        if(self.precision < len(self.stack)):
            self.stack.pop(0)
        
        self.stack.append(position)

    def __init__(self, precision=5):
        self.precision = precision