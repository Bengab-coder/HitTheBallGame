import random
import time

import cvzone
from cvzone import HandTrackingModule
import cv2 as cv
import numpy as np
import random

WIDTH = 720
HEIGHT = 480

camera = cv.VideoCapture(0)
camera.set(3, WIDTH)  # width
camera.set(4, HEIGHT)  # height
handTracker = HandTrackingModule.HandDetector(maxHands=1, minTrackCon=0.8, detectionCon=0.8)

distance = 0
distancePercent = 0
cx, cy = random.randint(100, 500), random.randint(100, 350)
colorOutlineCircle = (255, 0, 255)
score = 0
currentTime = 0

startTime = time.time()
playTime = 30
started = True

while True:
    print("[OPENCV]:Getting Image Frame..")
    _, frame = camera.read()
    frame = cv.flip(frame, 1)

    if started:
        currentTime = int(abs(time.time() - startTime))
        remainingTime = int(np.interp(currentTime, (0, playTime), (playTime, 0)))
        result = handTracker.findHands(frame, flipType=False, draw=False)

        if remainingTime > 0:
            if result:
                lmList = result[0]['lmList']
                bbox = result[0]['bbox']

                cvzone.cornerRect(frame, bbox)

                x1, y1, w, h = bbox
                x2, y2 = x1 + w, y1 + h

                firstPoint = lmList[2]
                secondPoint = lmList[17]

                cvzone.putTextRect(frame, 'p1', firstPoint, scale=1)
                cvzone.putTextRect(frame, 'p2', secondPoint, scale=1)

                distance, info = handTracker.findDistance(firstPoint, secondPoint)
                distancePercent = np.interp(distance, (80, 200), (0, 100))
                barIndicatorY = int(np.interp(distancePercent, (0, 100), (317, 80)))

                if distancePercent <= 30:
                    barIndicatorColor = (0, 0, 255)
                elif 0 < distancePercent < 100:
                    barIndicatorColor = (255, 0, 255)
                else:
                    barIndicatorColor = (0, 255, 0)

                cvzone.putTextRect(frame, f"{int(distancePercent)}%", (x1 + 10, y1 - 20), colorR=(0, 255, 0), scale=2)
                cv.rectangle(frame, (575, 430), (630, 80), barIndicatorColor, thickness=2)
                cv.rectangle(frame, (575, 430), (630, barIndicatorY), barIndicatorColor, thickness=-1)

                if distancePercent >= 30:
                    cv.circle(frame, (600, 455), 20, (0, 255, 0), thickness=-1)
                    if x1 < cx < x2 and y1 < cy < y2:
                        cx, cy = random.randint(100, 500), random.randint(100, 350)
                        colorOutlineCircle = (0, 255, 0)
                        score += 1
                    else:
                        colorOutlineCircle = (255, 0, 255)
                else:
                    cv.circle(frame, (600, 455), 20, (0, 0, 255), thickness=-1)

            # score board
            cvzone.putTextRect(frame, f"Score:{score}", (450, 50), scale=2)

            # Time board
            cvzone.putTextRect(frame, f"Time:{str(remainingTime).zfill(2)}", (20, 50), scale=2)

            cv.putText(frame, 'Press d to quit.', (180, 470), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=3,
                       color=(255, 255, 0))

            cv.circle(frame, (cx, cy), 10, thickness=-1, color=(255, 255, 0))
            cv.circle(frame, (cx, cy), 15, thickness=2, color=(255, 255, 255))
            cv.circle(frame, (cx, cy), 20, thickness=3, color=colorOutlineCircle)

        else:
            cvzone.putTextRect(frame, 'Game Over', (210, HEIGHT // 2))
            cv.putText(frame, 'Press r to restart !', (180, 300), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1,
                       thickness=3, color=(255, 255, 0))
            cv.putText(frame, 'Press d to quit.', (180, 350), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, thickness=3,
                       color=(255, 255, 0))

    cv.imshow("Hit the Ball Game", frame)
    key = cv.waitKey(1)

    if key & 0xff == ord('d'):
        break

    elif key == ord('r'):
        score = 0
        currentTime = 0
        startTime = time.time()

camera.release()
cv.destroyAllWindows()
