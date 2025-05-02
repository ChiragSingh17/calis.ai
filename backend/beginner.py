import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import threading
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

engine = pyttsx3.init()
speak_lock = threading.Lock()

def speak(text):
    with speak_lock:
        engine.say(text)
        engine.runAndWait()

previous_pose = "Let's try to hold for a bit!"
last_spoken_time = 0
cooldown = 3
cap = cv2.VideoCapture(0)

start_time = time.time()
correct_pose_start_time = None
total_correct_time = 0
target_hold_time = 3
motivational_messages = [
    "You're doing great!",
    "Keep it up!",
    "Every second counts!",
    "Feel that strength building!",
    "Almost there!",
    "Good effort!",
    "Keep trying to lift!",
    "Feel those muscles working!",
    "Every attempt makes you stronger!",
    "Almost got it!",
]

message_index = 0

#---------------------------------------------------------------------------------------------------

def beginner_lsit(cap, cooldown, last_spoken_time, previous_pose, mp_drawing, mp_pose, start_time, correct_pose_start_time, total_correct_time, target_hold_time, motivational_messages, message_index):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            h, w, _ = image.shape

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                def get_point(landmark):
                    return [landmarks[landmark.value].x, landmarks[landmark.value].y]

                l_shoulder = get_point(mp_pose.PoseLandmark.LEFT_SHOULDER)
                l_ear = get_point(mp_pose.PoseLandmark.LEFT_EAR)
                l_hip = get_point(mp_pose.PoseLandmark.LEFT_HIP)
                l_knee = get_point(mp_pose.PoseLandmark.LEFT_KNEE)
                l_ankle = get_point(mp_pose.PoseLandmark.LEFT_ANKLE)
                r_ear = get_point(mp_pose.PoseLandmark.RIGHT_EAR)
                r_shoulder = get_point(mp_pose.PoseLandmark.RIGHT_SHOULDER)
                r_hip = get_point(mp_pose.PoseLandmark.RIGHT_HIP)
                r_knee = get_point(mp_pose.PoseLandmark.RIGHT_KNEE)
                r_ankle = get_point(mp_pose.PoseLandmark.RIGHT_ANKLE)

                head_angle_l = calculate_angle(l_ear, l_shoulder, l_hip)
                back_angle_l = calculate_angle(l_shoulder, l_hip, l_knee)
                leg_angle_l = calculate_angle(l_hip, l_knee, l_ankle)
                head_angle_r = calculate_angle(r_ear, r_shoulder, r_hip)
                back_angle_r = calculate_angle(r_shoulder, r_hip, r_knee)
                leg_angle_r = calculate_angle(r_hip, r_knee, r_ankle)

                if not 160 < head_angle_l < 200 and not 160 < head_angle_r < 200:
                    pose_status = "Try to keep your head straighter."
                elif not 70 < back_angle_l < 110 and not 70 < back_angle_r < 110:
                    pose_status = "Focus on keeping your back straight."
                elif not 160 < leg_angle_l < 205 and not 160 < leg_angle_r < 205:
                    pose_status = "Try to straighten your legs more."
                else:
                    pose_status = "Looking good!"

                current_time = time.time()
                if pose_status != previous_pose and (current_time - last_spoken_time) > cooldown:
                    threading.Thread(target=speak, args=(pose_status,), daemon=True).start()
                    print("Feedback : ", pose_status)
                    previous_pose = pose_status
                    last_spoken_time = current_time

                if "Looking good" in pose_status:
                    if correct_pose_start_time is None:
                        correct_pose_start_time = current_time
                    elif current_time - correct_pose_start_time >= target_hold_time:
                        if (current_time - last_spoken_time) > cooldown:
                            threading.Thread(target=speak, args=(motivational_messages[message_index % len(motivational_messages)],), daemon=True).start()
                            print("Motivational Feedback:", motivational_messages[message_index % len(motivational_messages)])
                            last_spoken_time = current_time
                            message_index += 1
                        total_correct_time += (current_time - correct_pose_start_time)
                        correct_pose_start_time = None
                else:
                    if correct_pose_start_time is not None:
                        total_correct_time += current_time - correct_pose_start_time
                        correct_pose_start_time = None

                all_angles = [head_angle_l, back_angle_l, leg_angle_l, head_angle_r, back_angle_r, leg_angle_r]
                ideal_angles = [180, 90, 180, 180, 90, 180]
                errors = [abs(a - b) for a, b in zip(ideal_angles, all_angles)]
                accuracies = [max(0, 100 - (e / 45) * 100) for e in errors]
                avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0

                cv2.putText(image, f"{int(leg_angle_l)}", tuple(np.multiply(l_knee, [w, h]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(image, f"{int(leg_angle_r)}", tuple(np.multiply(r_knee, [w, h]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                indicator_color = (0, 255, 0) if "Looking good" in pose_status else (0, 0, 255)
                cv2.circle(image, center=(50, 50), radius=20, color=indicator_color, thickness=-1)

                cv2.putText(image, f"Hold Time: {int(current_time - start_time) if correct_pose_start_time is not None else int(total_correct_time)}s",
                            (w - 280, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 215, 0), 2)

                cv2.putText(image, pose_status, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2),
                                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2))

            cv2.imshow("Beginner L-sit Feedback", image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Total time: {int(time.time() - start_time)} seconds")
    print(f"Total time with good form: {int(total_correct_time)} seconds")

#-------------------------------------------------------------------------------------------------------

def beginner_handstand(cap, cooldown, last_spoken_time, previous_pose, mp_drawing, mp_pose, start_time, correct_pose_start_time, total_correct_time, target_hold_time, motivational_messages, message_index):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Couldn't read from camera.")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            h, w, _ = image.shape

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                def get_point(landmark):
                    return [landmarks[landmark.value].x, landmarks[landmark.value].y]

                l_shoulder = get_point(mp_pose.PoseLandmark.LEFT_SHOULDER)
                r_shoulder = get_point(mp_pose.PoseLandmark.RIGHT_SHOULDER)
                l_elbow = get_point(mp_pose.PoseLandmark.LEFT_ELBOW)
                r_elbow = get_point(mp_pose.PoseLandmark.RIGHT_ELBOW)
                l_wrist = get_point(mp_pose.PoseLandmark.LEFT_WRIST)
                r_wrist = get_point(mp_pose.PoseLandmark.RIGHT_WRIST)
                l_hip = get_point(mp_pose.PoseLandmark.LEFT_HIP)
                r_hip = get_point(mp_pose.PoseLandmark.RIGHT_HIP)
                l_knee = get_point(mp_pose.PoseLandmark.LEFT_KNEE)
                r_knee = get_point(mp_pose.PoseLandmark.RIGHT_KNEE)
                l_ankle = get_point(mp_pose.PoseLandmark.LEFT_ANKLE)
                r_ankle = get_point(mp_pose.PoseLandmark.RIGHT_ANKLE)
                nose = get_point(mp_pose.PoseLandmark.NOSE)

                shoulder_angle_l = calculate_angle(l_elbow, l_shoulder, l_hip)
                shoulder_angle_r = calculate_angle(r_elbow, r_shoulder, r_hip)
                elbow_angle_l = calculate_angle(l_wrist, l_elbow, l_shoulder)
                elbow_angle_r = calculate_angle(r_wrist, r_elbow, r_shoulder)
                hip_angle_l = calculate_angle(l_shoulder, l_hip, l_knee)
                hip_angle_r = calculate_angle(r_shoulder, r_hip, r_knee)
                knee_angle_l = calculate_angle(l_hip, l_knee, l_ankle)
                knee_angle_r = calculate_angle(r_hip, r_knee, r_ankle)

                is_upside_down = nose[1] < l_shoulder[1] and nose[1] < r_shoulder[1]
                is_straight_body = (160 < hip_angle_l < 200 and 160 < hip_angle_r < 200 and
                                    160 < knee_angle_l < 200 and 160 < knee_angle_r < 200 and
                                    150 < elbow_angle_l < 210 and 150 < elbow_angle_r < 210 and
                                    80 < shoulder_angle_l < 110 and 80 < shoulder_angle_r < 110)

                if not is_upside_down:
                    pose_status = "Try to get upside down safely!"
                elif not is_straight_body:
                    pose_status = "Focus on aligning your body."
                else:
                    pose_status = "You're inverted! Keep trying to hold."

                current_time = time.time()
                if pose_status != previous_pose and (current_time - last_spoken_time) > cooldown:
                    threading.Thread(target=speak, args=(pose_status,), daemon=True).start()
                    print("Feedback : ", pose_status)
                    previous_pose = pose_status
                    last_spoken_time = current_time

                if "inverted" in pose_status:
                    if correct_pose_start_time is None:
                        correct_pose_start_time = current_time
                    elif current_time - correct_pose_start_time >= target_hold_time:
                        if (current_time - last_spoken_time) > cooldown:
                            threading.Thread(target=speak, args=(motivational_messages[message_index % len(motivational_messages)],), daemon=True).start()
                            print("Motivational Feedback:", motivational_messages[message_index % len(motivational_messages)])
                            last_spoken_time = current_time
                            message_index += 1
                        total_correct_time += (current_time - correct_pose_start_time)
                        correct_pose_start_time = None
                else:
                    if correct_pose_start_time is not None:
                        total_correct_time += current_time - correct_pose_start_time
                        correct_pose_start_time = None

                cv2.putText(image, f"Hold Time: {int(current_time - start_time) if correct_pose_start_time else int(total_correct_time)}s",
                            (10, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, pose_status, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2),
                                          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2))

            cv2.imshow("Beginner Handstand Feedback", image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Total time: {int(time.time() - start_time)} seconds")
    print(f"Total time inverted (even briefly): {int(total_correct_time)} seconds")

#-------------------------------------------------------------------------------------------------------

def beginner_frontlever(cap, cooldown, last_spoken_time, previous_pose, mp_drawing, mp_pose,
                        start_time, correct_pose_start_time, total_correct_time, target_hold_time,
                        motivational_messages, message_index):

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                def get_point(landmark):
                    return [landmarks[landmark.value].x, landmarks[landmark.value].y]

                # Get keypoints
                l_shoulder = get_point(mp_pose.PoseLandmark.LEFT_SHOULDER)
                l_elbow = get_point(mp_pose.PoseLandmark.LEFT_ELBOW)
                l_wrist = get_point(mp_pose.PoseLandmark.LEFT_WRIST)
                l_hip = get_point(mp_pose.PoseLandmark.LEFT_HIP)
                l_knee = get_point(mp_pose.PoseLandmark.LEFT_KNEE)
                l_ankle = get_point(mp_pose.PoseLandmark.LEFT_ANKLE)

                r_shoulder = get_point(mp_pose.PoseLandmark.RIGHT_SHOULDER)
                r_elbow = get_point(mp_pose.PoseLandmark.RIGHT_ELBOW)
                r_wrist = get_point(mp_pose.PoseLandmark.RIGHT_WRIST)
                r_hip = get_point(mp_pose.PoseLandmark.RIGHT_HIP)
                r_knee = get_point(mp_pose.PoseLandmark.RIGHT_KNEE)
                r_ankle = get_point(mp_pose.PoseLandmark.RIGHT_ANKLE)

                # Thresholds
                arm_straight_threshold = 160
                back_straight_threshold = 150
                shoulder_raise_threshold = 70

                # Angles
                hand_angle_l = calculate_angle(l_wrist, l_elbow, l_shoulder)
                shoulder_angle_l = calculate_angle(l_elbow, l_shoulder, l_hip)
                back_angle_l = calculate_angle(l_shoulder, l_hip, l_knee)
                leg_angle_l = calculate_angle(l_hip, l_knee, l_ankle)

                hand_angle_r = calculate_angle(r_wrist, r_elbow, r_shoulder)
                shoulder_angle_r = calculate_angle(r_elbow, r_shoulder, r_hip)
                back_angle_r = calculate_angle(r_shoulder, r_hip, r_knee)
                leg_angle_r = calculate_angle(r_hip, r_knee, r_ankle)

                # Conditions
                is_arms_straight = hand_angle_l > arm_straight_threshold and hand_angle_r > arm_straight_threshold
                is_back_arching = back_angle_l > back_straight_threshold and back_angle_r > back_straight_threshold
                are_shoulders_raised = shoulder_angle_l < shoulder_raise_threshold and shoulder_angle_r < shoulder_raise_threshold
                are_legs_straight = leg_angle_l > (arm_straight_threshold - 20) and leg_angle_r > (arm_straight_threshold - 20)

                # Feedback logic
                if not is_arms_straight:
                    pose_status = "Try to straighten your arms."
                elif not are_shoulders_raised:
                    pose_status = "Try to raise your hips higher."
                elif not is_back_arching:
                    pose_status = "Try to arch your back less."
                elif not are_legs_straight:
                    pose_status = "Try to straighten your legs."
                elif are_shoulders_raised and is_back_arching and is_arms_straight and are_legs_straight:
                    pose_status = "You're lifting! Try to hold."
                else:
                    pose_status = "Keep trying to find the position."

                # Speech feedback
                current_time = time.time()
                if pose_status != previous_pose and (current_time - last_spoken_time) > cooldown:
                    threading.Thread(target=speak, args=(pose_status,), daemon=True).start()
                    print("Feedback:", pose_status)
                    previous_pose = pose_status
                    last_spoken_time = current_time

                # Hold tracking
                if "lifting" in pose_status:
                    if correct_pose_start_time is None:
                        correct_pose_start_time = current_time
                    elif current_time - correct_pose_start_time >= target_hold_time:
                        if (current_time - last_spoken_time) > cooldown:
                            message = motivational_messages[message_index % len(motivational_messages)]
                            threading.Thread(target=speak, args=(message,), daemon=True).start()
                            print("Motivational Feedback:", message)
                            last_spoken_time = current_time
                            message_index += 1
                        total_correct_time += current_time - correct_pose_start_time
                        correct_pose_start_time = None
                else:
                    if correct_pose_start_time is not None:
                        total_correct_time += current_time - correct_pose_start_time
                        correct_pose_start_time = None

        cap.release()
        cv2.destroyAllWindows()

        return {
            "total_correct_time": total_correct_time,
            "last_pose": previous_pose,
            "last_message_time": last_spoken_time,
            "message_index": message_index
        }


n = input("Enter The Skill to perform : ")
if n == "lsit":
    beginner_lsit(cap, cooldown, last_spoken_time, previous_pose, mp_drawing, mp_pose, start_time, correct_pose_start_time, total_correct_time, target_hold_time, motivational_messages, message_index)
elif n == "handstand":
    beginner_handstand(cap, cooldown, last_spoken_time, previous_pose, mp_drawing, mp_pose, start_time, correct_pose_start_time, total_correct_time, target_hold_time, motivational_messages, message_index)
elif n == "frontlever":
    beginner_frontlever(cap, cooldown, last_spoken_time, previous_pose, mp_drawing, mp_pose, start_time, correct_pose_start_time, total_correct_time, target_hold_time, motivational_messages, message_index)
else:
    pass