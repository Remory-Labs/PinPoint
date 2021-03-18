import cv2
import imutils
import numpy as np

protopath = "MobileNetSSD_deploy.prototxt"
modelpath = "MobileNetSSD_deploy.caffemodel"

net = cv2.dnn.readNetFromCaffe(protopath, modelpath)

def main():
    feed = cv2.VideoCapture('vids/sess2/right.mp4')
    feed = cv2.VideoCapture('video.mp4')

    while True:
        ret, frame = feed.read()
        frame = imutils.resize(frame, width=500)
        blank = np.zeros((300, 300), np.uint8)

        (H, W) = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

        net.setInput(blob)
        found = net.forward()

        for i in range(found.shape[2]):

            confidence = found[0, 0, i, 2]
            if 0.2 < confidence:
                idx = int(found[0, 0, i, 1])

                if idx != 15:
                    continue

                (startX, startY, endX, endY) = (found[0, 0, i, 3:7] * np.array([W, H, W, H])).astype("int")

                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(frame, str(endY - startY), (endX, endY), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 0)

                pin = round(190 / (endY - startY) * 100, 2)

                cv2.putText(frame, str(pin), (endX, int(endY - ((endY - startY) / 2))), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 0)

                center = (int(startX + ((endX - startX) / 2)), (int(endY - ((endY - startY) / 2))))
                cv2.circle(frame, center, 5, (0, 255, 0), 2)


                x = mapVals(center[0], 0, W, 0, 300)
                y = mapVals(pin, 60, 200, 300, 0)

                cv2.circle(blank, (x, y), 5, (255, 0, 0), -1)

        cv2.imshow("Feed", frame)
        cv2.imshow("Top-Down", blank)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

def mapVals(x, xMin, xMax, yMin, yMax):
    return int((x - xMin) * (yMax - yMin) / (xMax - xMin) + yMin)

main()