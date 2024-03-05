
from colorama import Fore, Style
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from carb_calc.ml_logic.model import load_model, predict
from carb_calc.ml_logic.preprocessor import preprocessing
import carb_calc.interface.google_vision as GoogleVision
import uvicorn
import uuid

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
    prediction = predict(processed_image,app.state.model)
    return prediction

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
async def upload(file: UploadFile = File(...)):
    """
     Endpoint to upload an image file and detect objects using Google Cloud Vision API.

    Args:
        file (UploadFile): The uploaded image file.

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
    # Get a unique file name from the uploaded file
    file.filename = f'{uuid.uuid4()}.jpg'

    # Read the contents of the uploaded file
    contents = await file.read()

    return GoogleVision.localize_objects_base64(contents)

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
