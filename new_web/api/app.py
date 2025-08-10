from flask import Flask, request, jsonify, render_template
from rembg import remove
import cv2
import numpy as np
import os
import base64

print("==== Flask app is being loaded ====")

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files or request.files['image'].filename == '':
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    file_bytes = np.frombuffer(file.read(), np.uint8)
    
    # Decode image into OpenCV format
    input_image = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
    
    try:
        # Encode back to bytes for rembg
        _, buffer = cv2.imencode('.png', input_image)
        output_bytes = remove(buffer.tobytes())

        # Convert output to base64 string
        base64_img = base64.b64encode(output_bytes).decode('utf-8')

        return jsonify({'image': base64_img})
    except Exception as e:
        print("Error during image processing:", e)
        return jsonify({'error': str(e)}), 500

