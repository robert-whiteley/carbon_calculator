import base64
import cv2
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from carb_calc.ml_logic_v2.yolo_model import load_model, prediction
from carb_calc.ml_logic_v2.yolo_preprocessor import load_preprocessor, preprocessing
from PIL import Image

# Initialize Flask app and SocketIO
app = Flask(__name__, static_folder="./templates/static")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins='*')

# Load YOLO model and preprocessor
model = load_model()
image_processor = load_preprocessor()

def base64_to_image(base64_string):
    """
    Convert a base64-encoded string to an image.

    Args:
        base64_string (str): Base64-encoded image string.

    Returns:
        numpy.ndarray: Decoded image as a NumPy array.
    """
    base64_data = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

@socketio.on("connect")
def test_connect():
    """Handle client connection."""
    print("Connected")
    emit("my response", {"data": "Connected"})

@socketio.on("image")
def receive_image(image):
    """
    Receive base64-encoded image from the client, process it using YOLO model,
    and emit the result back to the client.

    Args:
        image (str): Base64-encoded image string.
    """
    image = base64_to_image(image)
    image = Image.fromarray(image)
    processed_image, target_sizes = preprocessing(image, image_processor)
    objs_boxes = prediction(processed_image, target_sizes, image_processor, image, model)
    package = {'bboxes': objs_boxes}
    emit('result', package)

@app.route("/v3")
def v3():
    """Render HTML page for version 3."""
    return render_template("edge.html")

@app.route("/")
def index():
    """Render HTML page for the index."""
    return render_template("index.html")

if __name__ == "__main__":
    # Run the Flask app with SocketIO support
    socketio.run(app, debug=True, host='0.0.0.0')
