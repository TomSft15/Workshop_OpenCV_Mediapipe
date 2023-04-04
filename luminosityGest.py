import cv2
import mediapipe as mp
import os
import math
import screen_brightness_control as sbc

def luminosityGesture(image, hand_position):
    fingerDistance = 0
    normalizedDistance = 0
    new_volume = 0
    # Récupérer le chemin absolu de la luminosité
    # brightness_path = '/sys/class/backlight/intel_backlight/brightness'

    # # Lire la valeur de luminosité actuelle
    # with open(brightness_path, 'r') as f:
    #     brightness = int(f.read())

    # # Récupérer la valeur maximale de luminosité
    # max_brightness_path = '/sys/class/backlight/intel_backlight/max_brightness'
    # with open(max_brightness_path, 'r') as f:
    #     max_brightness = int(f.read())

    x1, y1 = hand_position[4][1], hand_position[4][2]
    x2, y2 = hand_position[8][1], hand_position[8][2]
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    
    cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
    cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
    cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
    cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
    fingerDistance = math.hypot(x2 - x1, y2 - y1)
    normalizedDistance = ((fingerDistance - 10) / (220 - 10)) * 100
    if (normalizedDistance > 100):
        normalizedDistance = 100
    print(int(normalizedDistance))
    result = os.popen("amixer sget Master").readline()
    if "%" in result:
        volume = int(result[result.index('[')+1:result.index('%')])
    else:
        volume = 0
    if (normalizedDistance < 50):
        volume = volume - 5
    if (normalizedDistance > 50):
        volume = volume + 5
    if (normalizedDistance > 0):
        # Définir le nouveau volume
        os.system("amixer sset Master " + str(volume) + "%")

def main():
    hand_position = []
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
                    hand_position.append([id, cx, cy])
                    if (len(hand_position) == 21):
                        luminosityGesture(image, hand_position)
                        hand_position = []
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == ord("q"):
                break
    cap.release()
    

if __name__ == '__main__':
    main()