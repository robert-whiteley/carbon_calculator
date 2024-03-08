from transformers import YolosImageProcessor
import torch

def load_preprocessor():
    """
    Loads the image preprocessor from the transformers package.
    """
    image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

    print("✅ Preprocessor loaded")

    return image_processor

def preprocessing(image, image_preprocessor):
    """
    Takes an image and returns the preprocessed image to be input to the model.
    """

    inputs = image_preprocessor(images=image, return_tensors="pt")
    target_sizes = torch.tensor([image.size[::-1]])

    return inputs, target_sizes
