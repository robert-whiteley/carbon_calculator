
from colorama import Fore, Style
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import carb_calc.interface.google_vision as GoogleVision
import uvicorn

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/predict")
def predict():
    """
    This is the endpoint for the predictions

    Args: to be defined
    """
    pass

@app.get("/detect-objects")
def detect_objects():
    google_response = GoogleVision.localize_objects_uri('https://www.everydayfamilycooking.com/wp-content/uploads/2020/03/strawberries-and-applesauce.jpg')
    print(f"Number of objects found: {len(google_response)}")
    number_of_objects = len(google_response)
    objects = []
    for object_ in google_response:
        obj = {
            'name': object_.name,
            'confidence': object_.score,
        }

        print(f"\n{object_.name} (confidence: {object_.score})")
        print("Normalized bounding polygon vertices: ")
        for vertex in object_.bounding_poly.normalized_vertices:
            print(f" - ({vertex.x}, {vertex.y})")
    return 'done'

@app.get("/")
def root():
    '''
    This works as an API status checker
    '''
    response = {
        'res': 'Carbon Calculator - The first step for a better world!',
        'authors': 'Robert, Joe, Daniel, Braveen, Mathieu'
    }
    return response


if __name__ == '__main__':
    print(Fore.GREEN + "--Carbon-Footprint-API-Started--" + Style.RESET_ALL)
    uvicorn.run("fast:app", host='127.0.0.1', port=8000, log_level="info", reload=True)
