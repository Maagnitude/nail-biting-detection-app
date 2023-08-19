import cv2
import mediapipe as mp
import time
from tools.send_email import Email
from tools.reward_system import Reward
from tools.sound_controller import SoundController
from tools.plot_data import PlotData

reward_system = Reward()
sound_controller = SoundController()
plotter = PlotData()

class NailBitingDetection():
    
    def __init__(self):
        # Initializing Mediapipe Hands module
        mp_hands = mp.solutions.hands
        self.hands = mp_hands.Hands()

        # Initializing Mediapipe Face Detection module
        mp_face_detection = mp.solutions.face_detection
        self.face_detection = mp_face_detection.FaceDetection()

        # Initialize OpenCV for camera capture
        self.cap = cv2.VideoCapture(0)
        
        self.hand_in_mouth_region = False

        self.printed = False
        self.music_filename = "resources/got_caught.mp3"
        self.nail_biting_count = 0
        self.last_bite_time = time.time()
        self.time_since_last_bite = 0.0

        # For timer
        self.countdown_duration = 10
        self.countdown_start_time = 0.0
        self.countdown_end_time = 0.0
        self.biting_duration = 0.0
        self.countdown_active = False
        self.time_biting = 0.0


    def detect(self, email_dict=None):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                continue

            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect face
            face_results = self.face_detection.process(rgb_frame)

            if face_results.detections:
                # Face detected
                for detection in face_results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = frame.shape
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                    
                    # Offsets for the mouth region
                    mouth_rect_left = x + 70
                    mouth_rect_top = y + 110
                    mouth_rect_right = x + w - 30
                    mouth_rect_bottom = y + h - 10
                    
                    # Draw a green square around the mouth
                    cv2.rectangle(frame, (mouth_rect_left, mouth_rect_top),
                                    (mouth_rect_right, mouth_rect_bottom), (0, 255, 0), 2)
                    
                    # Process frame with Mediapipe Hands
                    hand_results = self.hands.process(rgb_frame)
                    
                    if hand_results.multi_hand_landmarks:
                        # Hand detected
                        for hand_landmarks in hand_results.multi_hand_landmarks:
                            palm_landmarks = hand_landmarks.landmark[:9]
                            
                            # Calculate the center of the palm
                            palm_center_x = int(sum([lm.x for lm in palm_landmarks]) / len(palm_landmarks) * frame.shape[1])
                            palm_center_y = int(sum([lm.y for lm in palm_landmarks]) / len(palm_landmarks) * frame.shape[0])

                            square_size = 35
                            hand_rect_left = palm_center_x - square_size
                            hand_rect_top = palm_center_y - square_size
                            hand_rect_right = palm_center_x + square_size
                            hand_rect_bottom = palm_center_y + square_size
                            
                            # Draw a red square around the hand
                            cv2.rectangle(frame, (hand_rect_left, hand_rect_top),
                                        (hand_rect_right, hand_rect_bottom), (0, 0, 255), 2)
                            
                            mouth_region_x_range = range(mouth_rect_left, mouth_rect_right)
                            mouth_region_y_range = range(mouth_rect_top, mouth_rect_bottom)
                            
                            self.hand_in_mouth_region = (hand_rect_left in mouth_region_x_range or hand_rect_right in mouth_region_x_range) \
                                                    and (hand_rect_top in mouth_region_y_range or hand_rect_bottom in mouth_region_y_range)
                            
                            if self.hand_in_mouth_region:
                                # Hand is in the mouth region
                                self.last_bite_time = time.time()
                                self.time_since_last_bite = 0.0
                                reward_system.earned_rewards = []
                                if not sound_controller.is_playing():
                                    # Play sound as long as the hand is in the mouth region
                                    sound_controller.play_sound(self.music_filename)
                                    
                                if not self.countdown_active:
                                    # Initialize countdown timer
                                    self.countdown_start_time = time.time()
                                    plotter.time_stamps.append(time.strftime("%d-%m-%Y %H:%M:%S"))
                                    self.countdown_active = True
                                    self.nail_biting_count += 1 
                                    
                                if not self.printed:
                                    # Send an email once
                                    if email_dict is not None:
                                        email = Email(username=email_dict["username"], password=email_dict["password"], receiver_email=email_dict["receiver_email"])
                                        email.send_email(frame)
                                    
                                    # Print on the console once
                                    print(f"Nail biting detected at {time.strftime('%H:%M:%S')}!")
                                    self.printed = True
                            else:
                                # Hand is not in the mouth region
                                if self.countdown_active:
                                    self.countdown_end_time = time.time()
                                    self.biting_duration = self.countdown_end_time - self.countdown_start_time
                                    plotter.biting_durations.append(round(self.biting_duration, 3))
                                    print(f"Biting duration: {self.biting_duration:.3f}")
                                    self.countdown_active = False
                                self.time_since_last_bite = time.time() - self.last_bite_time
                                # Check for earned rewards
                                reward_system.check_for_rewards(self.time_since_last_bite)
                                self.printed = False
                    else:
                        if not self.countdown_active:
                            self.time_since_last_bite = time.time() - self.last_bite_time
                            # Check for earned rewards
                            reward_system.check_for_rewards(self.time_since_last_bite)
                        self.printed = False
            else:
                self.printed = False
                
            # Display countdown timer
            if self.countdown_active:
                self.time_biting = time.time() - self.countdown_start_time
                if self.time_biting > 0.0:
                    cv2.putText(frame, f"Biting for: {int(self.time_biting)}s", (10, 460), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                # Displaying no-biting timer
                cv2.putText(frame, f"Clean for: {self.time_since_last_bite:.0f}s", (10, 460), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                
            # Displaying nail-biting count and rewards
            if reward_system.earned_rewards.__len__() > 0:
                cv2.putText(frame, f"Title: {reward_system.earned_rewards[-1]}", (10, 60), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, "Title: Noob", (10, 60), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                
            # Displaying nail-biting count
            cv2.putText(frame, f"Caught: {self.nail_biting_count} times", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow("Biting Nails Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            
            # To plot the data
            plotter.plot_data(self.hand_in_mouth_region)

        sound_controller.close()
        self.cap.release()
        cv2.destroyAllWindows()