import cv2
import mediapipe as mp
import os

def displayFinger(image, nbFinger, overlayList):
    if (nbFinger > 0):
        if (nbFinger == 1):
            overlayList[3] = cv2.resize(overlayList[3], (200, 200))
            x, y, _ = overlayList[3].shape
            image[0:x, 0:y] = overlayList[3]
        if (nbFinger == 2):
            overlayList[4] = cv2.resize(overlayList[4], (200, 200))
            x, y, _ = overlayList[4].shape
            image[0:x, 0:y] = overlayList[4]
        if (nbFinger == 3):
            overlayList[2] = cv2.resize(overlayList[2], (200, 200))
            x, y, _ = overlayList[2].shape
            image[0:x, 0:y] = overlayList[2]
        if (nbFinger == 4):
            overlayList[0] = cv2.resize(overlayList[0], (200, 200))
            x, y, _ = overlayList[0].shape
            image[0:x, 0:y] = overlayList[0]
        if (nbFinger == 5):
            overlayList[1] = cv2.resize(overlayList[1], (200, 200))
            x, y, _ = overlayList[1].shape
            image[0:x, 0:y] = overlayList[1]

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
    return nbFinger

def getfiles(path):
    myList = os.listdir(path)
    for i in range(len(myList)):
        myList[i] = path + myList[i]
    return myList

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
                        nbFinger = nbFingerUp(hand_position)
                        hand_position = []
                        displayFinger(image, nbFinger, overlayList)
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == ord("q"):
                break
    cap.release()

if __name__ == '__main__':
    main()