
import cv2
from hand_tracking import HandTracker


def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    tracker = HandTracker()

    if not cap.isOpened():
        print("Could not open webcam.")
        tracker.close()
        return

    print("AirScroll pinch detection test started!")
    print("Bring your thumb and index finger together.")
    print("Press Q to quit.")

    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)
        frame, results = tracker.process_frame(frame)

        distance = tracker.get_pinch_distance(results)

        if distance is not None:
            if distance < 0.05:
                status = "PINCH DETECTED"
                color = (0, 255, 0)
            else:
                status = "HAND OPEN"
                color = (0, 165, 255)

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
                f"Distance: {distance:.3f}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
        else:
            cv2.putText(
                frame,
                "No hand detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        cv2.imshow("AirScroll - Pinch Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    tracker.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
