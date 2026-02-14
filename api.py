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
API_KEY = os.getenv('API_KEY', 'Y2OYhJpk2OjKmCic-fmVCm_BPXuhBc2N75hZukqjQstOyFPF')
API_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

from collections import Counter

@app.route("/api/allergen/substitutes", methods=["POST"])
def get_allergen_substitutes():
    """
    Use FlavorDB API to find molecularly-similar substitutes for an allergen.
    Steps:
      1. Find entity by readable name → get dominant category
      2. Pick best matching entity alias from that category
      3. Call by-alias to get top similar entities
      4. Return top 3 as substitutes
    """
    data = request.get_json() or {}
    allergen = data.get("allergen", "").strip()

    if not allergen:
        return jsonify({"error": "allergen is required"}), 400

    print(f"\n{'🚨'*20}")
    print(f"  ALLERGEN SUBSTITUTE REQUEST RECEIVED")
    print(f"  Allergen: '{allergen}'")
    print(f"{'🚨'*20}")

    try:
        # ── STEP 1: Search FlavorDB by readable name ──────────────────────────
        print(f"\n  [STEP 1] Searching FlavorDB for entity: '{allergen.lower()}'")
        search_url = "https://api.foodoscope.com/flavordb/entities/by-entity-alias-readable"
        search_resp = requests.get(
            search_url,
            params={"entity_alias_readable": allergen.lower()},
            headers=API_HEADERS,
            timeout=10
        )
        print(f"  [STEP 1] Status: {search_resp.status_code}")

        if search_resp.status_code != 200:
            print(f"  [STEP 1] ❌ Failed - raw response: {search_resp.text[:200]}")
            return jsonify({"error": f"FlavorDB search failed: {search_resp.status_code}"}), 500

        search_data = search_resp.json()
        entities = search_data.get("content", [])
        print(f"  [STEP 1] ✅ Found {len(entities)} entity match(es):")
        for e in entities:
            print(f"           • {e.get('entity_alias_readable')} [{e.get('category_readable')}] alias={e.get('entity_alias')}")

        if not entities:
            print(f"  [STEP 1] ❌ No entities returned for '{allergen}'")
            return jsonify({"error": f"No FlavorDB entity found for '{allergen}'"}), 404

        # ── STEP 2: Find the dominant category ───────────────────────────────
        print(f"\n  [STEP 2] Determining dominant category...")
        categories = [e.get("category_readable", "") for e in entities if e.get("category_readable")]
        category_counts = Counter(categories)
        print(f"  [STEP 2] Category counts: {dict(category_counts)}")

        if not categories:
            return jsonify({"error": "No category data found"}), 404

        dominant_category = category_counts.most_common(1)[0][0]
        print(f"  [STEP 2] ✅ Dominant category: '{dominant_category}'")

        # ── STEP 3: Pick the best entity alias to query ───────────────────────
        print(f"\n  [STEP 3] Selecting best entity from dominant category '{dominant_category}'...")
        best_entity = next(
            (e for e in entities if e.get("category_readable") == dominant_category),
            entities[0]
        )
        print(f"  [STEP 3] Best entity: {best_entity.get('entity_alias_readable')}")

        # Prefer entity_alias_readable (properly capitalized) over raw alias slug
        # The by-alias endpoint expects names like "Mango", "Peanut", "Orange"
        alias_readable = best_entity.get("entity_alias_readable", "")
        alias_slug = best_entity.get("entity_alias", "")
        # Use readable name, capitalized — matches the API's expected format
        alias = alias_readable.title() if alias_readable else alias_slug.title()
        print(f"  [STEP 3] ✅ Using alias for pairing lookup: '{alias}'")

        # ── STEP 4: Get molecularly similar foods via by-alias ────────────────
        print(f"\n  [STEP 4] Fetching molecularly similar foods for '{alias}'...")
        pairing_url = "https://api.foodoscope.com/flavordb/food/by-alias"
        pairing_resp = requests.get(
            pairing_url,
            params={"food_pair": alias},
            headers=API_HEADERS,
            timeout=10
        )
        print(f"  [STEP 4] Status: {pairing_resp.status_code}")

        if pairing_resp.status_code != 200:
            print(f"  [STEP 4] ❌ Failed - raw response: {pairing_resp.text[:200]}")
            return jsonify({"error": f"FlavorDB pairing failed: {pairing_resp.status_code}"}), 500

        pairing_data = pairing_resp.json()
        similar_entities = pairing_data.get("topSimilarEntities", [])
        print(f"  [STEP 4] ✅ Found {len(similar_entities)} similar entities:")
        for s in similar_entities[:5]:
            print(f"           • {s.get('entityName')} [{s.get('category')}] — {s.get('similarMolecules')} shared molecules")
        if len(similar_entities) > 5:
            print(f"           ... and {len(similar_entities) - 5} more")

        # ── STEP 5: Filter to same category, return top 3 ────────────────────
        print(f"\n  [STEP 5] Filtering to dominant category '{dominant_category}'...")
        same_cat = [
            e for e in similar_entities
            if e.get("category", "").lower().replace("-", " ") in dominant_category.lower()
            or dominant_category.lower() in e.get("category", "").lower()
        ]
        print(f"  [STEP 5] Same-category matches: {len(same_cat)}")

        # Use same-category if we have at least 2; otherwise fall back to top overall
        if len(same_cat) >= 2:
            top_substitutes = same_cat[:3]
            print(f"  [STEP 5] ✅ Using {len(top_substitutes)} same-category substitutes")
        else:
            top_substitutes = similar_entities[:3]
            print(f"  [STEP 5] ⚠️  Not enough same-category results, using top {len(top_substitutes)} overall")

        for s in top_substitutes:
            print(f"           → {s.get('entityName')} ({s.get('similarMolecules')} molecules)")

        # ── BUILD RESPONSE ────────────────────────────────────────────────────
        result = {
            "allergen": allergen,
            "matched_entity": best_entity.get("entity_alias_readable"),
            "category": dominant_category,
            "substitutes": [
                {
                    "name": s["entityName"],
                    "category": s.get("category", ""),
                    "similar_molecules": s.get("similarMolecules", 0),
                    "wikipedia": s.get("wikipedia", ""),
                    "description": (
                        f"Shares {s.get('similarMolecules', 0)} flavor molecules with {allergen}. "
                        f"A natural {s.get('category', 'food').lower()} substitute."
                    )
                }
                for s in top_substitutes
            ]
        }

        print(f"\n  ✅ DONE — returning {len(result['substitutes'])} substitutes for '{allergen}'")
        print(f"{'─'*50}\n")
        return jsonify(result)

    except Exception as e:
        print(f"\n  ❌ UNHANDLED ERROR in allergen substitutes: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


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
    print(f"  🔑 API Token: {API_KEY[:20]}..." if API_KEY else "  ❌ No API token found!")
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