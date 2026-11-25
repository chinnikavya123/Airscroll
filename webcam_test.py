
import cv2
from hand_tracking import HandTracker


def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    tracker = HandTracker()

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        tracker.close()
        return

    print("AirScroll webcam test started!")
    print("Press Q to quit.")

    while True:
        success, frame = cap.read()

        if not success:
            print("Failed to read webcam frame.")
            break

        frame = cv2.flip(frame, 1)

        frame, results = tracker.process_frame(frame)

        position = tracker.get_index_finger_position(
            results, frame.shape
        )

        if position:
            x, y = position

            cv2.circle(frame, (x, y), 12, (0, 255, 0), -1)

            cv2.putText(
                frame,
                f"Index Finger: X={x}, Y={y}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
        else:
            cv2.putText(
                frame,
                "No hand detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

        cv2.imshow("AirScroll - Hand Tracking Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    tracker.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
