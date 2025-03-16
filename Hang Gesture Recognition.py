import cv2
import mediapipe as mp

# Define a dictionary for the gestures
gesture_dict = {
    'gesture1': 'High Five',
    'gesture3': 'Thumbs Up',
    'gesture4': 'Pointing Up',
    'gesture5': 'Middle Finger Up',
    'gesture6': 'Unknown Gesture',
    'gesture8': 'Gun',
    'gesture9': 'Salute',
    'gesture11': 'Loser',
    'gesture12': 'Winner',
    'gesture13': 'Clenched Fist',
    'gesture14': 'Call Me',
    'gesture15': 'Palm',
    'gesture16': 'Handshake',
    'gesture17': 'Thumbs Up'
}

# Define a function to check the gesture
def check_gesture(thumb_tip1, thumb_mcp1, index_finger_tip1, middle_finger_tip1, pinky_tip1):
    if thumb_tip1.y < thumb_mcp1.y and index_finger_tip1.y > thumb_mcp1.y and pinky_tip1.y > thumb_mcp1.y:
        return gesture_dict['gesture3']  # Thumbs Up
    elif middle_finger_tip1.x > thumb_tip1.y and index_finger_tip1.x < thumb_mcp1.y and thumb_tip1.x > thumb_mcp1.x:
        return gesture_dict['gesture4']  # Pointing Up
    elif middle_finger_tip1.y < thumb_mcp1.y and thumb_tip1.y > thumb_mcp1.y and index_finger_tip1.y > thumb_mcp1.y:
        return gesture_dict['gesture5']  # Middle Finger Up
    elif thumb_tip1.y < thumb_mcp1.y and index_finger_tip1.y < thumb_mcp1.y and middle_finger_tip1.x < thumb_mcp1.y:
        return gesture_dict['gesture1']  # High Five
    elif index_finger_tip1.y < thumb_mcp1.y and middle_finger_tip1.y < thumb_mcp1.y and thumb_tip1.y > thumb_mcp1.y:
        return gesture_dict['gesture9']  # Salute
    elif thumb_tip1.y < thumb_mcp1.y and index_finger_tip1.y < thumb_mcp1.y and middle_finger_tip1.y < thumb_mcp1.y:
        return gesture_dict['gesture11']  # Loser
    elif thumb_tip1.y < thumb_mcp1.x and middle_finger_tip1.x > thumb_mcp1.x:
        return gesture_dict['gesture8']  # Gun
    elif thumb_tip1.y < thumb_mcp1.y and index_finger_tip1.y < thumb_mcp1.y and middle_finger_tip1.y > thumb_mcp1.y:
        return gesture_dict['gesture12']  # Winner
    elif thumb_tip1.y < thumb_mcp1.y and index_finger_tip1.y < thumb_mcp1.y and middle_finger_tip1.y < thumb_mcp1.y:
        return gesture_dict['gesture12']  # Wave
    elif thumb_tip1.y > thumb_mcp1.y and index_finger_tip1.y > thumb_mcp1.y and middle_finger_tip1.y > thumb_mcp1.y:
        return gesture_dict['gesture13']  # Clenched Fist
    elif pinky_tip1.x < thumb_mcp1.y and index_finger_tip1.y > thumb_mcp1.y and middle_finger_tip1.y > thumb_mcp1.y:
        return gesture_dict['gesture14']  # Call Me
    elif thumb_tip1.x > thumb_mcp1.y and index_finger_tip1.x > index_finger_mcp1.y and middle_finger_tip1.x > middle_finger_mcp1.y and pinky_tip1.x > pinky_mcp1.y:
        return gesture_dict['gesture15']  # Palm
    elif thumb_tip1.x > index_finger_tip1.x and thumb_tip1.x > middle_finger_mcp1.x and thumb_tip1.x > thumb_mcp1.x:
        return gesture_dict['gesture16']  # Handshake
    elif thumb_tip1.y > thumb_mcp1.y and index_finger_tip1.y < index_finger_mcp1.y and middle_finger_tip1.y < middle_finger_mcp1.y and ring_finger_tip1.y < ring_finger_mcp1.y and pinky_tip1.y < pinky_mcp1.y:
        return gesture_dict['gesture17']  # Thumbs Up
    else:
        return gesture_dict['gesture6']  # Unknown Gesture

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize MediaPipe Drawing Utility
mp_drawing = mp.solutions.drawing_utils

# Initialize the video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip the frame horizontally for a selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and draw the hand landmarks
    results = hands.process(rgb_image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip1 = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_mcp1 = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
            index_finger_tip1 = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip1 = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            pinky_tip1 = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # Use the function to check the gesture
            gesture_text = check_gesture(thumb_tip1, thumb_mcp1, index_finger_tip1, middle_finger_tip1, pinky_tip1)

            # Draw the hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Display the gesture text
            cv2.putText(frame, gesture_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the image
    cv2.imshow('MediaPipe Hands', frame)

    # Exit if ESC key is pressed
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release the video capture and close the windows
cap.release()
cv2.destroyAllWindows()
