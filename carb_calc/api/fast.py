
from colorama import Fore, Style
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from carb_calc.ml_logic.model import load_model, prediction
from carb_calc.ml_logic.preprocessor import preprocessing
from carb_calc.ml_logic.image_cropper import image_cropper
from carb_calc.ml_logic.co2_val import co2_query
import carb_calc.interface.google_vision as GoogleVision
import json
import uvicorn
import numpy as np

app = FastAPI()
app.state.model = load_model()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    """
    This is the endpoint for the predictions
    Args: to be defined
    """
    image = await image.read()
    object_localisation = GoogleVision.localize_objects_base64(image)
    cropped_image, bin_cropped_image = image_cropper(image, object_localisation)
    processed_image = preprocessing(cropped_image)
    classification = prediction(processed_image,app.state.model)
    output = co2_query(classification)
    cropped_image_json = json.dumps(np.array(cropped_image).tolist())

    return JSONResponse(status_code=200, content={"message": output, "image_cropped":cropped_image_json})



@app.get("/detect-objects")
def detect_objects(url:str = 'https://www.everydayfamilycooking.com/wp-content/uploads/2020/03/strawberries-and-applesauce.jpg'):
    """
    Endpoint to detect objects in an image.

    Returns:
        dict: A dictionary containing information about detected objects in the image.
              The dictionary has the following structure:
              {
                  'objects': [
                      {
                          'name': str,  # Name of the detected object
                          'confidence': float,  # Confidence score of the detection
                          'vertices': [  # List of vertices forming a bounding box around the object
                              {
                                  'x': float,  # X-coordinate of the vertex
                                  'y': float   # Y-coordinate of the vertex
                              },
                              ...
                          ]
                      },
                      ...
                  ]
              }
    """
    return GoogleVision.localize_objects_uri(url)

@app.post("/upload")
async def upload(image: UploadFile = File(...)):
    """
    Endpoint to upload an image and detect objects in it.

    Args:
        image (UploadFile): The image file to be uploaded for object detection.

    Returns:
        JSONResponse: A JSON response containing information about detected objects in the uploaded image.
                      The response has the following structure:
                      {
                          'message': dict  # A dictionary containing information about detected objects in the image.
                      }
    """
    contents = await image.read()
    return JSONResponse(status_code=200, content={"message": GoogleVision.localize_objects_base64(contents)})

@app.get("/")
def root():
    '''
    This works as an API status checker
    Returns:
        dict: {
            'res': 'Carbon Calculator - The first step for a better world!',
            'authors': 'Robert, Joe, Daniel, Braveen, Mathieu'
        }

    '''
    response = {
        'res': 'Carbon Calculator - The first step for a better world!',
        'authors': 'Robert, Joe, Daniel, Braveen, Mathieu'
    }
    return response

if __name__ == '__main__':
    print(Fore.GREEN + "--Carbon-Footprint-API-Started--" + Style.RESET_ALL)
    uvicorn.run("fast:app", host='127.0.0.1', port=8000, log_level="info", reload=True)
