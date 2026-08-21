from src.recommender import recommend_recipes

results = recommend_recipes(
    "chicken, rice, onion, tomato"
)

print(results[
    [
        "name",
        "you_have",
        "you_need",
        "final_score"
    ]
])