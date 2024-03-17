# Carbon Calculator (Static Images and Video Streaming)

## Introduction
The Carbon Calculator application was developed as part of the capstone project during the LeWagon Bootcamp. Its primary objective is to calculate the carbon footprint of fruits and vegetables, both from static images and live video streams.
[Check the project presentation here.](https://docs.google.com/presentation/d/1QucjrJPvjX4da7awNxiwpVnmO40UiFY_LMHjuQteBaE/edit#slide=id.g2c25e50f944_0_382)


## Technologies Used

- **Python** <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" height="36">

- **Tensorflow** <img src="https://upload.wikimedia.org/wikipedia/commons/2/2d/Tensorflow_logo.svg" height="36">

- **PyTorch** <img src="https://upload.wikimedia.org/wikipedia/commons/9/96/Pytorch_logo.png" height="36">

- **FastAPI** <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" height="36">

- **Flask** <img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg" height="36">

- **SocketIO** <img src="https://upload.wikimedia.org/wikipedia/commons/9/96/Socket-io.svg" height="36">

- **TensorflowJS** <img src="https://upload.wikimedia.org/wikipedia/commons/1/11/TensorFlowLogo.svg" height="36">

- **Docker** <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Docker_%28container_engine%29_logo.svg" height="36">

- **BigQuery** <img src="https://cloud.google.com/images/social-icon-google-cloud-1200-630.png" height="36">

- **Google Cloud Vision** <img src="https://cloud.google.com/images/social-icon-google-cloud-1200-630.png" height="36">

## Versions

There are three distinct versions of the application, each addressing different challenges and incorporating various technologies.

### V1 (Branch: Mk1)
V1 represents the initial version of the application and is located on a separate branch. This version focuses on experimenting with different approaches and technologies, laying the groundwork for subsequent iterations.

V1 is based on the [Vision Transformer model](https://huggingface.co/google/vit-base-patch16-224) from Google, fine-tuned through transfer learning. Transfer learning involves taking a pre-trained model and fine-tuning it on a specific task, in this case, recognizing more than 100+ fruits and vegetables. It aims to achieve object recognition using advanced machine learning techniques, specifically leveraging the Vision Transformer architecture.

### V2 and V3 (Master Branch)
V2 and V3 represent advancements in the project architecture and functionality.

- **V2**: Utilizes the YOLOv8 Tiny model for object detection. Object detection is a computer vision task that involves identifying and locating objects within an image. YOLO (You Only Look Once) is a popular object detection algorithm known for its speed and accuracy. In this version, inference is performed server-side, meaning the object detection process occurs on the server hosting the application.

- **V3**: Employs the COCO SSD (Common Objects in Context - Single Shot Multibox Detector) model for object detection. Similar to V2, object detection is a primary focus of this version. However, V3 adopts the ML@Edge architectural pattern. ML@Edge, or Machine Learning at the Edge, involves deploying machine learning models directly onto edge devices, such as browsers or IoT devices, to perform inference locally. In this case, TensorflowJS is loaded on the browser, enabling client-side inference and reducing latency by executing machine learning models directly on the user's device.
