import cv2
import imutils
import numpy as np
import handleDatabase
from utility import util
from camera import Camera
from humanDetector import Detector

height = 190
moveTreshold = 10

def main():
    c = Camera("video", "video.mp4")

    print(handleDatabase.connect())

    detectionStack = []

    while True:
        frame = c.getFrame()
        #frame = imutils.resize(frame, width=500)
        blank = np.zeros((300, 300), np.uint8)

        global H, W
        (H, W) = frame.shape[:2]

        recs = Detector.detectWithDNN(frame)

        for (center, pin, bounds) in recs:
            cv2.circle(frame, center, 5, (0, 255, 0), 2)

            util.push(center)

            (x1, y1, x2, y2) = bounds
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0))

            x = util.mapVals(util.avgHeading()[0], 0, W, 0, 300)
            y = util.mapVals(pin, 60, 200, 300, 0)

            for pos in range(len(util.stack)):
                if(util.calcDistance(util.stack[pos], util.stack[pos - 1]) < moveTreshold):
                     cv2.circle(frame, util.stack[pos], 3, (0, 255, 0), -1)
                else:
                     cv2.circle(frame, util.stack[pos], 3, (0, 0, 255), -1)
               
            cv2.circle(frame, util.avgHeading(), 3, (255, 255, 255), -1)
            cv2.circle(blank, (x, y), 5, (255, 0, 0), -1)

        cv2.imshow("Feed", frame)
        cv2.imshow("Top-Down", blank)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()