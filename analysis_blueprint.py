# analysis_blueprint.py

import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from analysis import analyze_video

# Create a Blueprint object
analysis_bp = Blueprint('analysis_bp', __name__)

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

def allowed_file(filename: str) -> bool:
    """Checks if the file extension is allowed."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@analysis_bp.route('/analyze', methods=['POST'])
def upload_and_analyze():
    """Endpoint to upload a video and get pose analysis results."""
    if 'video' not in request.files:
        return jsonify({"error": "No video file part in the request"}), 400

    file = request.files['video']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        video_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        try:
            file.save(video_path)
            analysis_result = analyze_video(video_path)
            return jsonify(analysis_result), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred during analysis: {str(e)}"}), 500
        finally:
            if os.path.exists(video_path):
                os.remove(video_path)
    else:
        return jsonify({"error": "File type not allowed"}), 400
