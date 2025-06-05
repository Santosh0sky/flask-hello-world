from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Configure upload settings
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/')
def home():
    return 'Hellooe, World!'

@app.route('/about')
def about():
    return 'About'

@app.route("/api/health", methods=["GET"])
def health_check():
    print("Health check endpoint called.")
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route("/api/upload-pdf", methods=["POST"])
def upload_pdf():
    print("Uploading PDF...")
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected"}), 400
    if file:
        # Validate file type
        if file.content_type != "application/pdf":
            return jsonify({"success": False, "message": "Only PDF files are allowed"}), 400
        # Read file content to check size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        if file_size > MAX_FILE_SIZE:
            return jsonify({"success": False, "message": f"File size exceeds maximum limit of {MAX_FILE_SIZE/1024/1024}MB"}), 413
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        # Save the file
        file.save(file_path)
        return jsonify({
            "success": True,
            "message": "File uploaded successfully",
            "data": {
                "filename": filename,
                "originalName": file.filename,
                "size": file_size,
                "contentType": file.content_type,
                "path": file_path
            }
        }), 200
    return jsonify({"success": False, "message": "Unknown error"}), 500

if __name__ == '__main__':
    app.run(debug=True)