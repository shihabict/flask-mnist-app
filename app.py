import onnxruntime as ort
from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
from PIL import Image
import io

app = Flask(__name__)
# Load ONNX model once globally
onnx_model_path = "model/mnist_cnn.onnx"
ort_session = ort.InferenceSession(onnx_model_path)

def predict_digit(image_array):

    image_array = image_array.astype(np.float32) / 255.0

    input_tensor = image_array.reshape(1, 1, 28, 28).astype(np.float32)

    input_name = ort_session.get_inputs()[0].name
    ort_inputs = {input_name: input_tensor}

    ort_outs = ort_session.run(None, ort_inputs)
    probabilities = ort_outs

    predicted_digit = int(np.argmax(probabilities))
    confidence_scores = [float(p) for p in probabilities]

    return predicted_digit, confidence_scores


@app.route('/')
def index():
    return "App running"
    # return render_template('index.html')

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

        return jsonify({
            "predicted_digit": digit,
            "confidence_scores": confidences
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

