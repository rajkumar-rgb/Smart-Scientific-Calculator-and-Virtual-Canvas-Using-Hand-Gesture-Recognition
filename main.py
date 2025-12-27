import cv2
import mediapipe as mp

from virtual_calculator import run_calculator
from canvas import run_canvas


def main():
    # Use DirectShow for Windows camera stability
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Camera not accessible")
        return

    print("Camera opened successfully")

    # MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8
    )

    # Create visible main window (NOT fullscreen to avoid focus issues)
    cv2.namedWindow(
        "Unified Gesture Control Platform",
        cv2.WINDOW_NORMAL
    )

    # ================= MAIN LOOP =================
    while True:
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.flip(img, 1)

        # Instructions text
        cv2.putText(
            img,
            "C = Calculator | N = Canvas | Q = Quit",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

        cv2.imshow("Unified Gesture Control Platform", img)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            cv2.destroyAllWindows()
            run_calculator(cap, hands)
            cv2.namedWindow(
                "Unified Gesture Control Platform",
                cv2.WINDOW_NORMAL
            )

        elif key == ord('n'):
            cv2.destroyAllWindows()
            run_canvas(cap, hands)
            cv2.namedWindow(
                "Unified Gesture Control Platform",
                cv2.WINDOW_NORMAL
            )

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Camera closed cleanly")


if __name__ == "__main__":
    main()
