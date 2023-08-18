import cv2
import mediapipe as mp
import pygame
import time
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize pygame for audio
pygame.mixer.init()

time_stamps = []
nail_biting_counts = []

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection()

# Initialize OpenCV for camera capture
cap = cv2.VideoCapture(0)

printed = False
music_filename = "resources/got_caught.mp3"
nail_biting_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect face
    face_results = face_detection.process(rgb_frame)

    if face_results.detections:
        for detection in face_results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            
            mouth_rect_left = x
            mouth_rect_top = y
            mouth_rect_right = x + w
            mouth_rect_bottom = y + h
            
            # Draw a green square around the mouth
            cv2.rectangle(frame, (mouth_rect_left, mouth_rect_top),
                            (mouth_rect_right, mouth_rect_bottom), (0, 255, 0), 2)
            
            # Process frame with Mediapipe Hands
            hand_results = hands.process(rgb_frame)
            
            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    palm_landmarks = hand_landmarks.landmark[:9]
                    
                    # Calculate the center of the palm
                    palm_center_x = int(sum([lm.x for lm in palm_landmarks]) / len(palm_landmarks) * frame.shape[1])
                    palm_center_y = int(sum([lm.y for lm in palm_landmarks]) / len(palm_landmarks) * frame.shape[0])

                    square_size = 30
                    hand_rect_left = palm_center_x - square_size
                    hand_rect_top = palm_center_y - square_size
                    hand_rect_right = palm_center_x + square_size
                    hand_rect_bottom = palm_center_y + square_size
                    
                    cv2.rectangle(frame, (hand_rect_left, hand_rect_top),
                                (hand_rect_right, hand_rect_bottom), (0, 0, 255), 2)
                    
                    mouth_region_x_range = range(mouth_rect_left, mouth_rect_right)
                    mouth_region_y_range = range(mouth_rect_top, mouth_rect_bottom)
                    
                    hand_in_mouth_region = (hand_rect_left in mouth_region_x_range or hand_rect_right in mouth_region_x_range) and (hand_rect_top in mouth_region_y_range or hand_rect_bottom in mouth_region_y_range)
                    
                    if hand_in_mouth_region and not pygame.mixer.music.get_busy():
                        if not printed:
                            print(f"Nail biting detected at {time.strftime('%H:%M:%S')}!")
                            printed = True
                        pygame.mixer.music.load(music_filename)
                        pygame.mixer.music.play()
                        nail_biting_count += 1 
                        
                        time_stamps.append(datetime.now())
                        nail_biting_counts.append(nail_biting_count)
                    else:
                        printed = False
            else:
                printed = False
    else:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        printed = False
        
    # Display nail-biting count
    cv2.putText(frame, f"Caught Nail Biting: {nail_biting_count} times", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow("Eating Nails Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    # Display the nail-biting count chart
    plt.clf()
    plt.plot(time_stamps, nail_biting_counts, marker='o')
    plt.xlabel('Time')
    plt.ylabel('Nail Biting Count')
    plt.title('Nail Biting Detection Chart')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the chart in a separate window
    plt.pause(0.01)

pygame.mixer.music.stop()
pygame.mixer.music.unload()
pygame.mixer.quit()
cap.release()
cv2.destroyAllWindows()