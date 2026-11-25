
import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

        self.results = None

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return frame, self.results

    def get_index_finger_position(self, results, frame_shape):
        if results and results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            index_tip = hand_landmarks.landmark[
                self.mp_hands.HandLandmark.INDEX_FINGER_TIP
            ]

            height, width = frame_shape[:2]

            x = int(index_tip.x * width)
            y = int(index_tip.y * height)

            return x, y

        return None

    def close(self):
        self.hands.close()
