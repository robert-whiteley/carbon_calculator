import base64
import cv2
import numpy as np
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from ml_logic_v2.yolo_model import load_model, prediction
from ml_logic_v2.yolo_preprocessor import load_preprocessor, preprocessing
from PIL import Image

app = Flask(__name__, static_folder="./templates/static")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)
model = load_model()
image_processor = load_preprocessor()

async def load_model():
    return await load_model()

def base64_to_image(base64_string):
    # Extract the base64 encoded binary data from the input string
    base64_data = base64_string.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


@socketio.on("connect")
def test_connect():
    print("Connected")
    emit("my response", {"data": "Connected"})


@socketio.on("image")
def receive_image(image):
    # Decode the base64-encoded image data
    image = base64_to_image(image)
    image = Image.fromarray(image)
    processed_image, target_sizes = preprocessing(image, image_processor)
    objs_boxes = prediction(processed_image, target_sizes, image_processor, image, model)


    #processed_img_data = base64.b64encode(frame_encoded).decode()
    #b64_src = "data:image/jpg;base64,"
    #processed_img_data = b64_src + processed_img_data
    package = {'bboxes': objs_boxes}
    emit('result', package)

    if len(objs_boxes) > 0:
        emit("classification", objs_boxes[0]['class'])


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080, host='0.0.0.0')
