import onnxruntime as ort
from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
from PIL import Image
import io

from prediction.predict import predict_digit

app = Flask(__name__)


@app.route('/')
def index():
    # return "App running"
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read image in PIL format
        image = Image.open(file).convert('L')
        image = image.resize((28, 28))

        # Convert to NumPy array
        image_np = np.array(image)

        # Call ONNX prediction function
        digit, confidences = predict_digit(image_np)

        print(f"Predicted Class: {digit}\nConfidence Scores: {confidences}")

        return jsonify({
            "predicted_digit": digit,
            "confidence_scores": confidences
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

