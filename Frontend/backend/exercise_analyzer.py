import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def calculate_angle(a, b, c):
    """Calculate the angle between three points."""
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle

def analyze_pushup(frame):
    """Analyze push-up form using MediaPipe."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)
    feedback = []
    angles = {}
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        
        left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        back_angle = calculate_angle(left_shoulder, left_hip, right_hip)
        
        angles = {
            'left_arm': left_arm_angle,
            'right_arm': right_arm_angle,
            'back': back_angle
        }
        
        if back_angle < 170:
            feedback.append(f"Keep your back straight (Current angle: {back_angle:.1f}°)")
        if left_arm_angle > 160 or right_arm_angle > 160:
            feedback.append(f"Lower your body more (Current angle: {min(left_arm_angle, right_arm_angle):.1f}°)")
        if left_arm_angle < 90 or right_arm_angle < 90:
            feedback.append(f"Push up more (Current angle: {max(left_arm_angle, right_arm_angle):.1f}°)")
            
    return feedback, angles

def analyze_pullup(frame):
    """Analyze pull-up form using MediaPipe."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)
    feedback = []
    angles = {}
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        
        left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        
        angles = {
            'left_arm': left_arm_angle,
            'right_arm': right_arm_angle
        }
        
        if left_arm_angle > 160 or right_arm_angle > 160:
            feedback.append(f"Pull up more (Current angle: {min(left_arm_angle, right_arm_angle):.1f}°)")
        if left_arm_angle < 90 or right_arm_angle < 90:
            feedback.append(f"Lower your body more (Current angle: {max(left_arm_angle, right_arm_angle):.1f}°)")
            
    return feedback, angles

def analyze_squat(frame):
    """Analyze squat form using MediaPipe."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)
    feedback = []
    angles = {}
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
        
        left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
        
        angles = {
            'left_knee': left_knee_angle,
            'right_knee': right_knee_angle
        }
        
        if left_knee_angle > 160 or right_knee_angle > 160:
            feedback.append(f"Squat lower (Current angle: {min(left_knee_angle, right_knee_angle):.1f}°)")
        if left_knee_angle < 90 or right_knee_angle < 90:
            feedback.append(f"Don't squat too low (Current angle: {max(left_knee_angle, right_knee_angle):.1f}°)")
            
    return feedback, angles

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        frame_data = data['frame']
        exercise_type = data.get('exerciseType', 'pushup')
        
        frame_bytes = base64.b64decode(frame_data)
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
        
        if exercise_type == 'pushup':
            feedback, angles = analyze_pushup(frame)
        elif exercise_type == 'pullup':
            feedback, angles = analyze_pullup(frame)
        elif exercise_type == 'squat':
            feedback, angles = analyze_squat(frame)
        else:
            feedback = []
            angles = {}
        
        return jsonify({
            'success': True,
            'feedback': feedback,
            'angles': angles
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 