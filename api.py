"""
FlavorBridge Flask API - Connect React frontend to Python backend.
Uses real Foodoscope API for recipe data.
Run: python api.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flavor_bridge import recommend_recipes, fetch_recipe_by_title, fetch_recipe_instructions, fetch_recipes_by_region
from src.data.mock_data import (
    COMFORT_CUISINES,
    TARGET_CUISINES,
    COMMON_ALLERGENS,
    ALLERGEN_SUBSTITUTES,
    INITIAL_USER_PROFILE,
    INITIAL_SETTINGS,
    MOCK_RESTAURANTS,
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})


@app.route("/api/data", methods=["GET"])
def get_data():
    """Return UI static data (cuisines, allergens, etc.) - still from mock_data for UI."""
    return jsonify({
        "comfortCuisines": COMFORT_CUISINES,
        "targetCuisines": TARGET_CUISINES,
        "commonAllergens": COMMON_ALLERGENS,
        "allergenSubstitutes": ALLERGEN_SUBSTITUTES,
        "initialUserProfile": INITIAL_USER_PROFILE,
        "initialSettings": INITIAL_SETTINGS,
        "restaurants": MOCK_RESTAURANTS,
    })


@app.route("/api/recipe/<recipe_title>", methods=["GET"])
def get_recipe_by_title(recipe_title):
    """Fetch a single recipe by title from the real API."""
    recipe = fetch_recipe_by_title(recipe_title)
    if not recipe:
        return jsonify({"error": f"Recipe '{recipe_title}' not found"}), 404
    
    # Also fetch instructions
    recipe_id = recipe.get("Recipe_id", "")
    instructions = fetch_recipe_instructions(recipe_id) if recipe_id else []
    
    return jsonify({
        "recipe": recipe,
        "instructions": instructions
    })


@app.route("/api/recipes/region/<region>", methods=["GET"])
def get_recipes_by_region(region):
    """Fetch recipes by region from the real API."""
    limit = request.args.get("limit", 10, type=int)
    diet = request.args.get("diet", "", type=str)
    
    recipes = fetch_recipes_by_region(region, diet=diet, limit=limit)
    
    if not recipes:
        return jsonify({"error": f"No recipes found for region '{region}'"}), 404
    
    return jsonify({
        "recipes": recipes,
        "count": len(recipes)
    })


@app.route("/api/recommend", methods=["POST"])
def recommend():
    """Main recommendation endpoint - uses real API data."""
    data = request.get_json() or {}
    source = data.get("comfortDish", "").strip()
    target = data.get("targetCuisine", "").strip()
    excluded = data.get("excludedAllergens", [])

    if not source or not target:
        return jsonify({"error": "comfortDish (source recipe) and targetCuisine are required"}), 400

    print(f"\n\n")
    print(f"╔{'═'*78}╗")
    print(f"║{' '*78}║")
    print(f"║{'  NEW RECOMMENDATION REQUEST':^78}║")
    print(f"║{' '*78}║")
    print(f"╚{'═'*78}╝")
    print(f"")
    print(f"  🍽️  Comfort Dish: {source}")
    print(f"  🌍 Target Cuisine: {target}")
    print(f"  🚫 Excluded Allergens: {excluded if excluded else 'None'}")
    print(f"")
    
    try:
        results = recommend_recipes(
            source_recipe_title=source,
            target_cuisine=target,
            excluded_allergens=excluded,
        )
        
        print(f"\n{'─'*80}")
        print(f"📤 FINAL RESULTS TO SEND TO FRONTEND")
        print(f"{'─'*80}")
        print(f"Total Recommendations: {len(results)}")
        print(f"")
        for i, r in enumerate(results, 1):
            print(f"  {i}. {r.get('recipe_title')}")
            print(f"     Score: {r.get('final_score'):.3f}")
            print(f"     Explanation: {r.get('explanation', ['No explanation'])[0][:60]}...")
        print(f"{'─'*80}\n")
        
        return jsonify(results)
        
    except Exception as e:
        print(f"\n❌ ERROR in recommendation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "FlavorBridge API with Real Data"})


if __name__ == "__main__":
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                               ║")
    print("║                        🌉 FLAVORBRIDGE API SERVER 🌉                          ║")
    print("║                                                                               ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")
    print("")
    print("  ✅ Using REAL Foodoscope API for recipe data")
    print("  🌐 Server: http://localhost:5000")
    print("  📡 CORS enabled for: http://localhost:3000")
    print("")
    print("  Available Endpoints:")
    print("    • GET  /api/health")
    print("    • GET  /api/data")
    print("    • POST /api/recommend")
    print("    • GET  /api/recipe/<title>")
    print("    • GET  /api/recipes/region/<region>")
    print("")
    print("═══════════════════════════════════════════════════════════════════════════════")
    print("\n  Waiting for requests...\n")
    
    app.run(port=5000, debug=True)