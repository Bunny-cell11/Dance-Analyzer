import numpy as np
import mediapipe as mp

# Mapping landmark names to their index in MediaPipe's PoseLandmark enum
LANDMARK_MAP = {name: i for i, name in enumerate(mp.solutions.pose.PoseLandmark._member_names_)}

def get_landmark(landmarks, name: str):
    """Retrieves landmark coordinates by name."""
    index = LANDMARK_MAP[name]
    return [landmarks[index].x, landmarks[index].y]

def calculate_angle(a, b, c):
    """Calculates the angle between three points (angle at point b)."""
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

# --- Define Your Standard Poses Here ---
# A pose is defined by the angles of key joints.
# You can add more poses like "Warrior II", "Tree Pose", etc.
STANDARD_POSES = {
    "T-Pose": {
        "description": "Arms extended horizontally to the sides.",
        "tolerance": 35, # degrees
        "elbow_angle_min": 160,
        "elbow_angle_max": 200, # A straight arm is 180, allow tolerance
        "shoulder_angle_min": 75,
        "shoulder_angle_max": 105  # A 90-degree angle with the torso
    }
    # Example for another pose:
    # "Right-Arm-Raised": {
    #     "description": "Right arm raised straight up.",
    #     "tolerance": 20,
    #     "shoulder_angle_r_min": 160,
    #     "shoulder_angle_r_max": 200,
    #     "elbow_angle_r_min": 160,
    #     "elbow_angle_r_max": 200
    # }
}
