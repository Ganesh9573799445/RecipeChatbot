from PIL import Image

from src.image_processor import detect_ingredients
from src.recommender import recommend_recipes


# Image path
image_path = r"C:\Users\konga\OneDrive\Desktop\RecipeChatbot\Ingredientimage.png"


# Load image
image = Image.open(image_path)


# Detect ingredients
detected = detect_ingredients(image)


print("\nDetected ingredients:")

for ingredient, score in detected:
    print(f"{ingredient}: {score:.2f}")


# Convert detected ingredients into text
ingredient_text = ", ".join(
    ingredient
    for ingredient, score in detected
)


print("\nIngredients sent to recommender:")
print(ingredient_text)


# Get recommendations
recommendations = recommend_recipes(
    ingredient_text
)


print("\nRecommended Recipes:")

for _, recipe in recommendations.iterrows():

    print("\nRecipe:", recipe["name"])

    print(
        "Similarity:",
        round(recipe["similarity"], 3)
    )

    print(
        "Ingredient Match:",
        round(recipe["ingredient_match"], 3)
    )

    print(
        "Final Score:",
        round(recipe["final_score"], 3)
    )

    print(
        "You have:",
        recipe["you_have"]
    )

    print(
        "You need:",
        recipe["you_need"]
    )