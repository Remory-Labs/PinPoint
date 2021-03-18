import cv2
import imutils
import numpy as np
import handleDatabase
import ppUtility as util

protopath = "MobileNetSSD_deploy.prototxt"
modelpath = "MobileNetSSD_deploy.caffemodel"

net = cv2.dnn.readNetFromCaffe(protopath, modelpath)

height = 190
moveTreshold = 10

def main():
    feed = cv2.VideoCapture('vids/sess2/right.mp4')
    #feed = cv2.VideoCapture('video.mp4')

    print(handleDatabase.connect())

    detectionStack = []

    while True:
        ret, frame = feed.read()
        frame = imutils.resize(frame, width=500)
        blank = np.zeros((300, 300), np.uint8)

        global H, W
        (H, W) = frame.shape[:2]

        recs = detectHumanPosition(frame)

        for (center, pin) in recs:
            cv2.circle(frame, center, 5, (0, 255, 0), 2)

            util.push(center)

            x = util.mapVals(util.avgHeading()[0], 0, W, 0, 300)
            y = util.mapVals(pin, 60, 200, 300, 0)

            #for pos in range(len(util.stack)):
                #if(util.calcDistance(util.stack[pos], util.stack[pos - 1]) < moveTreshold):
                     #cv2.circle(frame, util.stack[pos ], 3, (0, 255, 0), -1)
                #else:
                     #cv2.circle(frame, util.stack[pos], 3, (0, 0, 255), -1)
               
            cv2.circle(frame, util.avgHeading(), 3, (255, 255, 255), -1)
            cv2.circle(blank, (x, y), 5, (255, 0, 0), -1)

        cv2.imshow("Feed", frame)
        cv2.imshow("Top-Down", blank)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

def detectHumanPosition(frame):
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    found = net.forward()

    recogs = []

    for i in range(found.shape[2]):

        confidence = found[0, 0, i, 2]
        if 0.2 < confidence:
            idx = int(found[0, 0, i, 1])

            if idx != 15:
                continue

            (startX, startY, endX, endY) = (found[0, 0, i, 3:7] * np.array([W, H, W, H])).astype("int")

            center = (int(startX + ((endX - startX) / 2)), (int(endY - ((endY - startY) / 2))))
            pin = round(height / (endY - startY) * 100, 2)

            recogs.append((center, pin))

    return recogs

if __name__ == '__main__':
    main()