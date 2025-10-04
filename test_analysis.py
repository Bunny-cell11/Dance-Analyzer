import pytest
import os
from poses import calculate_angle
from analysis import analyze_video

# Get the absolute path to the directory containing this test file
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

def test_calculate_ninety_degree_angle():
    """Tests if the angle calculation is correct for a 90-degree angle."""
    a = [0, 1]
    b = [0, 0]
    c = [1, 0]
    angle = calculate_angle(a, b, c)
    assert 89.9 < angle < 90.1

def test_analyze_video_output_format():
    """Tests if the main analysis function returns a dictionary."""
    # Create a robust path to the test video
    video_path = os.path.join(TESTS_DIR, 'test_video.mp4')
    
    # Ensure the test video actually exists before running the test
    assert os.path.exists(video_path), f"Test video not found at {video_path}"

    result = analyze_video(video_path)
    assert isinstance(result, dict)
