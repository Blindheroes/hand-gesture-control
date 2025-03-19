# main.py (versi debugging)
import cv2
import mediapipe as mp
import pyautogui
import math
from controller import MouseController
from utils.gestures import identify_gesture, GESTURES
from utils.smoothing import SmoothingFilter


class HandGestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mouse = MouseController()
        self.smoother = SmoothingFilter()
        self.screen_w, self.screen_h = pyautogui.size()
        self.debug_text = []

    def get_finger_state(self, landmarks, joints):
        if joints == [1, 2, 3, 4]:  # Hanya untuk ibu jari
            # Gunakan 3 landmark: MCP (2), IP (3), dan tip (4)
            mcp = [landmarks[joints[0]].x, landmarks[joints[0]].y]
            ip = [landmarks[joints[1]].x, landmarks[joints[1]].y]
            tip = [landmarks[joints[2]].x, landmarks[joints[2]].y]

            # Hitung vektor
            vec1 = [ip[0] - mcp[0], ip[1] - mcp[1]]
            vec2 = [tip[0] - ip[0], tip[1] - ip[1]]

            # Hitung sudut antara vektor
            dot_product = vec1[0]*vec2[0] + vec1[1]*vec2[1]
            mag1 = (vec1[0]**2 + vec1[1]**2)**0.5
            mag2 = (vec2[0]**2 + vec2[1]**2)**0.5
            angle = math.degrees(math.acos(dot_product/(mag1*mag2 + 1e-8)))

            return 1 if angle > 100 else 0  # Threshold sudut
        else:
            # Logika original untuk jari lain
            tip_y = landmarks[joints[3]].y
            dip_y = landmarks[joints[2]].y
            return 1 if tip_y < dip_y else 0

    def process_frame(self, frame):
        self.debug_text = []  # Reset debug text
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        # Debug 1: Status deteksi tangan
        self.debug_text.append(
            f"Hands detected: {bool(results.multi_hand_landmarks)}")

        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0].landmark
            h, w, _ = frame.shape

            # Debug 2: Koordinat jari telunjuk
            index_finger = landmarks[8]
            self.debug_text.append(
                f"Index finger (X,Y): ({index_finger.x:.2f}, {index_finger.y:.2f})")

            # Konversi koordinat
            screen_x = int(index_finger.x * self.screen_w)
            screen_y = int(index_finger.y * self.screen_h)

            # Debug 3: Koordinat layar
            self.debug_text.append(
                f"Screen position: ({screen_x}, {screen_y})")

            # Deteksi status jari
            finger_states = {
                'thumb': self.get_finger_state(landmarks, [1, 2, 3, 4]),
                'index': self.get_finger_state(landmarks, [5, 6, 7, 8]),
                'middle': self.get_finger_state(landmarks, [9, 10, 11, 12]),
                'ring': self.get_finger_state(landmarks, [13, 14, 15, 16]),
                'pinky': self.get_finger_state(landmarks, [17, 18, 19, 20])
            }

            # Debug 4: Status jari
            finger_status = ", ".join(
                [f"{k}:{v}" for k, v in finger_states.items()])
            self.debug_text.append(f"Fingers: [{finger_status}]")

            current_gesture = identify_gesture(finger_states)
            self.debug_text.append(
                f"Current gesture: {current_gesture.upper()}")

            self.mouse.execute_action(current_gesture, screen_x, screen_y)

            # Visualisasi
            cv2.circle(frame, (int(index_finger.x*w),
                       int(index_finger.y*h)), 10, (0, 255, 0), -1)

        # Gambar debug text
        y_offset = 30
        for line in self.debug_text:
            cv2.putText(frame, line, (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            y_offset += 30

        return frame


if __name__ == "__main__":
    print("=== Starting Hand Gesture Control ===")
    print("Initializing webcam...")
    detector = HandGestureDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Failed to open webcam!")
        exit()

    print("Webcam initialized successfully")
    print("Press 'Q' to quit")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("ERROR: Failed to capture frame")
            break

        frame = detector.process_frame(frame)
        cv2.imshow('Hand Control - DEBUG MODE', frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            print("Exiting program...")
            break

    cap.release()
    cv2.destroyAllWindows()
