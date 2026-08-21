from PIL import Image
from src.image_processor import detect_ingredients


image_path = r"C:\Users\konga\OneDrive\Desktop\RecipeChatbot\Ingredientimage.png"

image = Image.open(image_path)

results = detect_ingredients(image)

print("\nDetected ingredients:")

for ingredient, score in results:

    print(
        f"{ingredient}: {score:.2f}"
    )