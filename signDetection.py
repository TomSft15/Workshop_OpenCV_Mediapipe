import cv2
import mediapipe as mp
import os

def nbFingerUp(hand_position):
    tipIds = [4, 8, 12, 16, 20]
    finger = []
    if (hand_position[tipIds[0]][1] > hand_position[tipIds[0] - 1][1]):
            finger.append(1)
    else:
        finger.append(0)
    for id in range(1, 5):
        if (hand_position[tipIds[id]][2] < hand_position[tipIds[id] - 2][2]):
            finger.append(1)
        else:
            finger.append(0)
    nbFinger = finger.count(1)
    return finger

def getfiles(path):
    myList = os.listdir(path)
    for i in range(len(myList)):
        myList[i] = path + myList[i]
    return myList

def handleSign(tabFingers, hand_position, image):
    if (tabFingers.count(1) == 5):
        cv2.putText(image, "HELLO",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    elif (tabFingers[2] == 1 and tabFingers[1] == 0 and
        tabFingers[3] == 0 and tabFingers[4] == 0):
        cv2.putText(image, "FUCK YOU",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    elif (tabFingers[1] == 1 and tabFingers[4] == 1):
        if ((hand_position[8][2] < hand_position[12][2] and hand_position[20][2] < hand_position[12][2])
            and (hand_position[8][2] < hand_position[16][2] and hand_position[20][2] < hand_position[16][2])):
            cv2.putText(image, "LOVE",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    elif (tabFingers.count(0) == 5):
        cv2.putText(image, "WAKANDA",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        for i in range(len(hand_position)):
            if (hand_position[4][2] > hand_position[i][2]):
                cv2.putText(image, "BAD",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif (hand_position[4][2] < hand_position[i][2]):
                cv2.putText(image, "GOOD",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def main():
    hand_position = []
    overlayList = []
    nbFinger = 0
    pathDirectory = "assets/"
    myList = getfiles(pathDirectory)
    for i in myList:
        img_finger = cv2.imread(f'{i}')
        overlayList.append(img_finger)
    # Declaring Hand model
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    #drawing mediapipe solutions
    mpDraw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    with mpHands.Hands(model_complexity=0,
        min_detection_confidence=0.5, 
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mpDraw.draw_landmarks(image, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
                    # get the landmark position on the screen
                    h, w, _ = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if (id == 8 or id == 5):
                        cv2.circle(image, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                    hand_position.append([id, cx, cy])
                    if (len(hand_position) == 21):
                        tabFinger = nbFingerUp(hand_position)
                        handleSign(tabFinger, hand_position, image)
                        hand_position = []
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == ord("q"):
                break
    cap.release()

if __name__ == '__main__':
    main()
