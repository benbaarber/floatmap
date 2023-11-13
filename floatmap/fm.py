import cv2 as cv
from typing import Callable
from numpy.typing import NDArray
from hands import HandDetector
import asyncio


class Floatmap:
  def __init__(self) -> None:
    self.detector = HandDetector()
    self.feed = cv.VideoCapture(0)

  def record(self, on_data: Callable[[NDArray], None]) -> None:
    while self.feed.isOpened():
      # Capture frame by frame
      ret, frame = self.feed.read()

      if not ret:
        print("Failed to recieve frame. Exiting...")
        break

      result = self.detector.findHands(frame, draw=False)
      asyncio.run(on_data(result))

      # Flip frame and display
      # cv.imshow("Hand Detection", cv.flip(frame, 1))
    else:
      self.kill()

  def kill(self):
    self.feed.release()
    cv.destroyAllWindows()
