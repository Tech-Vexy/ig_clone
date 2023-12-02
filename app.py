# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import initialize_app, storage

app = Flask(__name__)
CORS(app)

# Initialize Firebase
cred = None  # Add your Firebase Admin SDK credentials
initialize_app(cred, {'storageBucket': 'your-firebase-storage-bucket'})

# Endpoint to upload an image
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    image_path = f'images/{image.filename}'

    # Upload image to Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(image_path)
    blob.upload_from_file(image)

    # Get the public URL of the uploaded image
    image_url = blob.public_url

    return jsonify({'image_url': image_url}), 200

if __name__ == '__main__':
    app.run(debug=True)
