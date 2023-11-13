import cv2 as cv
from cv2.typing import MatLike
import mediapipe as mp
import numpy as np
from numpy.typing import NDArray


class HandDetector:
  def __init__(self) -> None:
    self.mp_hands = mp.solutions.hands
    self.mp_drawing = mp.solutions.drawing_utils
    self.mp_styles = mp.solutions.drawing_styles
    self.hands = self.mp_hands.Hands()

  def findHands(self, frame: MatLike, draw=True) -> NDArray:
    # Convert to RGB
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Process hands
    result = self.hands.process(rgb_frame)
    if result.multi_hand_landmarks:
      if draw:
        for lms in result.multi_hand_landmarks:
          self.mp_drawing.draw_landmarks(
            frame,
            lms,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_styles.get_default_hand_landmarks_style(),
            self.mp_styles.get_default_hand_connections_style(),
          )

      return np.array(
        [
          [[lm.x, lm.y, lm.z] for lm in lms.landmark]
          for lms in result.multi_hand_landmarks
        ]
      )
    else:
      return np.array([])


if __name__ == "__main__":
  cap = cv.VideoCapture(0)
  detector = HandDetector()

  while cap.isOpened():
    # Capture frame by frame
    ret, frame = cap.read()

    if not ret:
      print("Failed to recieve frame. Exiting...")
      break

    result = detector.findHands(frame)
    print(result)
    print("shape", np.array(result).shape)

    # Flip frame and display
    cv.imshow("Hand Detection", cv.flip(frame, 1))

    # Listen for exit key
    if cv.waitKey(1) == ord("q"):
      break

  cap.release()
  cv.destroyAllWindows()
