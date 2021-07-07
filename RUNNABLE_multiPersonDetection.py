from numpy.core.fromnumeric import shape, size
from camera import Camera
from cameraMatcher import Matcher
import cv2
import numpy as np

def main():
    c1 = Camera("video", "back", "dnn", "videopath.mp4")


    Camera.WIDTH = 720

    m = Matcher(180, [c1])

    while True:
        blank = np.zeros((300, 300), np.uint8)
        p = m.calcPosition()
       
        try:
            i = 0
            pos = m.matchIt(p)
            for cam in p:
                for detection in range(0, len(cam[1][0])):
                    g = cam[1]
                    center = g[0][detection]
                    height = g[1][detection]
                    #sides = g[2][detection]
                    rec = g[3][detection]
                    #idx = g[4]

                    cv2.rectangle(cam[0], (rec[0], rec[1]), (rec[2], rec[3]), (255, 0, 0), 2)
                    cv2.circle(cam[0], center, 10, (255, 0, 255), -1)
                    cv2.putText(cam[0], str(height), (center[0] + 60, center[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)

                cv2.rectangle(blank, (10, 10), (290, 20), (255, 255, 255), 2)
                cv2.circle(blank, pos, 10, (255, 255, 255), -1)
                cv2.imshow("feed" + str(i), cam[0])
                i += 1
        except:
            continue

        cv2.imshow("top-down", blank)
        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()

if __name__ == '__main__':
    main()