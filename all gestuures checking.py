class GestureRecognitionThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        gesture_dict = {
            'gesture1': 'Hello',
            'gesture2': 'Goodbye',
            'gesture3': 'Thumbs Up',
            'gesture4': 'Pointing Up',
            'gesture5': 'Middle Finger Up',
            'gesture6': 'Unknown Gesture'
        }
        cap = cv2.VideoCapture(0)
        with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        # Get the landmarks
                        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                        thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
                        index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

                        # Check if the thumb is above the base of the thumb and the index finger is below the base of the thumb
                        if thumb_tip.y < thumb_mcp.y and index_finger_tip.y > thumb_mcp.y:
                            gesture_text = gesture_dict['gesture3']  # Thumbs Up
                        # Check if the index finger is above the base of the thumb and the thumb is below the base of the thumb
                        elif index_finger_tip.y < thumb_mcp.y and thumb_tip.y > thumb_mcp.y:
                            gesture_text = gesture_dict['gesture4']  # Pointing Up
                        # Check if the middle finger is above the base of the thumb and the thumb and index finger are below the base of the thumb
                        elif middle_finger_tip.y < thumb_mcp.y and thumb_tip.y > thumb_mcp.y and index_finger_tip.y > thumb_mcp.y:
                            gesture_text = gesture_dict['gesture5']  # Middle Finger Up
                        else:
                            gesture_text = gesture_dict['gesture6']  # Unknown Gesture

                        cv2.putText(image, gesture_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        cap.release()

n = int(input("Enter the number of speakers: "))
SpeechToTextThread(n).start()
GestureRecognitionThread().start()
