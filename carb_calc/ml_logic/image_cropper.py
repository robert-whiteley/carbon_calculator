import numpy as np
from PIL import Image
import io

# get image from backend api

def image_cropper(image, object_localisation):

    img = Image.open(io.BytesIO(image))

    # get the dimensions
    img_array = np.asarray(img)
    x_shape = img_array.shape[1]
    y_shape = img_array.shape[0]

    # get the bounding box
    bbox = object_localisation['objects'][0]['vertices']

    # get the bounding box array elements
    for coord in bbox:
        coord['x'] = int(round(coord['x'] * x_shape, 0))
        coord['y'] = int(round(coord['y'] * y_shape, 0))

    # slice out the object image
    obj_array = img_array[bbox[0]['y']:bbox[2]['y'], bbox[0]['x']:bbox[1]['x']]
    pil_img = Image.fromarray(obj_array)
    binary_img = converter_pil_binary(pil_img)

    return pil_img, binary_img

def converter_pil_binary(image: Image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    converted_image = img_byte_arr.getvalue()

    return converted_image


if __name__ == '__main__':
    pass
