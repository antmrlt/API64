from flask import Flask, request, jsonify, send_from_directory
import base64
import os
import time
import uuid

app = Flask(__name__)

# Fetch the API key from the environment variable
API_KEY = os.getenv('API_KEY')

# Check if the API_KEY is not set
if not API_KEY:
    raise ValueError("API_KEY environment variable is required but not set.")

# Fetch Domain from the environment variable
APP_DOMAIN = os.getenv('APP_DOMAIN', 'localhost')
print(f"APP_DOMAIN is set to: {APP_DOMAIN}")

# Fetch Flask environment (e.g., 'production', 'development')
FLASK_ENV = os.getenv('FLASK_ENV', 'production')  # Default to 'production' if not set

# Set the environment for Flask (Optional, useful for debugging)
app.config['ENV'] = FLASK_ENV

# Directory where the files will be saved and served
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
print(f"UPLOAD_FOLDER is set to: {UPLOAD_FOLDER}")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Content-Type to File Extension mapping dictionary
CONTENT_TYPE_MAPPING = {
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/vnd.ms-excel": "xls",
    "application/vnd.ms-excel.sheet.macroEnabled.12": "xlsm",
    "application/vnd.ms-excel.template.macroEnabled.12": "xltm",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.template": "xltx",
    "application/vnd.ms-excel.addin.macroEnabled.12": "xlam",
    "application/vnd.ms-excel.sheet.binary.macroEnabled.12": "xlsb",
    "application/vnd.ms-excel.sheet": "xls",
    "application/vnd.oasis.opendocument.spreadsheet": "ods",
    "application/pdf": "pdf",
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    "image/tiff": "tiff",
    "image/bmp": "bmp",
    "text/plain": "txt",
    "text/html": "html",
    "text/css": "css",
    "text/javascript": "js",
    "application/json": "json",
    "application/xml": "xml",
    "application/zip": "zip",
    "application/x-tar": "tar",
    "application/x-gzip": "gz",
    "audio/mpeg": "mp3",
    "audio/wav": "wav",
    "audio/ogg": "ogg",
    "video/mp4": "mp4",
    "video/x-msvideo": "avi",
    "video/x-matroska": "mkv",
    "application/vnd.ms-powerpoint": "ppt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
    "application/vnd.ms-word": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx"
}

# Function to get file extension based on content type
def get_file_extension(content_type):
    return CONTENT_TYPE_MAPPING.get(content_type, content_type.split('/')[-1])

# Function to decode and save the Base64 string to a file
def save_base64_to_file(base64_string, file_name):
    try:
        # Decode the Base64 string
        decoded_data = base64.b64decode(base64_string)
        
        # Save the decoded data to a file in the UPLOAD_FOLDER
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(file_path, 'wb') as file:
            file.write(decoded_data)

        # Set file permissions to read-only (444)
        os.chmod(file_path, 0o444)  # Read-only for everyone
        
        return True, file_path
    except Exception as e:
        return False, str(e)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get API key and check if it's valid
    api_key = request.headers.get('API-Key')
    if api_key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 403
    
    # Get the payload (Base64 string and Content-Type)
    data = request.json
    if 'base64_string' not in data or 'content_type' not in data:
        return jsonify({"error": "Base64 string and Content-Type are required in payload"}), 400
    
    base64_string = data['base64_string']
    content_type = data['content_type']
    
    # Determine the correct file extension based on the content_type using the dictionary
    file_extension = get_file_extension(content_type)

    # Generate a unique file name based on timestamp and UUID
    file_name = f"file_{int(time.time())}_{uuid.uuid4().hex}.{file_extension}"

    # Decode and save the Base64 string to a file
    success, file_path = save_base64_to_file(base64_string, file_name)

    if success:
        # Generate the URL for accessing the file
        file_url = f"http://{APP_DOMAIN}:5000/uploads/{file_name}"
        return jsonify({"message": f"File saved as {file_name}", "file_url": file_url}), 200
    else:
        return jsonify({"error": file_path}), 500

# Serve files from the UPLOAD_FOLDER
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    # Run Flask with debug=False in production
    app.run(debug=False, host='0.0.0.0', port=5000)
