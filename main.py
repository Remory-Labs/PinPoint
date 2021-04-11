import cv2
import imutils
import numpy as np
import handleDatabase
from utility import Util
from camera import Camera
from cameraMatcher import Matcher

def main():
    #c = Camera("video", "video.mp4")
    cameras = []
    c = Camera("video", "vids/sess2/left.mp4")
    c2 = Camera("video", "vids/sess2/right.mp4")
    #cameras.append(c)
    cameras.append(c2)

    m = Matcher(190, cameras)
    #c = Camera("video", "vids/sess2/right.mp4")
    #c = Camera("video", "https://192.168.0.102:8080/video")
    
    print(handleDatabase.connect())

    detectionStack = []

    while True:
        blank = np.zeros((300, 300), np.uint8)
        c = 0
        h = m.match()
        for (frame, recs) in h:
            c += 1

            try:
                (center, personHeight, bounds) = recs
                cv2.circle(frame, center, 5, (0, 255, 0), 2)

                (x1, y1, x2, y2) = bounds
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0))

    #           x = util.mapVals(util.avgHeading()[0], 0, W, 0, 300)
    #           y = util.mapVals(pin, 60, 200, 300, 0)
    #           for pos in range(len(util.stack)):
    #               if(util.calcDistance(util.stack[pos], util.stack[pos - 1]) < moveTreshold):
    #                    cv2.circle(frame, util.stack[pos], 3, (0, 255, 0), -1)
    #               else:
    #                    cv2.circle(frame, util.stack[pos], 3, (0, 0, 255), -1)
    #              
    #           cv2.circle(frame, util.avgHeading(), 3, (255, 255, 255), -1)
    #           cv2.circle(blank, (x, y), 5, (255, 0, 0), -1)
            except:
                pass
            cv2.imshow("Feed" + str(c), frame)
            

      
        #cv2.imshow("Top-Down", blank)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()