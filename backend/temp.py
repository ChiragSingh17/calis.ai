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

previous_pose = "Perfect form ! Keep it up!"
last_spoken_time = 0
cooldown = 2

cap = cv2.VideoCapture(0)

start_time = time.time()
correct_pose_start_time = None
total_correct_time = 0

#---------------------------------------------------------------------------------------------------

def lsit(cap, cooldown, last_spoken_time, previous_pose, mp_drawing, mp_pose, start_time, correct_pose_start_time, total_correct_time):
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

                if not 170 < head_angle_l < 190 and not 170 < head_angle_r < 190:
                    pose_status = "Keep your head straight"
                elif not 80 < back_angle_l < 100 and not 80 < back_angle_r < 100:
                    pose_status = "Keep your back straight"
                elif not 170 < leg_angle_l < 195 and not 170 < leg_angle_r < 190:
                    pose_status = "Keep your legs straight"
                else:
                    pose_status = "Perfect form ! Keep it up!"

                current_time = time.time()
                if pose_status != previous_pose and (current_time - last_spoken_time) > cooldown:
                    threading.Thread(target=speak, args=(pose_status,), daemon=True).start()
                    print("Feedback : ", pose_status)
                    previous_pose = pose_status
                    last_spoken_time = current_time

                if "Perfect" in pose_status:
                    if correct_pose_start_time is None:
                        correct_pose_start_time = current_time
                else:
                    if correct_pose_start_time is not None:
                        total_correct_time += current_time - correct_pose_start_time
                        correct_pose_start_time = None

                all_angles = [head_angle_l, back_angle_l, leg_angle_l, head_angle_r, back_angle_r, leg_angle_r]
                ideal_angles = [180, 90, 180, 180, 90, 180]
                errors = [abs(a - b) for a, b in zip(ideal_angles, all_angles)]
                accuracies = [max(0, 100 - (e / 30) * 100) for e in errors]
                avg_accuracy = sum(accuracies) / len(accuracies)

                cv2.putText(image, f"{int(leg_angle_l)}", tuple(np.multiply(l_knee, [w, h]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(image, f"{int(leg_angle_r)}", tuple(np.multiply(r_knee, [w, h]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                indicator_color = (0, 255, 0) if "Perfect" in pose_status else (0, 0, 255)
                cv2.circle(image, center=(50, 50), radius=20, color=indicator_color, thickness=-1)

                cv2.putText(image, f"Accuracy: {avg_accuracy:.2f}%", (w - 250, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 215, 0), 2)

                elapsed_time = int(time.time() - start_time)
                correct_time_display = int(total_correct_time) if correct_pose_start_time is None else int(total_correct_time + (time.time() - correct_pose_start_time))

                cv2.putText(image, f"Total Time: {elapsed_time}s", (10, h - 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Correct Time: {correct_time_display}s", (10, h - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                cv2.putText(image, pose_status, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2),
                                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2))

            cv2.imshow("Pose Feedback", image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Total time: {int(time.time() - start_time)} seconds")
    print(f"Total time with correct pose: {int(total_correct_time) if correct_pose_start_time is None else int(total_correct_time + (time.time() - correct_pose_start_time))} seconds")

        
# ---------------------------------------------------------------------------------------------------

def handstand(cap, cooldown, last_spoken_time, previous_pose, mp_drawing, mp_pose, start_time, correct_pose_start_time, total_correct_time):
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
                l_wrist = get_point(mp_pose.PoseLandmark.LEFT_WRIST)
                l_elbow = get_point(mp_pose.PoseLandmark.LEFT_ELBOW)
                l_hip = get_point(mp_pose.PoseLandmark.LEFT_HIP)
                l_knee = get_point(mp_pose.PoseLandmark.LEFT_KNEE)
                l_ankle = get_point(mp_pose.PoseLandmark.LEFT_ANKLE)

                r_wrist = get_point(mp_pose.PoseLandmark.RIGHT_WRIST)
                r_elbow = get_point(mp_pose.PoseLandmark.RIGHT_ELBOW)
                r_shoulder = get_point(mp_pose.PoseLandmark.RIGHT_SHOULDER)
                r_hip = get_point(mp_pose.PoseLandmark.RIGHT_HIP)
                r_knee = get_point(mp_pose.PoseLandmark.RIGHT_KNEE)
                r_ankle = get_point(mp_pose.PoseLandmark.RIGHT_ANKLE)

                hand_angle_l = calculate_angle(l_wrist, l_elbow, l_shoulder)
                back_angle_l = calculate_angle(l_shoulder, l_hip, l_knee)
                leg_angle_l = calculate_angle(l_hip, l_knee, l_ankle)
                hand_angle_r = calculate_angle(r_wrist, r_elbow, r_shoulder)
                back_angle_r = calculate_angle(r_shoulder, r_hip, r_knee)
                leg_angle_r = calculate_angle(r_hip, r_knee, r_ankle)

                if not 175 < hand_angle_l < 185 and not 175 < hand_angle_r < 185:
                    pose_status = "Keep your elbows straight"
                elif not 175 < back_angle_l < 200 and not 175 < back_angle_r < 200:
                    pose_status = "Activate your core and straighten your back"
                elif not 170 < leg_angle_l < 195 and not 170 < leg_angle_r < 190:
                    pose_status = "Keep your legs straight"
                else:
                    pose_status = "Perfect form ! Keep it up!"

                current_time = time.time()
                if pose_status != previous_pose and (current_time - last_spoken_time) > cooldown:
                    threading.Thread(target=speak, args=(pose_status,), daemon=True).start()
                    print("Feedback : ", pose_status)
                    previous_pose = pose_status
                    last_spoken_time = current_time

                if "Perfect" in pose_status:
                    if correct_pose_start_time is None:
                        correct_pose_start_time = current_time
                else:
                    if correct_pose_start_time is not None:
                        total_correct_time += current_time - correct_pose_start_time
                        correct_pose_start_time = None

                all_angles = [hand_angle_l, back_angle_l, leg_angle_l, hand_angle_r, back_angle_r, leg_angle_r]
                ideal_angles = [180, 185, 180, 180, 185, 180]
                errors = [abs(a - b) for a, b in zip(ideal_angles, all_angles)]
                accuracies = [max(0, 100 - (e / 30) * 100) for e in errors]
                avg_accuracy = sum(accuracies) / len(accuracies)

                cv2.putText(image, f"{int(leg_angle_l)}", tuple(np.multiply(l_knee, [w, h]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(image, f"{int(leg_angle_r)}", tuple(np.multiply(r_knee, [w, h]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                indicator_color = (0, 255, 0) if "Perfect" in pose_status else (0, 0, 255)
                cv2.circle(image, center=(50, 50), radius=20, color=indicator_color, thickness=-1)

                cv2.putText(image, f"Accuracy: {avg_accuracy:.2f}%", (w - 250, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 215, 0), 2)

                elapsed_time = int(time.time() - start_time)
                correct_time_display = int(total_correct_time) if correct_pose_start_time is None else int(total_correct_time + (time.time() - correct_pose_start_time))

                cv2.putText(image, f"Total Time: {elapsed_time}s", (10, h - 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(image, f"Correct Time: {correct_time_display}s", (10, h - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                cv2.putText(image, pose_status, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2),
                                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2))

            cv2.imshow("Pose Feedback", image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Total time: {int(time.time() - start_time)} seconds")
    print(f"Total time with correct pose: {int(total_correct_time) if correct_pose_start_time is None else int(total_correct_time + (time.time() - correct_pose_start_time))} seconds")


# ---------------------------------------------------------------------------------------------------

def frontlever(cap, cooldown, last_spoken_time, previous_pose, mp_drawing, mp_pose):
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

                l_ear = get_point(mp.pose.PoseLandmark.LEFT_EAR)
                l_shoulder = get_point(mp_pose.PoseLandmark.LEFT_SHOULDER)
                l_wrist = get_point(mp_pose.PoseLandmark.LEFT_WRIST)
                l_elbow = get_point(mp_pose.PoseLandmark.LEFT_ELBOW)
                l_hip = get_point(mp_pose.PoseLandmark.LEFT_HIP)
                l_knee = get_point(mp_pose.PoseLandmark.LEFT_KNEE)
                l_ankle = get_point(mp_pose.PoseLandmark.LEFT_ANKLE)

                r_ear = get_point(mp.pose.PoseLandmark.RIGHT_EAR)
                r_wrist = get_point(mp_pose.PoseLandmark.RIGHT_WRIST)
                r_elbow = get_point(mp_pose.PoseLandmark.RIGHT_ELBOW)
                r_shoulder = get_point(mp_pose.PoseLandmark.RIGHT_SHOULDER)
                r_hip = get_point(mp_pose.PoseLandmark.RIGHT_HIP)
                r_knee = get_point(mp_pose.PoseLandmark.RIGHT_KNEE)
                r_ankle = get_point(mp_pose.PoseLandmark.RIGHT_ANKLE)

                hand_angle_l = calculate_angle(l_wrist, l_elbow, l_shoulder)
                shoulder_angle_l = calculate_angle(l_elbow, l_shoulder, l_hip)
                head_angle_l = calculate_angle(l_ear, l_shoulder, l_hip)
                back_angle_l = calculate_angle(l_shoulder, l_hip, l_knee)
                leg_angle_l = calculate_angle(l_hip, l_knee, l_ankle)
                hand_angle_r = calculate_angle(r_wrist, r_elbow, r_shoulder)
                head_angle_r = calculate_angle(r_ear, r_shoulder, r_hip)
                back_angle_r = calculate_angle(r_shoulder, r_hip, r_knee)
                shoulder_angle_r = calculate_angle(r_elbow, r_shoulder, r_hip)
                leg_angle_r = calculate_angle(r_hip, r_knee, r_ankle)

                if not 170 < hand_angle_l <= 180 and not 170 < hand_angle_r <= 180:
                    pose_status = "try keeping your arms straight"
                elif not 170 < back_angle_l < 195 and not 170 < back_angle_r < 190:
                    pose_status = "raise your hips"
                elif not 30 < shoulder_angle_l < 60 and not 30 < shoulder_angle_r < 60:
                    pose_status = "raise your hips up and lock your scapula"
                elif not 175 < head_angle_l < 185 and not 175 < head_angle_r < 185:
                    pose_status = "keep your head and neck straight"
                elif not 170 < leg_angle_l < 195 and not 170 < leg_angle_r < 190:
                    pose_status = "keep your legs straight"
                else:
                    pose_status = "Perfect form ! Keep it up!"

                current_time = time.time()
                if pose_status != previous_pose and (current_time - last_spoken_time) > cooldown:
                    threading.Thread(target=speak, args=(pose_status,), daemon=True).start()
                    print("Feedback : ", pose_status)
                    previous_pose = pose_status
                    last_spoken_time = current_time

                all_angles = [hand_angle_l, back_angle_l, head_angle_r, leg_angle_l, hand_angle_r, head_angle_r, back_angle_r, leg_angle_r]
                ideal_angles = [180, 90, 180, 180, 180, 180, 90, 180]
                errors = [abs(a - b) for a, b in zip(ideal_angles, all_angles)]
                accuracies = [max(0, 100 - (e / 30) * 100) for e in errors]
                avg_accuracy = sum(accuracies) / len(accuracies)

                cv2.putText(image, f"{int(leg_angle_l)}", tuple(np.multiply(l_knee, [w, h]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(image, f"{int(leg_angle_r)}", tuple(np.multiply(r_knee, [w, h]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                indicator_color = (0, 255, 0) if "Perfect" in pose_status else (0, 0, 255)
                cv2.circle(image, center=(50, 50), radius=20, color=indicator_color, thickness=-1)

                cv2.putText(image, f"Accuracy: {avg_accuracy:.2f}%", (w - 250, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 215, 0), 2)

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2),
                                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2))

            cv2.imshow("Pose Feedback", image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

while True:
    n = input("Please select a pose : ")
    n.lower()
    if n == "lsit":
        lsit(cap, cooldown, last_spoken_time, previous_pose, mp_drawing, mp_pose, start_time, correct_pose_start_time, total_correct_time)
    elif n == "handstand":
        handstand(cap, cooldown, last_spoken_time, previous_pose, mp_drawing, mp_pose, start_time, correct_pose_start_time, total_correct_time)
    elif n == "frontlever":
        frontlever(cap, cooldown, last_spoken_time, previous_pose, mp_drawing, mp_pose)
    else:
        break
# ---------------------------------------------------------------------------------------------------

cap.release()
cv2.destroyAllWindows()