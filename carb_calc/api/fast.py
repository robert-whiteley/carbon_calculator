
from colorama import Fore, Style
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from carb_calc.ml_logic.model import load_model, prediction
from carb_calc.ml_logic.preprocessor import preprocessing
import carb_calc.interface.google_vision as GoogleVision
from PIL import Image
import base64
import io
import uvicorn
import uuid
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

@app.get("/predict")
def predict(crop_image):
    """
    This is the endpoint for the predictions
    Args: to be defined
    """
    processed_image = preprocessing(crop_image)
    output = prediction(processed_image,app.state.model)
    return output

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
