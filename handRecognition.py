import cv2 as cv
import mediapipe as mp

cap = cv.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame by frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to recieve frame. Exiting...")
        break

    # Convert to RGB
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Process hands
    result = hands.process(rgb_frame)
    if result.multi_hand_landmarks:
        for landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

    # Display frame
    cv.imshow("frame", frame)

    # Liste for exit key
    if cv.waitKey(1) == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
