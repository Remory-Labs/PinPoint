import cv2, pickle, struct, socket, imutils

class Camera:
    camType = None
    heading = None
    detectionMethod = None
    flipped = False
    cam = cv2.VideoCapture()
    index = 0

    WIDTH = 720

    h = None
    w = None

    def getFrame(self, size=WIDTH):
        frame = None
        
        if(self.camType == "video" or self.camType == "webcam"):
            ret, frame = self.cam.read()
            frame = imutils.resize(frame, width=size)

        elif(self.camType == "ip"):
            frame = ""
            try:
                frame = self.cam.grab()[1]
            except:
                frame = self.cam.read()[1]
            frame = imutils.resize(frame, width=size)

        else:
            raise Exception("Video stream ended for an Unknown reason.")

        if(self.flipped):
            frame = cv2.flip(frame, 1)

        return frame
        
    def replay(self):
        self.cam.set(cv2.CAP_PROP_POS_FRAMES, 1)
        
    def __init__(self, camType="video", heading="front", method="dnn", args="0", flipped=False, index=0, width=720):
        self.camType = camType.lower()
        self.heading = heading.lower()
        self.detectionMethod = method.lower()
        self.flipped = flipped
        self.index = index

        if(self.camType == "video"):
            if not type(args) is str:
                raise TypeError("Video type needs correct path to file. Expected: string")
            self.cam = cv2.VideoCapture(args)

        elif(self.camType == "webcam"):
            try:
                index = int(args)
                self.cam = cv2.VideoCapture(index)
            except ValueError:
                raise TypeError("Webcam type needs a camera index. Expected: int")

        elif(self.camType == "ip"):
            if not type(args) is str:
                raise TypeError("IP type needs a correct IP address. Expected: string")
            self.cam = cv2.VideoCapture(args)

        else:
            raise Exception("Camera type is not supported, they are the following: Video, Webcam, IP")
       
        try:
            self.h, self.w = self.getFrame(Camera.WIDTH).shape[:2]
        except:
            raise Exception("Can't read from camera, perhaps it's not configured correctly.")