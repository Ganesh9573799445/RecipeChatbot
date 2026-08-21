import ast
import os
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# Paths
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "RAW_recipes.csv"
)

EMBEDDINGS_PATH = os.path.join(
    BASE_DIR,
    "models",
    "recipe_embeddings.npy"
)


# -----------------------------
# Load recipe dataset
# -----------------------------

df = pd.read_csv(DATA_PATH)


# Convert ingredients and steps
df['ingredients'] = df['ingredients'].apply(
    lambda x: ast.literal_eval(x)
    if isinstance(x, str) else x
)

df['steps'] = df['steps'].apply(
    lambda x: ast.literal_eval(x)
    if isinstance(x, str) else x
)


# Create ingredient text
df['ingredient_text'] = df['ingredients'].apply(
    lambda x: ', '.join(x)
)


# Remove missing recipe names
df = df.dropna(subset=['name'])


# Remove duplicate recipes
df = df.drop_duplicates(
    subset='name'
)


# -----------------------------
# Load Sentence-BERT
# -----------------------------

model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)


# -----------------------------
# Load recipe embeddings
# -----------------------------

recipe_embeddings = np.load(
    EMBEDDINGS_PATH
)


# -----------------------------
# Ingredient cleaning
# -----------------------------

def clean_ingredient(ingredient):

    ingredient = ingredient.lower().strip()

    if ingredient.endswith("ies"):
        ingredient = ingredient[:-3] + "y"

    elif ingredient.endswith("oes"):
        ingredient = ingredient[:-2]

    elif ingredient.endswith("s") and not ingredient.endswith("ss"):
        ingredient = ingredient[:-1]

    return ingredient


# -----------------------------
# Ingredient matching
# -----------------------------

def get_ingredient_match(
    user_ingredients,
    recipe_ingredients
):

    user_list = [
        clean_ingredient(x)
        for x in user_ingredients.split(',')
    ]

    recipe_list = [
        clean_ingredient(x)
        for x in recipe_ingredients.split(',')
    ]

    matched = []
    missing = []

    for user_item in user_list:

        found = False

        for recipe_item in recipe_list:

            if user_item == recipe_item:

                matched.append(user_item)

                found = True

                break

        if not found:

            missing.append(user_item)

    if len(user_list) == 0:
        score = 0

    else:
        score = len(matched) / len(user_list)

    return score, matched, missing


# -----------------------------
# Compare ingredients
# -----------------------------

def compare_ingredients(
    user_ingredients,
    recipe_ingredients
):

    user_list = [
        clean_ingredient(x)
        for x in user_ingredients.split(',')
    ]

    recipe_list = [
        clean_ingredient(x)
        for x in recipe_ingredients.split(',')
    ]

    matched = []
    needed = []

    for recipe_item in recipe_list:

        found = False

        for user_item in user_list:

            if recipe_item == user_item:

                matched.append(recipe_item)

                found = True

                break

        if not found:

            needed.append(recipe_item)

    return matched, needed


# -----------------------------
# Recommendation function
# -----------------------------

def recommend_recipes(
    user_ingredients,
    top_n=5
):

    # User embedding
    user_embedding = model.encode(
        [user_ingredients]
    )

    # Semantic similarity
    similarities = cosine_similarity(
        user_embedding,
        recipe_embeddings
    )[0]

    # Top 20 candidates
    top_indices = np.argsort(
        similarities
    )[-20:][::-1]

    candidates = df.iloc[
        top_indices
    ].copy()

    candidates['similarity'] = (
        similarities[top_indices]
    )

    # Ingredient matching
    match_results = candidates[
        'ingredient_text'
    ].apply(
        lambda x: get_ingredient_match(
            user_ingredients,
            x
        )
    )

    candidates['ingredient_match'] = (
        match_results.apply(
            lambda x: x[0]
        )
    )

    # Final score
    candidates['final_score'] = (
        candidates['similarity'] * 0.70
        +
        candidates['ingredient_match'] * 0.30
    )

    # You have / You need
    comparison_results = candidates[
        'ingredient_text'
    ].apply(
        lambda x: compare_ingredients(
            user_ingredients,
            x
        )
    )

    candidates['you_have'] = (
        comparison_results.apply(
            lambda x: x[0]
        )
    )

    candidates['you_need'] = (
        comparison_results.apply(
            lambda x: x[1]
        )
    )

    # Sort
    candidates = candidates.sort_values(
        by='final_score',
        ascending=False
    )

    return candidates.head(top_n)[
        [
            'id',
            'name',
            'ingredients',
            'steps',
            'description',
            'ingredient_text',
            'similarity',
            'ingredient_match',
            'you_have',
            'you_need',
            'final_score'
        ]
    ]