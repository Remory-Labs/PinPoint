import cv2
import imutils
import numpy as np
import handleDatabase
from utility import Util
from camera import Camera
from cameraMatcher import Matcher

#from humanDetector import Detector

def main():

    cameras = []

    c1 = Camera("video", "front", "dnn", "vids/sess2/front.mp4")
    c2 = Camera("video", "right", "blaze", "vids/sess2/right.mp4")
    cameras.append(c1)
    cameras.append(c2)

    m = Matcher(190, cameras)
    
    print(handleDatabase.connect())

    while True:
        blank = np.zeros((300, 300), np.uint8)
        c = 0
        h = m.calcPosition()
        m.matchPositions()

        #for i in range(len(cameras)):
            #frame = cameras[i].getFrame(1000)
            #person = Detector.detectWithDNN(frame)
            #center, personHeight = Util.getCenterAndHumanPin(person[0], Matcher.height)
            #recs = (center, personHeight, person)
            #h = [(frame, recs)]

        for (frame, recs) in h:
            c += 1

            if(recs != -1):
                (center, personHeight, personPosBox) = recs
                if(len(personPosBox) != 0):
                    (x1, y1, x2, y2) = personPosBox
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0))

            cv2.circle(frame, center, 5, (0, 255, 0), 2)

            #x = util.mapVals(util.avgHeading()[0], 0, W, 0, 300)
            #y = util.mapVals(pin, 60, 200, 300, 0)
            cv2.imshow("Feed" + str(c), frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()