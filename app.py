import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from analysis import analyze_video

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/analyze', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({"error": "No video file part"}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)

        # --- Perform analysis ---
        try:
            analysis_result = analyze_video(video_path)
            # --- Clean up the uploaded file ---
            os.remove(video_path)
            return jsonify(analysis_result), 200
        except Exception as e:
            # Clean up in case of error
            if os.path.exists(video_path):
                os.remove(video_path)
            return jsonify({"error": f"An error occurred during analysis: {str(e)}"}), 500

    return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
