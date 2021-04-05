import cv2, pickle, struct, socket

class Camera:
    camType = "" # video, webcam, ip
    cam = cv2.VideoCapture()

    clientSocket = ""
    data = b""
    payloadSize = 0

    def getFrame(self):
        if(self.camType == "video" or self.camType == "webcam"):
            ret, frame = Camera.cam.read()
            return frame

        elif(self.camType == "ip"):
            while len(Camera.data) < Camera.payloadSize:
                packet = Camera.clientSocket.recv(4*1024)
                if not packet: 
                    break

                Camera.data += packet
            packedSize = Camera.data[:Camera.payloadSize]
            Camera.data = Camera.data[Camera.payloadSize:]
            msgSize = struct.unpack("Q", packedSize)[0]
            
            while len(Camera.data) < msgSize:
                Camera.data += Camera.clientSocket.recv(4*1024)
            frameData = Camera.data[:msgSize]
            Camera.data = Camera.data[msgSize:]
            frame = pickle.loads(frameData)
            return frame

        else:
            raise Exception("Video stream ended for an Unknown reason.")

    def __init__(self, camType, args):
        self.camType = camType.lower()

        if(self.camType == "video"):
            if not type(args) is str:
                raise TypeError("Video type needs correct path to file. Expected: string")
            Camera.cam = cv2.VideoCapture(args)

        elif(self.camType == "webcam"):
            if not type(args) is int:
                raise TypeError("Webcam type needs a camera index. Expected: int")
            Camera.cam = cv2.VideoCapture(args)

        elif(self.camType == "ip"):
            if not type(args) is str:
                raise TypeError("IP type needs a correct IP address. Expected: string")
            Camera.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            Camera.clientSocket.connect((args, 2077))
            Camera.payloadSize = struct.calcsize("Q")

        else:
            raise Exception("Camera type is not supported, they are the following: Video, Webcam, IP")