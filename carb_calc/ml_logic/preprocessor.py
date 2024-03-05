from PIL import Image
from transformers import AutoImageProcessor

#Test_images file path
filepath = '../test_images'

#Takes the cropped image from google vision API
def preprocessing(crop_image):
    """
    Takes image (jpeg, webp) as an input and processes it using google's image processor
    """
    image = Image.open(crop_image)
    processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224")
    processor(image, return_tensors='pt')
    processed_image = processor(image, return_tensors='pt')

    print("✅ Processed image")

    return processed_image
