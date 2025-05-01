# Calisthenics.py
import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose_data = {'pose_status': 'Initializing...', 'accuracy': 0}
current_frame = None  # Updated live from camera stream

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def analyze_pose():
    global current_frame, pose_data
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            if current_frame is None:
                continue

            frame = current_frame.copy()
            h, w, _ = frame.shape
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                def get_point(landmark):
                    return [landmarks[landmark.value].x * w, landmarks[landmark.value].y * h]

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
                    pose_status = "keep your head straight"
                elif not 80 < back_angle_l < 100 and not 80 < back_angle_r < 100:
                    pose_status = "keep your back straight"
                elif not 170 < leg_angle_l < 195 and not 170 < leg_angle_r < 190:
                    pose_status = "keep your legs straight"
                else:
                    pose_status = "Perfect form! Keep it up!"

                all_angles = [head_angle_l, back_angle_l, leg_angle_l,
                              head_angle_r, back_angle_r, leg_angle_r]
                ideal_angles = [180, 90, 180, 180, 90, 180]
                errors = [abs(a - b) for a, b in zip(ideal_angles, all_angles)]
                accuracies = [max(0, 100 - (e / 30) * 100) for e in errors]
                avg_accuracy = sum(accuracies) / len(accuracies)

                pose_data.update({
                    'pose_status': pose_status,
                    'accuracy': avg_accuracy
                })

                print("Analyzing frame...")
                print(f"Pose status: {pose_status} | Accuracy: {avg_accuracy:.2f}%")
