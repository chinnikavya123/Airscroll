
import cv2
import pyautogui
from hand_tracking import HandTracker
from collections import deque

pyautogui.FAILSAFE = True

SCROLL_SPEED = 35
MOVEMENT_THRESHOLD = 8
PINCH_THRESHOLD = 0.05


def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    tracker = HandTracker()

    if not cap.isOpened():
        print("Could not open webcam.")
        tracker.close()
        return

    previous_y = None
    paused = False
    previous_pinch = False
    smooth_positions = deque(maxlen=5)

    print("AirScroll gesture scrolling started!")
    print("Move your index finger up and down to scroll.")
    print("Pinch to pause or resume.")
    print("Press Q to quit.")

    try:
        while True:
            success, frame = cap.read()

            if not success:
                break

            frame = cv2.flip(frame, 1)
            frame, results = tracker.process_frame(frame)

            position = tracker.get_index_finger_position(
                results, frame.shape
            )

            pinch_distance = tracker.get_pinch_distance(results)

            if pinch_distance is not None:
                current_pinch = pinch_distance < PINCH_THRESHOLD

                if current_pinch and not previous_pinch:
                    paused = not paused
                    previous_y = None
                    smooth_positions.clear()

                previous_pinch = current_pinch

            if position and not paused:
                x, y = position
                smooth_positions.append(y)

                current_y = sum(smooth_positions) / len(smooth_positions)

                if previous_y is not None:
                    movement = previous_y - current_y

                    if abs(movement) > MOVEMENT_THRESHOLD:
                        if movement > 0:
                            pyautogui.scroll(SCROLL_SPEED)
                        else:
                            pyautogui.scroll(-SCROLL_SPEED)

                previous_y = current_y

            else:
                previous_y = None
                smooth_positions.clear()

            if paused:
                status = "SCROLLING PAUSED"
                color = (0, 0, 255)
            else:
                status = "SCROLLING ACTIVE"
                color = (0, 255, 0)

            cv2.putText(
                frame,
                status,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

            cv2.putText(
                frame,
                f"Scroll Speed: {SCROLL_SPEED}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.imshow("AirScroll - Gesture Scrolling", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except pyautogui.FailSafeException:
        print("AirScroll stopped using PyAutoGUI failsafe.")

    finally:
        cap.release()
        tracker.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
