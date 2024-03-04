
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
def root():
    '''
    This works as an API status checker
    '''
    response = {
        'greeting': 'Carbon Calc Team is the best!'
    }
    return response
