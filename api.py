"""
FlavorBridge Flask API - Connect React frontend to Python backend.
Uses real Foodoscope API for recipe data.
Run: python api.py
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flavor_bridge import (
    recommend_recipes, 
    fetch_recipe_by_title, 
    fetch_recipe_instructions, 
    fetch_recipes_by_region,
    API_BASE_URL
)
from src.data.mock_data import (
    COMFORT_CUISINES,
    TARGET_CUISINES,
    COMMON_ALLERGENS,
    ALLERGEN_SUBSTITUTES,
    INITIAL_USER_PROFILE,
    INITIAL_SETTINGS,
    MOCK_RESTAURANTS,
)
import requests

# Get API token from environment variable
API_TOKEN = os.getenv('FOODOSCOPE_API_TOKEN', 'Y2OYhJpk2OjKmCic-fmVCm_BPXuhBc2N75hZukqjQstOyFPF')
API_HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

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


@app.route("/api/recipe/search", methods=["POST"])
def search_recipes():
    """
    Search for recipes by title/query.
    Body: { "query": "chicken curry" }
    """
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    if len(query) < 3:
        return jsonify({"error": "Query must be at least 3 characters"}), 400
    
    print(f"\n🔍 RECIPE SEARCH REQUEST")
    print(f"   Query: '{query}'")
    
    try:
        # Call Foodoscope API to search recipes by title
        url = f"{API_BASE_URL}/recipe-bytitle/recipeByTitle"
        params = {"title": query}
        
        print(f"   API URL: {url}")
        print(f"   Params: {params}")
        
        response = requests.get(url, params=params, headers=API_HEADERS, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            api_data = response.json()
            
            if api_data.get("success") and api_data.get("data"):
                recipes = api_data["data"]
                print(f"   ✅ Found {len(recipes)} recipes")
                
                # Return top 20 results
                return jsonify({
                    "success": True,
                    "query": query,
                    "count": len(recipes),
                    "recipes": recipes[:20]
                })
            else:
                print(f"   ❌ No recipes found")
                return jsonify({
                    "success": True,
                    "query": query,
                    "count": 0,
                    "recipes": []
                })
        else:
            print(f"   ❌ API Error: {response.status_code}")
            return jsonify({"error": f"API returned status {response.status_code}"}), 500
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/recipe/details/<recipe_id>", methods=["GET"])
def get_recipe_details(recipe_id):
    """
    Get full recipe details including instructions.
    """
    print(f"\n📖 RECIPE DETAILS REQUEST")
    print(f"   Recipe ID: {recipe_id}")
    
    try:
        # Fetch instructions
        instructions = fetch_recipe_instructions(recipe_id)
        
        print(f"   ✅ Found {len(instructions)} instruction steps")
        
        return jsonify({
            "success": True,
            "recipe_id": recipe_id,
            "instructions": instructions
        })
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return jsonify({"error": str(e)}), 500


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
    print(f"  🔑 API Token: {API_TOKEN[:20]}..." if API_TOKEN else "  ❌ No API token found!")
    print("  🌐 Server: http://localhost:5000")
    print("  📡 CORS enabled for: http://localhost:3000")
    print("")
    print("  Available Endpoints:")
    print("    • GET  /api/health")
    print("    • GET  /api/data")
    print("    • POST /api/recommend")
    print("    • POST /api/recipe/search")
    print("    • GET  /api/recipe/details/<recipe_id>")
    print("    • GET  /api/recipe/<title>")
    print("    • GET  /api/recipes/region/<region>")
    print("")
    print("═══════════════════════════════════════════════════════════════════════════════")
    print("\n  Waiting for requests...\n")
    
    app.run(port=5000, debug=True)