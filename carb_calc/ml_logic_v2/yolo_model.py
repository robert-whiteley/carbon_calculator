from transformers import YolosForObjectDetection
import torch

def load_model():
    """
    Loads pretrained model from transformers.
    """
    model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')

    print("✅ Model loaded")

    return model

def prediction(processed_image, target_sizes, image_processor, image, model):
    """
    Takes processed image and returns outputs.
    """
    outputs = model(**processed_image)
    results = image_processor.post_process_object_detection(outputs, threshold=0.3, target_sizes=target_sizes)[0]

    desired_classes = ['apple', 'banana', 'orange', 'broccoli', 'carrot']
    objs_bboxes = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        detected_class = model.config.id2label[label.item()]
        if detected_class in desired_classes:
            obj = {'class': detected_class}
            bboxes = []
            for i,vertex in enumerate(box):
                if not i%2:
                    bboxes.append(round(float(vertex/image.width),3))
                else:
                    bboxes.append(round(float(vertex/image.height),3))

            obj['bbox'] = bboxes
            objs_bboxes.append(obj)
    return objs_bboxes
