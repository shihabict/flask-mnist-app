from PIL import Image
import onnxruntime as ort
import numpy as np

onnx_model_path = "../model/mnist_cnn.onnx"
ort_session = ort.InferenceSession(onnx_model_path)

def predict_digit(image_array):

    image_array = image_array.astype(np.float32) / 255.0

    input_tensor = image_array.reshape(1, 1, 28, 28).astype(np.float32)

    input_name = ort_session.get_inputs()[0].name
    ort_inputs = {input_name: input_tensor}

    ort_outs = ort_session.run(None, ort_inputs)
    probabilities = ort_outs[0][0].astype(np.float32).flatten()
    confidence_scores = probabilities.tolist()

    predicted_digit = int(np.argmax(probabilities))
    # confidence_scores = [float(p) for p in probabilities]

    return predicted_digit, confidence_scores

if __name__ == '__main__':
    image_path = "../data/Example-of-a-MNIST-input-An-image-is-passed-to-the-network-as-a-matrix-of-28-by-28.png"
    # Read image in PIL format
    image = Image.open(image_path).convert('L')
    image = image.resize((28, 28))

    # Convert to NumPy array
    image_np = np.array(image)

    # Call ONNX prediction function
    digit, confidences = predict_digit(image_np)
    print(digit, confidences)