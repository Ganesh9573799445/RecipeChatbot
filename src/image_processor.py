from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch


# Load pretrained CLIP model
MODEL_NAME = "openai/clip-vit-base-patch32"

processor = CLIPProcessor.from_pretrained(MODEL_NAME)
model = CLIPModel.from_pretrained(MODEL_NAME)


# Ingredients that the model will check
INGREDIENTS = [
    "chicken",
    "beef",
    "pork",
    "shrimp",
    "fish",
    "rice",
    "potato",
    "tomato",
    "onion",
    "garlic",
    "carrot",
    "broccoli",
    "bell pepper",
    "green pepper",
    "cabbage",
    "spinach",
    "lettuce",
    "cucumber",
    "zucchini",
    "egg",
    "cheese",
    "mushroom",
    "ginger",
    "chili pepper",
    "corn",
    "peas",
    "beans",
    "lemon"
]


def detect_ingredients(image, threshold=0.06):

    image = image.convert("RGB")

    labels = [
        f"a photo of {ingredient}"
        for ingredient in INGREDIENTS
    ]

    inputs = processor(
        text=labels,
        images=image,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = outputs.logits_per_image.softmax(dim=1)[0]

    detected = []

    for ingredient, probability in zip(
        INGREDIENTS,
        probabilities
    ):

        score = probability.item()

        if score >= threshold:
            detected.append(
                (ingredient, score)
            )

    detected.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return detected