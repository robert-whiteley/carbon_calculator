from google.cloud import vision


def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations

    return objects

def localize_objects_uri(uri):
    """Localize objects in the image on internet

    Args:
    uri: The path to the file in the internet
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri
    response = convert_response(client.object_localization(image=image).localized_object_annotations)

    return response

def localize_objects_base64(content):
    """Localize objects in the image

    Args:
    content: The image in base64
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = convert_response(client.object_localization(image=image).localized_object_annotations)
    return response

def convert_response(objects):
    """
    Convert response from Google Cloud Vision API into a structured format.

    Args:
        objects (List): List of objects detected by Google Cloud Vision API.

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
    list_of_objects = []
    for object_ in objects:
        vertices = []
        for vertex in object_.bounding_poly.normalized_vertices:
            vertices.append({'x': vertex.x, 'y':vertex.y})
        obj = {
            'name': object_.name,
            'confidence': object_.score,
            'vertices': vertices
        }
        list_of_objects.append(obj)
    response = {'objects' : list_of_objects}
    return response
