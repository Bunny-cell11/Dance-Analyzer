# app.py

import os
from flask import Flask, jsonify

# This line was missing. It imports the blueprint object.
from analysis_blueprint import analysis_bp

def create_app():
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    
    # Configuration
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Register the analysis blueprint
    app.register_blueprint(analysis_bp)

    # Add the health check route to the main app
    @app.route('/')
    def health_check():
        """Health check endpoint for deployment platforms."""
        return jsonify({"status": "ok", "message": "Server is running."}), 200

    return app

# Create the app instance for Gunicorn to use
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
