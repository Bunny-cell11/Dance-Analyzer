import cv2
import mediapipe as mp
import numpy as np
from poses import STANDARD_POSES, calculate_angle, get_landmark

# Initialize MediaPipe components
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def analyze_video(video_path: str) -> dict:
    """
    Analyzes a video file to detect dance poses in each frame.

    Args:
        video_path: The path to the video file.

    Returns:
        A dictionary containing detected poses for each frame.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return {}

    detected_poses_summary = {}
    frame_number = 0

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, frame = cap.read() # Note: changed variable name to 'frame' for clarity
            if not success:
                break

            # --- MEMORY OPTIMIZATION ---
            # Resize the frame to a smaller width to reduce memory usage.
            # We maintain the aspect ratio to avoid distortion.
            frame = cv2.resize(frame, (640, int(frame.shape[0] * (640 / frame.shape[1]))))
            # --- END OF OPTIMIZATION ---

            # Convert the BGR image to RGB for MediaPipe
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # --- Pose Matching Logic ---
                # Check for T-Pose
                if "T-Pose" in STANDARD_POSES:
                    # Right arm angles
                    shoulder_r = get_landmark(landmarks, "RIGHT_SHOULDER")
                    elbow_r = get_landmark(landmarks, "RIGHT_ELBOW")
                    wrist_r = get_landmark(landmarks, "RIGHT_WRIST")
                    hip_r = get_landmark(landmarks, "RIGHT_HIP")
                    
                    # Left arm angles
                    shoulder_l = get_landmark(landmarks, "LEFT_SHOULDER")
                    elbow_l = get_landmark(landmarks, "LEFT_ELBOW")
                    wrist_l = get_landmark(landmarks, "LEFT_WRIST")
                    hip_l = get_landmark(landmarks, "LEFT_HIP")

                    # Calculate angles
                    elbow_angle_r = calculate_angle(shoulder_r, elbow_r, wrist_r)
                    shoulder_angle_r = calculate_angle(hip_r, shoulder_r, elbow_r)
                    elbow_angle_l = calculate_angle(shoulder_l, elbow_l, wrist_l)
                    shoulder_angle_l = calculate_angle(hip_l, shoulder_l, elbow_l)

                    # Get T-Pose angle requirements
                    t_pose_angles = STANDARD_POSES["T-Pose"]
                    
                    # Check if angles are within tolerance for T-Pose
                    # Note: This logic assumes 'elbow_angle_min', etc. are defined in your poses.py
                    # A more robust check should be implemented if poses.py changes.
                    if (t_pose_angles.get("elbow_angle_min", 0) <= elbow_angle_r <= t_pose_angles.get("elbow_angle_max", 360) and
                        t_pose_angles.get("shoulder_angle_min", 0) <= shoulder_angle_r <= t_pose_angles.get("shoulder_angle_max", 360) and
                        t_pose_angles.get("elbow_angle_min", 0) <= elbow_angle_l <= t_pose_angles.get("elbow_angle_max", 360) and
                        t_pose_angles.get("shoulder_angle_min", 0) <= shoulder_angle_l <= t_pose_angles.get("shoulder_angle_max", 360)):
                        
                        detected_poses_summary[f"frame_{frame_number}"] = "T-Pose"

                # Add more pose checks here...

            except AttributeError:
                # No landmarks detected in this frame
                pass
            
            frame_number += 1

    cap.release()
    return detected_poses_summary
