from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
from PIL import Image
import requests
from io import BytesIO

# Load the image processor and model
processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
model = AutoModelForImageClassification.from_pretrained("google/vit-base-patch16-224-in21k")

def classify_image(filepath):
    """Classify an image and return the predicted label."""
    # Load image
    image = Image.open(filepath)
    
    # Preprocess the image
    inputs = processor(images=image, return_tensors="pt")
    
    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Extract predictions
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1)
    
    # Map the output to class labels
    labels = model.config.id2label  # Get the label mapping from the model config
    predicted_label = labels[predictions.item()]
    return predicted_label
