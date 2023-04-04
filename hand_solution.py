import mediapipe as mp
import cv2


def main():
    # Declaring Hand model
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    #drawing mediapipe solutions
    mpDraw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    with mpHands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) \
        as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
                    print(id, cx, cy);
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == ord("q"):
                break
    cap.release()
    

if __name__ == '__main__':
    main()
    