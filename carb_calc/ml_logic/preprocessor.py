from PIL import Image
from transformers import AutoImageProcessor

#Test_images file path
filepath = '../test_images'

#Takes the cropped image from google vision API
def preprocessing(image):
    """
    Takes image (jpeg, webp) as an input and processes it using google's image processor
    """
    processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224")
    processed_image = processor(image, return_tensors='tf')

    print("✅ Processed image")

    return processed_image
