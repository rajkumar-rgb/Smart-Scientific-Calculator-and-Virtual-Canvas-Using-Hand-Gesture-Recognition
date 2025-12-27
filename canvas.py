import cv2
import numpy as np
import mediapipe as mp


def run_canvas(cap, hands):
    mp_draw = mp.solutions.drawing_utils

    ret, img = cap.read()
    if not ret:
        return

    h, w, _ = img.shape
    canvas = np.zeros((h, w, 3), dtype=np.uint8)

    prev_x, prev_y = None, None

    cv2.namedWindow("Virtual Canvas", cv2.WINDOW_NORMAL)

    while True:
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            lm = result.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(img, lm, mp.solutions.hands.HAND_CONNECTIONS)

            # Index finger tip
            x = int(lm.landmark[8].x * w)
            y = int(lm.landmark[8].y * h)

            # Fingertips Y
            tips = [8, 12, 16, 20]
            bases = [6, 10, 14, 18]

            fingers_up = 0
            for tip, base in zip(tips, bases):
                if lm.landmark[tip].y < lm.landmark[base].y:
                    fingers_up += 1

            # ✍️ DRAW MODE → Only index finger up
            if fingers_up == 1:
                if prev_x is not None:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), (0, 255, 0), 5)
                prev_x, prev_y = x, y

            # ❌ ERASE MODE → Fist closed (no fingers up)
            elif fingers_up == 0:
                cv2.circle(canvas, (x, y), 45, (0, 0, 0), -1)
                prev_x, prev_y = None, None

            else:
                prev_x, prev_y = None, None

        else:
            prev_x, prev_y = None, None

        # Merge canvas with camera
        img = cv2.addWeighted(img, 0.7, canvas, 0.3, 0)

        # UI Text
        cv2.putText(img, "DRAW : Index Finger",
                    (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(img, "ERASE : Closed Fist",
                    (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        cv2.putText(img, "Press Q / ESC to Exit",
                    (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.imshow("Virtual Canvas", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            cv2.destroyWindow("Virtual Canvas")
            return
