import random

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands=2)

timer = 0
stateResult = False
startGame= False
scores = [0, 0] #[AI, Player]


while True:
    imgBG = cv2.imread("Resources/bg.png")
    #imgBG = cv2.resize(imgBG, (0, 0), None,0.25,0.18 )

    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[: ,80:480]

    # Hand detection

    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG,str(int(timer)),(605,435),cv2.FONT_HERSHEY_PLAIN, 6, (255,255,255), 4)

        if timer>3:
            stateResult = True
            timer=0

            if hands:
                playerMove = None
                for hand in hands:
                    lmList = hand["lmList"]
                    wrist_x = lmList[0][0]

                    if wrist_x < img.shape[1] // 2:  # If the wrist is to the left of the center of the frame, it's the left hand
                        hand_label = "Right"
                        #hand = hands[0]
                        fingers = detector.fingersUp(hand)
                        print("Right" + str(fingers))
                    else:
                        hand_label = "Left"
                        #hand = hands[0]
                        fingers = detector.fingersUp(hand)
                        print("Left" + str(fingers))

                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    randomNumber = random.randint(1,3)

                    imgAI = cv2.imread(f'Resources/{randomNumber}.png',cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG,imgAI, (149, 310))

                    #player wins

                    if (playerMove == 1 and randomNumber == 3) or (playerMove == 2 and randomNumber == 1) or (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # AI wins

                    if (playerMove == 3 and randomNumber == 1) or (playerMove == 1 and randomNumber == 2) or (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1





    imgBG[234:654, 795:1195] = imgScaled
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG,imgAI, (149, 310))


    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)


    #cv2.imshow("Image",imgScaled)
    cv2.imshow("bg", imgBG)
    key=cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False