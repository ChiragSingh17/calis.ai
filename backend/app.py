import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import threading
import time
from flask import Flask, render_template, Response, jsonify
from flask_cors import CORS
import base64

# Flask setup
app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

# Mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Text-to-speech setup
engine = pyttsx3.init()
speak_lock = threading.Lock()

def speak(text):
    with speak_lock:
        try:
            engine.say(text)
            engine.runAndWait()
        except RuntimeError as e:
            print(f"Error in speak function: {e}")

previous_pose = "Perfect form ! Keep it up!"
last_spoken_time = 0
cooldown = 2  # seconds between TTS triggers
camera_active = False #global variable to control camera state
all_angles = []

def gen_frames():
    global previous_pose, last_spoken_time, camera_active, all_angles
    # Start webcam
    cap = cv2.VideoCapture(0)
    camera_active = True #set to true when camera starts
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while camera_active: #changed from cap.isOpened() to camera_active
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
                all_angles = [head_angle_l, back_angle_l, leg_angle_l, head_angle_r, back_angle_r, leg_angle_r]

                # Loosened thresholds to reduce jitter
                if not 170 < head_angle_l < 190 and not 170 < head_angle_r < 190:
                    pose_status = "keep your head straight"
                elif not 80 < back_angle_l < 100 and not 80 < back_angle_r < 100:
                    pose_status = "keep your back straight"
                elif not 170 < leg_angle_l < 195 and not 170 < leg_angle_r < 190:
                    pose_status = "keep your legs straight"
                else:
                    pose_status = "Perfect form ! Keep it up!"

                # Trigger speech only if pose changes + cooldown
                current_time = time.time()
                if pose_status != previous_pose and (current_time - last_spoken_time) > cooldown:
                    threading.Thread(target=speak, args=(pose_status,), daemon=True).start()
                    previous_pose = pose_status
                    last_spoken_time = current_time
                elif (current_time - last_spoken_time) > cooldown: # add this condition
                    threading.Thread(target=speak, args=(pose_status,), daemon=True).start() # speak again
                    last_spoken_time = current_time # update last_spoken_time

                # Accuracy
                ideal_angles = [180, 90, 180, 180, 90, 180]
                errors = [abs(a - b) for a, b in zip(ideal_angles, all_angles)]
                accuracies = [max(0, 100 - (e / 30) * 100) for e in errors]
                avg_accuracy = sum(accuracies) / len(accuracies)

                # Draw angle values
                cv2.putText(image, f"{int(leg_angle_l)}", tuple(np.multiply(l_knee, [w, h]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(image, f"{int(leg_angle_r)}", tuple(np.multiply(r_knee, [w, h]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # Status indicator circle
                indicator_color = (0, 255, 0) if "Perfect" in pose_status else (0, 0, 255)
                cv2.circle(image, center=(50, 50), radius=20, color=indicator_color, thickness=-1)

                # Accuracy display
                cv2.putText(image, f"Accuracy: {avg_accuracy:.2f}%", (w - 250, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 215, 0), 2)

                # Draw skeleton
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2),
                                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2))
            
            # Encode the image in base64 format
            _, buffer = cv2.imencode('.jpg', image)
            frame_data = base64.b64encode(buffer).decode('utf-8')
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            # yield frame_data #returning base64 encoded string
        cap.release()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera_active
    camera_active = False
    return jsonify({'message': 'Camera stopped'})

@app.route('/get_feedback')
def get_feedback():
    global previous_pose, all_angles
    # Return the feedback and accuracy as JSON
    ideal_angles = [180, 90, 180, 180, 90, 180]
    if all_angles:
        errors = [abs(a - b) for a, b in zip(ideal_angles, all_angles)]
        accuracies = [max(0, 100 - (e / 30) * 100) for e in errors]
        avg_accuracy = sum(accuracies) / len(accuracies)
    else:
        avg_accuracy = 0

    return jsonify({'feedback': previous_pose, 'accuracy': avg_accuracy})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
