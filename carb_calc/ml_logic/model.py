import torch
from transformers import AutoModelForImageClassification

def load_model():
    """
    Loads the model from the transformers package with pretrained weights
    """
    model = AutoModelForImageClassification.from_pretrained("google/vit-base-patch16-224")

    print("✅ Model loaded")

    return model

def predict(processed_image, model):
    """
    Takes processed image and model as input and returns the class with the highest log likelihood
    """
    with torch.no_grad():
        log = model(**processed_image).logits

    classification = log.argmax(-1).item()

    return classification
