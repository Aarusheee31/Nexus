"""
FlavorBridge Flask API - Connect React frontend to Python backend.
All mock data comes from src/data/mock_data.py only.
Run: python api.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flavor_bridge import recommend_recipes
from src.data.mock_data import (
    COMFORT_CUISINES,
    TARGET_CUISINES,
    COMMON_ALLERGENS,
    ALLERGEN_SUBSTITUTES,
    INITIAL_USER_PROFILE,
    INITIAL_SETTINGS,
    MOCK_RECIPES,
    MOCK_RESTAURANTS,
    INSTRUCTIONS,
)

TITLE_TO_ID = {
    "Chinese-Style Broccoli Salad": "C001",
    "Chinese Green Bean Stir-Fry": "C002",
    "Spicy Cabbage Kimchi": "K001",
    "Gochujang Sauce": "K002",
    "Judy's Hearty Vegetable Minestrone Soup": "I001",
    "Italian Zucchini Saute": "I002",
}

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])


@app.route("/api/data", methods=["GET"])
def get_data():
    """All UI mock data from mock_data.py."""
    recipes_flat = {}
    for recipes in MOCK_RECIPES.values():
        for r in recipes:
            t = r.get("title", "Unknown")
            rid = r.get("id") or TITLE_TO_ID.get(t)
            steps = INSTRUCTIONS.get(rid, {}).get("steps", []) if rid else []
            recipes_flat[t] = {
                "name": t,
                "image": "🍽️",
                "prepTime": f"{r.get('prep_time', 0)} min",
                "cookTime": f"{r.get('cook_time', 0)} min",
                "servings": str(r.get("servings", 4)),
                "difficulty": "Easy",
                "ingredients": [],
                "instructions": steps,
            }
    return jsonify({
        "comfortCuisines": COMFORT_CUISINES,
        "targetCuisines": TARGET_CUISINES,
        "commonAllergens": COMMON_ALLERGENS,
        "allergenSubstitutes": ALLERGEN_SUBSTITUTES,
        "initialUserProfile": INITIAL_USER_PROFILE,
        "initialSettings": INITIAL_SETTINGS,
        "restaurants": MOCK_RESTAURANTS,
        "recipes": recipes_flat,
    })


@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json() or {}
    source = data.get("comfortDish", "").strip()
    target = data.get("targetCuisine", "").strip()
    excluded = data.get("excludedAllergens", [])

    if not source or not target:
        return jsonify({"error": "comfortDish (source recipe) and targetCuisine are required"}), 400

    results = recommend_recipes(
        source_recipe_title=source,
        target_cuisine=target,
        excluded_allergens=excluded,
    )
    return jsonify(results)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "FlavorBridge API"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)