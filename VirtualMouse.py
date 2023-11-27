import cv2
import numpy as np
import Handtrack as htm
import time
import autopy

wCam, hCam = 640, 480
frameR = 100
smoothening = 7

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands = 1)
wScr, hScr = autopy.screen.size()

while True:
    # find hand landmark
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    #get the tip  of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #print(x1, y1, x2, y2)

    #cek fingers up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), 
                          (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        #index fingers moving mode
        if fingers[1] == 1 and fingers[2] == 0 :
            #convert coordinate
            x = np.interp(x1, (frameR, wCam - frameR), (0,wScr))
            y = np.interp(y1, (frameR, hCam - frameR), (0,hScr))

            #smoothen values
            clocX = plocX + (x - plocX) / smoothening
            clocY = plocY + (y - plocY) / smoothening
            #move mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        #find distance between fingers and clicking mouse
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 25:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 
                           15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

             #Find distance between fingers 
            length, img, lineInfo = detector.findDistance(8, 4, img)
            #Click right mouse if distance short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 
                           15, (0,255,0), cv2.FILLED)
                autopy.mouse.click(button=autopy.mouse.Button.RIGHT)
    #frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    #display
    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit the program
        break

cap.release()
cv2.destroyAllWindows()