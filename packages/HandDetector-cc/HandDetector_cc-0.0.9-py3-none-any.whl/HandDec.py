"""
Project : HandDetection-cc
version : 0.0.9
Developer : Chanchal Roy
Date : 20th Oct 2022
GitHub : https://github.com/Chexa12cc/HandDetector-cc
"""

# Required modules to work
# Try-Except block used if any module isn't installed it throws an error
try:
    import cv2
    import mediapipe
    import numpy
    import math
    import termcolor
except ImportError as i:
    print(termcolor.colored(f'Error! {i}', 'red'))

__author__ = 'Chanchal Roy'
__version__ = '0.0.9'
__all__ = ['HandDetector', 'init_cam', 'findHand', 'findLocations', 'fingerUp', 'findDistance', 'main']


# Base class of the module (HandDetector-cc)
class HandDetector:
    def __init__(
            self,
            cam_index: int = 0,
            win_width: int = 640,
            win_height: int = 360,
            cam_fps: int = 30,
            static_mode: bool = False,
            max_hands: int = 2,
            model_complex: int = 1,
            min_detection_con: float = 0.5,
            min_tracking_con: float = 0.5
    ):
        """
        Detects your hand using mediapipe in easier way and manipulate it using some cool functions and other stuffs!
        :param cam_index: Camera Index number(default 0)
        :param win_width: Cam window width in pixel(default 640)
        :param win_height: Cam window height in pixel(default 360)
        :param cam_fps: Cam window FPS(default 30) [Optional]
        :param static_mode: Picture or Live video as input(default False)
        :param max_hands: Maximum number of hands to detected(default 2)
        :param model_complex: Hand model complexity(default 1)
        :param min_detection_con: Minimum confidence to detect the hand(default 0.5)
        :param min_tracking_con: Minimum confidence to track the hand(default 0.5)
        """
        try:
            print(termcolor.colored("\nStarting Hand Detection...\n", 'green'))

            # Assigning the parameter values into class variables
            self.cam_index = cam_index
            self.win_width = win_width
            self.win_height = win_height
            self.cam_fps = cam_fps
            self.static_mode = static_mode
            self.max_hands = max_hands
            self.model_complex = model_complex
            self.min_detection_con = min_detection_con
            self.min_tracking_con = min_tracking_con

            self.mpHands = mediapipe.solutions.hands  # Hands module of mediapipe
            self.mpDraws = mediapipe.solutions.drawing_utils  # Drawing module of mediapipe
            self.mpStyle = mediapipe.solutions.drawing_styles  # Drawing styles of mediapipe

            # Initiating mediapipe hand detection
            self.hands = self.mpHands.Hands(
                self.static_mode,
                self.max_hands,
                self.model_complex,
                self.min_detection_con,
                self.min_tracking_con
            )
            self.fingerTipIDs = [4, 8, 12, 16, 20]  # Index numbers list of hand
        except Exception as e: print(termcolor.colored(f'Error! {e}', 'red'))

    def init_cam(self) -> numpy.ndarray:
        """
        Initiate your Webcam to grab computer vision.
        :return: Grabbed image as numpy ndarray.
        """
        try:
            self.cam = cv2.VideoCapture(self.cam_index, 700)
            self.cam.set(3, self.win_width)
            self.cam.set(4, self.win_height)
            self.cam.set(5, self.cam_fps)
            self.cam.set(6, cv2.VideoWriter_fourcc(*'MJPG'))

            return self.cam
        except Exception as e: print(termcolor.colored(f'Error! {e}', 'red'))

    def findHand(self, image: numpy.ndarray, draw_detect: bool = True, hand_connect: bool = True) -> numpy.ndarray:
        """
        Finds your hand and draws some detection over your hands.
        :param image: Grabbed image from your webcam.
        :param draw_detect: Bool value to draw the detection or not(default True).
        :param hand_connect: Bool value to draw the hand connection or not(default True).
        :return: Image as numpy ndarray.
        """
        try:
            imageRgb = cv2.cvtColor(image, 4)  # Converting BGR image to RGB image
            self.results = self.hands.process(imageRgb)  # Process the image to detect hands

            # Find the hand landmarks
            if self.results.multi_hand_landmarks:
                for handLms in self.results.multi_hand_landmarks:

                    # Draws detections on cam image
                    if draw_detect:
                        if hand_connect:
                            self.mpDraws.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS,
                                                        connection_drawing_spec=self.mpDraws.DrawingSpec((51, 255, 102)))
                        else:
                            self.mpDraws.draw_landmarks(image, handLms)

            return image
        except Exception as e: print(termcolor.colored(f'Error! {e}', 'red'))

    def findLocations(self, image: numpy.ndarray, hand_no: int = 0, draw_detect: bool = True,
                      draw_id: int | str = 'ALL') -> tuple:
        """
        Get the location of your hand.
        :param image: Grabbed image from your webcam as numpy ndarray.
        :param hand_no: Number of hand(default 0).
        :param draw_detect: Bool value to draw the detection or not(default True).
        :param draw_id: The hand lm ID to be drawn(default 'ALL').
        :return: List of hand landmark locations.
        """
        try:
            xList, yList, self.lmList = [], [], []
            self.bbox = ()
            self.win_height, self.win_width, c = image.shape  # Finds the cam window size

            # Find hand landmarks & assign it to variables
            if self.results.multi_hand_landmarks:
                try:
                    myHand = self.results.multi_hand_landmarks[hand_no]
                except:
                    myHand = self.results.multi_hand_landmarks[hand_no - 1]

                for id, handLm in enumerate(myHand.landmark):
                    cx, cy, cz = int(self.win_width * handLm.x), int(self.win_height * handLm.y), round(handLm.z, 2)
                    xList.append(cx)
                    yList.append(cy)
                    self.lmList.append((id, cx, cy, cz))

                    # Draws the detections on the hand image
                    if draw_detect:
                        if draw_id == 'ALL':
                            cv2.circle(image, (cx, cy), 13, (255, 255, 0), 2)
                        else:
                            if id == draw_id:
                                cv2.circle(image, (cx, cy), 13, (255, 255, 0), 2)

                # Creates a boundry box over hand image
                self.bbox = min(xList), min(yList), max(xList), max(yList)

            return self.lmList, self.bbox
        except Exception as e: print(termcolor.colored(f'Error! {e}', 'red'))

    def fingerUp(self) -> list:
        """
        Determines the fingers are up or down.
        :return: List of the fingers.
        """
        try:
            self.fingers = [0, 0, 0, 0, 0]  # List of fingers up/down value(0 for down & 1 for up)

            # Detects the thumb up or down
            if self.lmList[self.fingerTipIDs[0]][1] > self.lmList[self.fingerTipIDs[0] - 1][1]:
                self.fingers.pop(0)
                self.fingers.insert(0, 1)
            else:
                self.fingers.pop(0)
                self.fingers.insert(0, 0)

            # Detects the rest four fingers up or down
            for id in range(1, 5):
                if self.lmList[self.fingerTipIDs[id]][2] < self.lmList[self.fingerTipIDs[id] - 1][2]:
                    self.fingers.pop(id)
                    self.fingers.insert(id, 1)
                else:
                    self.fingers.pop(id)
                    self.fingers.insert(id, 0)

            return self.fingers
        except Exception as e: print(termcolor.colored(f'Error! {e}', 'red'))

    def findDistance(self, image: numpy.ndarray, p1_id: int, p2_id: int, draw_detect: bool = True) -> tuple:
        """
        Find the distance between two hand landmarks.
        :param image: Grabbed image from your webcam as numpy ndarray.
        :param p1_id: Point 1 hand landmark ID.
        :param p2_id: Point 2 hand landmark ID.
        :param draw_detect: Bool value to draw the detection or not(default True).
        :return: Tuple of image and length between two points.
        """
        try:
            x1, y1 = self.lmList[p1_id][1], self.lmList[p1_id][2]
            x2, y2 = self.lmList[p2_id][1], self.lmList[p2_id][2]
            px1, py1 = self.lmList[0][1], self.lmList[0][2]
            px2, py2 = self.lmList[9][1], self.lmList[9][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            self.palmLength = math.hypot((px2 - px1) ** 2, (py2 - py1) ** 2)
            self.length = round(math.hypot((x2 - x1) ** 2, (y2 - y1) ** 2) / self.palmLength, 2)

            if draw_detect:
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.circle(image, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
                cv2.circle(image, (x2, y2), 5, (255, 0, 255), cv2.FILLED)
                cv2.circle(image, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

            return self.length
        except Exception as e: print(termcolor.colored(f'Error! {e}', 'red'))


# Usage of the module
def main():
    import time

    timeS = time.time()

    class_obj = HandDetector()
    cam = class_obj.init_cam()

    while cam.isOpened():
        success, image = cam.read()
        if not success: continue

        detected_hand = class_obj.findHand(image, draw_detect=True)
        hand_landmark = class_obj.findLocations(image, draw_id=8)

        if hand_landmark[0] and hand_landmark[1]:

            finger_ups = class_obj.fingerUp()

            boundry = hand_landmark[1]
            cv2.rectangle(image, (boundry[0], boundry[1]), (boundry[2], boundry[3]), (0, 255, 255), 2)

            distance = class_obj.findDistance(image, 8, 12)
            print(f"Finger's Up : {finger_ups}       Finger Distance : {distance}")

        timeE = time.time()
        fps = int(1 / (timeE - timeS))
        timeS = timeE
        cv2.putText(image, str(f'FPS : {fps}'), (10, 30), 4, 1, (0, 255, 255), 3)
        cv2.imshow('Hand Detection - Chanchal Roy', image)
        if cv2.waitKey(1) & 0xff == ord('q'): break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
