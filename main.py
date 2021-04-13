import cv2
import imutils
import numpy as np
from handleDatabase import Database
from camera import Camera
from cameraMatcher import Matcher

def main():

    cameras = []

    #c1 = Camera("video", "left", "blaze", "vids/sess2/right.mp4", True)
    c2 = Camera("video", "left", "dnn", "vids/sess2/left.mp4")
    c3 = Camera("video", "right", "dnn", "vids/sess2/right.mp4")
    #cameras.append(c1)
    cameras.append(c2)
    cameras.append(c3)

    m = Matcher(190, cameras)
    
    #print(Database.connect())

    while True:
        blank = np.zeros((300, 300), np.uint8)
        c = 0
        h = m.calcPosition()
        p = m.matchPositions()

        cv2.circle(blank, (p[0] * 3, p[1] * 3), 5, (255, 255, 255), cv2.FILLED)
        cv2.imshow("Calc", blank)

        for (frame, recs) in h:
            c += 1

            if(recs != -1):
                (center, personHeight, personPosBox) = recs
                if(len(personPosBox) != 0):
                    (x1, y1, x2, y2) = personPosBox
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0))

                cv2.circle(frame, center, 5, (0, 255, 0), 2)

                cv2.imshow("Feed" + str(c), frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()