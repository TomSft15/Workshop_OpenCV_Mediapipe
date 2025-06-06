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

def dispWhichFinger(tabFinger, image):
    color = (0, 0, 255)
    color1 = (0, 0, 255)
    color2 = (0, 0, 255)
    color3 = (0, 0, 255)
    color4 = (0, 0, 255)
    if (tabFinger[0] == 1):
        color = (0, 255, 0)
    if (tabFinger[1] == 1):
        color1 = (0, 255, 0)
    if (tabFinger[2] == 1):
        color2 = (0, 255, 0)
    if (tabFinger[3] == 1):
        color3 = (0, 255, 0)
    if (tabFinger[4] == 1):
        color4 = (0, 255, 0)
    cv2.putText(image, "Thumb",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(image, "Index finger",(10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, color1, 2)
    cv2.putText(image, "Middle finger",(10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, color2, 2)
    cv2.putText(image, "Ring finger",(10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, color3, 2)
    cv2.putText(image, "Little finger",(10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, color4, 2)

def main():
    hand_position = []
    overlayList = []
    nbFinger = 0
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
                        dispWhichFinger(tabFinger, image)
                        hand_position = []
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == ord("q"):
                break
    cap.release()

if __name__ == '__main__':
    main()
