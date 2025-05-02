# backend/pose_analysis.py
import cv2
import numpy as np
import mediapipe as mp
import threading
import time
import pyttsx3

# Mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Text-to-speech setup
engine = pyttsx3.init()
speak_lock = threading.Lock()

def speak(text):
    with speak_lock:
        engine.say(text)
        engine.runAndWait()

previous_pose = "Perfect form ! Keep it up!"
last_spoken_time = 0
cooldown = 2  # seconds between TTS triggers

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points.

    Args:
        a (list): First point [x, y].
        b (list): Second point [x, y] (vertex).
        c (list): Third point [x, y].

    Returns:
        float: The angle in degrees.
    """
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def analyze_pose(image, width, height):
    """
    Analyze the pose in the given image and return feedback and accuracy.

    Args:
        image (numpy.ndarray): The image frame in BGR format.
        width (int):  Width of the image.
        height (int): Height of the image.

    Returns:
        tuple: (feedback, accuracy)
            feedback (str):  Textual feedback on the posture.
            accuracy (float): Overall posture accuracy (0-100).
    """
    global previous_pose, last_spoken_time, cooldown # Use global variables

    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # Unnecessary conversion, but kept for consistency
    h, w = height, width

    feedback = "No pose detected"  # Default feedback
    accuracy = 0.0

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        def get_point(landmark):
            return [landmarks[landmark.value].x * w, landmarks[landmark.value].y * h]  # Scale landmarks

        # Key points
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

        # Angles
        head_angle_l = calculate_angle(l_ear, l_shoulder, l_hip)
        back_angle_l = calculate_angle(l_shoulder, l_hip, l_knee)
        leg_angle_l = calculate_angle(l_hip, l_knee, l_ankle)
        head_angle_r = calculate_angle(r_ear, r_shoulder, r_hip)
        back_angle_r = calculate_angle(r_shoulder, r_hip, r_knee)
        leg_angle_r = calculate_angle(r_hip, r_knee, r_ankle)

        # Loosened thresholds to reduce jitter.  Slightly wider ranges.
        if not 165 < head_angle_l < 195 and not 165 < head_angle_r < 195: # Allow a bit more deviation
            feedback = "Keep your head straight"
        elif not 75 < back_angle_l < 105 and not 75 < back_angle_r < 105: # Allow a bit more deviation
            feedback = "Keep your back straight"
        elif not 165 < leg_angle_l < 195 and not 165 < leg_angle_r < 195: # Allow a bit more deviation
            feedback = "Keep your legs straight"
        else:
            feedback = "Perfect form! Keep it up!"

        # Trigger speech only if pose changes + cooldown
        current_time = time.time()
        if feedback != previous_pose and (current_time - last_spoken_time) > cooldown:
            threading.Thread(target=speak, args=(feedback,), daemon=True).start()
            previous_pose = feedback
            last_spoken_time = current_time

        # Accuracy calculation
        all_angles = [head_angle_l, back_angle_l, leg_angle_l, head_angle_r, back_angle_r, leg_angle_r]
        ideal_angles = [180, 90, 180, 180, 90, 180]
        errors = [abs(a - b) for a, b in zip(ideal_angles, all_angles)]
        accuracies = [max(0, 100 - (e / 30) * 100) for e in errors] # Reduced divisor from 20 to 30
        accuracy = sum(accuracies) / len(accuracies)

    pose.close()
    return feedback, accuracy
