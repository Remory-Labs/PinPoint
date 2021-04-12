import cv2, pickle, struct, socket, imutils

class Camera:
    camType = None
    heading = None
    detectionMethod = None
    cam = cv2.VideoCapture()

    clientSocket = None
    data = b""
    payloadSize = None

    def getFrame(self, size=500):
        if(self.camType == "video" or self.camType == "webcam"):
            ret, frame = self.cam.read()
            frame = imutils.resize(frame, width=size)
            return frame

        elif(self.camType == "ip"):
            while len(self.data) < self.payloadSize:
                packet = self.clientSocket.recv(4*1024)
                if not packet: 
                    break

                self.data += packet
            packedSize = self.data[:self.payloadSize]
            self.data = self.data[self.payloadSize:]
            msgSize = struct.unpack("Q", packedSize)[0]
            
            while len(self.data) < msgSize:
                self.data += self.clientSocket.recv(4*1024)
            frameData = self.data[:msgSize]
            self.data = self.data[msgSize:]
            frame = pickle.loads(frameData)
            frame = imutils.resize(frame, width=size)
            return frame

        else:
            raise Exception("Video stream ended for an Unknown reason.")

    def __init__(self, camType="video", heading="front", method="dnn", args="0"):
        self.camType = camType.lower()
        self.heading = heading.lower()
        self.detectionMethod = method.lower()

        if(self.camType == "video"):
            if not type(args) is str:
                raise TypeError("Video type needs correct path to file. Expected: string")
            self.cam = cv2.VideoCapture(args)

        elif(self.camType == "webcam"):
            if not type(args) is int:
                raise TypeError("Webcam type needs a camera index. Expected: int")
            self.cam = cv2.VideoCapture(args)

        elif(self.camType == "ip"):
            if not type(args) is str:
                raise TypeError("IP type needs a correct IP address. Expected: string")
            self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.clientSocket.connect((args, 2077))
           
            self.payloadSize = struct.calcsize("Q")

        else:
            raise Exception("Camera type is not supported, they are the following: Video, Webcam, IP")