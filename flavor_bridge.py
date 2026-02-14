"""
FlavorBridge - Translate comfort dishes across cuisines.
Uses real Foodoscope API for recipe data.
"""

from __future__ import annotations
import math
import requests
from typing import Any
import os # Import the os module
from dotenv import load_dotenv

from src.data import mock_data

load_dotenv()

# --- API Configuration ---
API_BASE_URL = "https://api.foodoscope.com/recipe2-api"
API_KEY = os.getenv("API_KEY") # Get the token from environment variables
API_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

# --- Common Ingredients Database ---
COMMON_INGREDIENTS = [
    "water", "cinnamon", "breadcrumb", "flour tortilla", "lemon juice", "lime juice",
    "white wine", "red wine", "flour", "purpose flour", "soy sauce", "tomato sauce",
    "butter", "milk", "vegetable broth", "cream mushroom soup", "sesame oil",
    "avocado", "steak", "salmon fillet", "broccoli", "artichoke heart", "lemon",
    "orange juice", "mushroom", "button mushroom", "garlic clove", "garlic", "vanilla",
    "black bean", "cornstarch", "corn", "egg", "beef", "almond", "walnut", "bay leaf",
    "olive oil", "vegetable oil", "shallot", "shrimp", "black pepper", "pepper",
    "onion", "tomato"
]

# Create lowercase version for matching
COMMON_INGREDIENTS_LOWER = [ing.lower() for ing in COMMON_INGREDIENTS]

# --- Texture Keywords ---
TEXTURE_KEYWORDS = {
    "creamy": ["cream", "milk", "butter", "cheese", "coconut milk", "yogurt", "sour cream"],
    "crunchy": ["crispy", "fried", "toasted", "nuts", "breadcrumb", "crackers"],
    "soft": ["simmer", "boil", "mash", "puree", "tender", "soft"],
    "chewy": ["pasta", "noodles", "rice", "bread", "dough"],
    "crispy": ["fry", "roast", "bake", "crisp", "sear"],
    "smooth": ["blend", "puree", "strain", "smooth", "silky"],
    "chunky": ["dice", "chop", "cube", "chunks", "pieces"],
    "tender": ["braise", "slow cook", "stew", "tender", "fall apart"],
}

# --- Comfort Level Keywords ---
COMFORT_KEYWORDS = {
    "high_comfort": ["soup", "stew", "curry", "casserole", "pot", "simmer", "braise", "comfort", "hearty", "warm"],
    "medium_comfort": ["pasta", "rice", "noodles", "bowl", "bake"],
    "light": ["salad", "fresh", "grilled", "steamed", "light", "healthy"],
}

# --- Adaptability Factors ---
ADAPTABILITY_KEYWORDS = {
    "easy_swap": ["chicken", "beef", "pork", "tofu", "shrimp"],  # Easy protein swaps
    "common_techniques": ["simmer", "stir", "cook", "heat", "add", "mix"],  # Common cooking methods
    "complex_techniques": ["temper", "fold", "knead", "proof", "reduce", "emulsify"],  # Complex techniques
}

# --- Static data from mock_data (for scoring logic only) ---
METHOD_KEYWORDS = mock_data.METHOD_KEYWORDS
PROTEIN_MAP = mock_data.PROTEIN_MAP
ALLERGEN_KEYWORDS_BACKEND = mock_data.ALLERGEN_KEYWORDS_BACKEND
MOCK_FOOD_PAIR = mock_data.MOCK_FOOD_PAIR


# === API FUNCTIONS ===

def fetch_recipe_by_title(title: str) -> dict | None:
    """Fetch recipe from API by title."""
    try:
        url = f"{API_BASE_URL}/recipe-bytitle/recipeByTitle"
        params = {"title": title}
        print(f"\n🔍 API CALL: Recipe by Title")
        print(f"   URL: {url}")
        print(f"   Params: {params}")
        
        response = requests.get(url, params=params, headers=API_HEADERS, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data.get('message', 'No message')}")
            
            if data.get("success") and data.get("data"):
                recipes = data["data"]
                print(f"   ✅ Found {len(recipes)} recipe(s)")
                if recipes and len(recipes) > 0:
                    print(f"   📋 First match: {recipes[0].get('Recipe_title', 'Unknown')}")
                    return recipes[0]
            else:
                print(f"   ❌ No recipes found in response")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
        
        return None
    except Exception as e:
        print(f"❌ ERROR fetching recipe by title: {e}")
        return None


def fetch_recipe_instructions(recipe_id: str) -> list[str]:
    """Fetch recipe instructions from API by recipe_id."""
    try:
        url = f"{API_BASE_URL}/instructions/{recipe_id}"
        print(f"\n📖 API CALL: Recipe Instructions")
        print(f"   URL: {url}")
        print(f"   Recipe ID: {recipe_id}")
        
        response = requests.get(url, headers=API_HEADERS, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "steps" in data:
                steps = data["steps"]
                print(f"   ✅ Found {len(steps)} cooking steps")
                if steps:
                    print(f"   First step: {steps[0][:80]}...")
                return steps
            else:
                print(f"   ❌ No 'steps' field in response")
                print(f"   Response keys: {list(data.keys())}")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
        
        return []
    except Exception as e:
        print(f"❌ ERROR fetching instructions: {e}")
        return []


def _normalize_region_name(region: str) -> str:
    """Normalize region name for API compatibility.
    
    The API expects single region names like 'Chinese', 'Italian', etc.
    If user provides compound names like 'Chinese and Mongolian', extract first region.
    """
    region = region.strip()
    
    # Handle compound regions (e.g., "Chinese and Mongolian" -> "Chinese")
    if " and " in region.lower():
        parts = region.split(" and ")
        normalized = parts[0].strip()
        print(f"\n⚠️  Compound region detected: '{region}'")
        print(f"   Using first region: '{normalized}'")
        return normalized
    
    # Handle other separators
    if "/" in region:
        parts = region.split("/")
        normalized = parts[0].strip()
        print(f"\n⚠️  Compound region detected: '{region}'")
        print(f"   Using first region: '{normalized}'")
        return normalized
    
    return region


def fetch_recipes_by_region(region: str, diet: str = "", limit: int = 50) -> list[dict]:
    """Fetch recipes from API by region and optional diet."""
    try:
        # Normalize region name
        normalized_region = _normalize_region_name(region)
        
        url = f"{API_BASE_URL}/recipe/region-diet/region-diet"
        params = {
            "region": normalized_region,
            "diet": 'vegan',
            "limit": limit
        }
        if diet:
            params["diet"] = diet
        
        print(f"\n🌍 API CALL: Recipes by Region")
        print(f"   URL: {url}")
        print(f"   Params: {params}")
        
        response = requests.get(url, params=params, headers=API_HEADERS, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data.get('message', 'No message')}")
            
            if data.get("success") and data.get("data"):
                recipes = data["data"]
                print(f"   ✅ Found {len(recipes)} recipes")
                
                # Show first few recipe titles
                if recipes:
                    print(f"   Sample recipes:")
                    for i, r in enumerate(recipes[:5], 1):
                        print(f"      {i}. {r.get('Recipe_title', 'Unknown')}")
                
                return recipes
            else:
                print(f"   ❌ No recipes found in response")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
            # Try alternative region names if first attempt failed
            if response.status_code == 400:
                print(f"\n   💡 Trying alternative region spellings...")
                alternatives = _get_alternative_region_names(region)
                for alt_region in alternatives:
                    print(f"   Trying: '{alt_region}'")
                    params["region"] = alt_region
                    response = requests.get(url, params=params, headers=API_HEADERS, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("success") and data.get("data"):
                            print(f"   ✅ Success with alternative name: '{alt_region}'")
                            return data["data"]
        
        return []
    except Exception as e:
        print(f"❌ ERROR fetching recipes by region: {e}")
        return []


def _get_alternative_region_names(region: str) -> list[str]:
    """Get alternative spellings/names for a region.
    
    Some regions might be named differently in the API.
    """
    region_lower = region.lower()
    alternatives = []
    
    # Common alternatives
    mappings = {
        "chinese and mongolian": ["Chinese", "Mongolian", "Asian"],
        "chinese": ["Chinese", "Asian"],
        "italian": ["Italian", "European"],
        "mexican": ["Mexican", "Latin American"],
        "indian": ["Indian", "Asian"],
        "japanese": ["Japanese", "Asian"],
        "thai": ["Thai", "Asian"],
        "french": ["French", "European"],
        "greek": ["Greek", "European"],
        "middle eastern": ["Middle Eastern", "Asian"],
        "spanish": ["Spanish", "European"],
        "korean": ["Korean", "Asian"],
        "vietnamese": ["Vietnamese", "Asian"],
    }
    
    for key, values in mappings.items():
        if key in region_lower:
            alternatives.extend([v for v in values if v.lower() != region_lower])
            break
    
    return alternatives[:3]  # Return max 3 alternatives


# === HELPER FUNCTIONS ===

def _parse_processes(processes_str: str) -> list[str]:
    """Parse the Processes field (e.g. 'heat||cook||stir') into a list."""
    if not processes_str:
        return []
    return [p.strip() for p in str(processes_str).split("||") if p.strip()]


def extract_ingredients_from_instructions(instructions: list[str]) -> list[str]:
    """
    Extract ingredients from cooking instructions by matching against COMMON_INGREDIENTS.
    
    Args:
        instructions: List of cooking step strings
        
    Returns:
        List of matched ingredients found in the instructions
    """
    found_ingredients = set()
    
    # Combine all instructions into one text for searching
    full_text = " ".join(instructions).lower()
    
    # Search for each common ingredient in the instructions
    for ingredient in COMMON_INGREDIENTS_LOWER:
        if ingredient in full_text:
            found_ingredients.add(ingredient)
    
    # Convert to sorted list for consistency
    result = sorted(list(found_ingredients))
    
    return result


def _get_ingredients_from_title(title: str) -> list[str]:
    """Infer ingredients from recipe title for allergen check."""
    t = title.lower()
    out = []
    for _, kws in PROTEIN_MAP.items():
        if any(kw in t for kw in kws):
            out.extend(kws[:1])
    if "vegetable" in t or "minestrone" in t or "broccoli" in t or "zucchini" in t:
        out.extend(["vegetable"])
    if "curry" in t:
        out.extend(["chicken", "coconut"])
    if "lentil" in t:
        out.extend(["lentil"])
    if "biryani" in t:
        out.extend(["rice"])
    return out if out else ["unknown"]


def detect_cooking_method(instructions: list[str]) -> str:
    """Detect primary cooking method from steps using METHOD_KEYWORDS."""
    text = " ".join(s.lower() for s in instructions)
    best_method, best_count = "slow_saucy", 0
    for method, keywords in METHOD_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in text)
        if count > best_count:
            best_count, best_method = count, method
    return best_method


def detect_protein(recipe_title: str) -> str:
    """Detect protein type from recipe title using PROTEIN_MAP."""
    t = recipe_title.lower()
    for protein, keywords in PROTEIN_MAP.items():
        if any(kw in t for kw in keywords):
            return protein
    return ""


def _infer_flavor_style(recipe_title: str, method: str) -> dict[str, float]:
    """Infer flavor style from dish name and cooking method."""
    title = recipe_title.lower()
    vector = {}
    if "curry" in title or "soup" in title:
        vector["savory"] = 0.4
        vector["aromatic"] = 0.3
    if "salad" in title:
        vector["fresh"] = 0.5
    if "kimchi" in title or "sauce" in title:
        vector["bold"] = 0.4
    if method == "slow_saucy":
        vector["comfort"] = 0.5
    if method == "stir_fry":
        vector["aromatic"] = vector.get("aromatic", 0) + 0.3
    if not vector:
        vector["savory"] = 0.5
    total = sum(vector.values())
    return {k: v / total for k, v in vector.items()} if total else {"savory": 0.5}


def flavor_similarity(source_vector: dict, target_vector: dict) -> float:
    """Cosine-like similarity between two flavor vectors."""
    if not source_vector or not target_vector:
        return 0.5
    all_keys = set(source_vector) | set(target_vector)
    dot = sum(source_vector.get(k, 0) * target_vector.get(k, 0) for k in all_keys)
    mag_s = math.sqrt(sum(v * v for v in source_vector.values()))
    mag_t = math.sqrt(sum(v * v for v in target_vector.values()))
    if mag_s == 0 or mag_t == 0:
        return 0.5
    return max(0.0, min(1.0, dot / (mag_s * mag_t)))


def ingredient_similarity(source_ingredients: list[str], target_ingredients: list[str]) -> float:
    """
    Calculate similarity between two ingredient lists using Jaccard similarity.
    
    Jaccard similarity = (intersection) / (union)
    
    Args:
        source_ingredients: List of ingredients from source recipe
        target_ingredients: List of ingredients from target recipe
        
    Returns:
        Similarity score between 0.0 and 1.0
    """
    if not source_ingredients or not target_ingredients:
        return 0.0
    
    # Convert to sets for intersection/union operations
    source_set = set(ing.lower().strip() for ing in source_ingredients)
    target_set = set(ing.lower().strip() for ing in target_ingredients)
    
    # Calculate Jaccard similarity
    intersection = len(source_set & target_set)
    union = len(source_set | target_set)
    
    if union == 0:
        return 0.0
    
    similarity = intersection / union
    
    return similarity


def detect_comfort_level(title: str, instructions: list[str], method: str) -> float:
    """
    Detect comfort level of a dish (0.0 to 1.0).
    
    High comfort: Soups, stews, slow-cooked dishes
    Medium comfort: Pasta, rice dishes, casseroles
    Light: Salads, grilled, fresh dishes
    
    Returns:
        Comfort score between 0.0 (light) and 1.0 (very comforting)
    """
    text = (title + " " + " ".join(instructions)).lower()
    
    high_count = sum(1 for kw in COMFORT_KEYWORDS["high_comfort"] if kw in text)
    medium_count = sum(1 for kw in COMFORT_KEYWORDS["medium_comfort"] if kw in text)
    light_count = sum(1 for kw in COMFORT_KEYWORDS["light"] if kw in text)
    
    # Additional boost for slow cooking methods
    if method == "slow_saucy":
        high_count += 2
    
    total = high_count + medium_count + light_count
    if total == 0:
        return 0.5  # Default moderate comfort
    
    # Weighted score: high comfort gets more weight
    score = (high_count * 1.0 + medium_count * 0.5 + light_count * 0.2) / total
    return min(1.0, score)


def detect_texture_profile(title: str, instructions: list[str], ingredients: list[str]) -> dict[str, float]:
    """
    Detect texture profile of a dish.
    
    Returns:
        Dictionary of texture types and their scores
        Example: {"creamy": 0.4, "soft": 0.3, "chunky": 0.3}
    """
    text = (title + " " + " ".join(instructions) + " " + " ".join(ingredients)).lower()
    
    texture_scores = {}
    for texture, keywords in TEXTURE_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in text)
        if count > 0:
            texture_scores[texture] = count
    
    # Normalize to sum to 1.0
    total = sum(texture_scores.values())
    if total > 0:
        texture_scores = {k: v / total for k, v in texture_scores.items()}
    
    return texture_scores


def calculate_texture_similarity(source_texture: dict, target_texture: dict) -> float:
    """
    Calculate similarity between two texture profiles using cosine similarity.
    
    Returns:
        Similarity score between 0.0 and 1.0
    """
    if not source_texture or not target_texture:
        return 0.5  # Default moderate similarity
    
    all_textures = set(source_texture.keys()) | set(target_texture.keys())
    
    dot_product = sum(
        source_texture.get(t, 0) * target_texture.get(t, 0) 
        for t in all_textures
    )
    
    mag_source = math.sqrt(sum(v * v for v in source_texture.values()))
    mag_target = math.sqrt(sum(v * v for v in target_texture.values()))
    
    if mag_source == 0 or mag_target == 0:
        return 0.5
    
    return dot_product / (mag_source * mag_target)


def calculate_adaptability(source: dict, target: dict) -> float:
    """
    Calculate how easy it is to adapt source recipe to target recipe.
    
    Factors:
    - Same cooking method = easier (40%)
    - Common ingredients = easier (30%)
    - Simple techniques = easier (20%)
    - Similar proteins = easier (10%)
    
    Returns:
        Adaptability score between 0.0 (hard) and 1.0 (easy)
    """
    score = 0.0
    
    # 1. Same cooking method (40%)
    if source.get("method") == target.get("method"):
        score += 0.4
    
    # 2. Ingredient overlap (30%)
    ing_sim = ingredient_similarity(
        source.get("ingredients_extracted", []),
        target.get("ingredients_extracted", [])
    )
    score += 0.3 * ing_sim
    
    # 3. Technique complexity (20%)
    # If both use common techniques, easier to adapt
    source_inst = " ".join(source.get("instructions", [])).lower()
    target_inst = " ".join(target.get("instructions", [])).lower()
    
    # Count common vs complex techniques
    common_in_target = sum(1 for kw in ADAPTABILITY_KEYWORDS["common_techniques"] if kw in target_inst)
    complex_in_target = sum(1 for kw in ADAPTABILITY_KEYWORDS["complex_techniques"] if kw in target_inst)
    
    if common_in_target > 0:
        technique_score = common_in_target / (common_in_target + complex_in_target + 1)
        score += 0.2 * technique_score
    else:
        score += 0.1  # Some baseline
    
    # 4. Protein similarity (10%)
    if source.get("protein") and source.get("protein") == target.get("protein"):
        score += 0.1
    elif not source.get("protein") or not target.get("protein"):
        score += 0.05  # Partial credit if one has no protein
    
    return min(1.0, score)


def contains_allergen(ingredients: list[str], excluded: list[str]) -> bool:
    """Check if any ingredient matches excluded allergens."""
    expanded = set()
    for e in excluded:
        el = str(e).lower()
        if el in ALLERGEN_KEYWORDS_BACKEND:
            expanded.update(ALLERGEN_KEYWORDS_BACKEND[el])
        else:
            expanded.add(el)
    ing_lower = [str(i).lower() for i in ingredients]
    return any(exc in ing or ing in exc for ing in ing_lower for exc in expanded)


def _pairing_overlap(source_protein: str, target_ingredients: list[str]) -> float:
    """Food pairing overlap using MOCK_FOOD_PAIR."""
    if source_protein != "chicken":
        return 0.5
    similar = [e["entityName"].lower() for e in MOCK_FOOD_PAIR["topSimilarEntities"]]
    target_lower = [str(i).lower() for i in target_ingredients]
    matches = sum(1 for s in similar if any(s in t or t in s for t in target_lower))
    return min(1.0, matches / max(1, len(MOCK_FOOD_PAIR["topSimilarEntities"])))


def score_recipe(source: dict, target: dict) -> tuple[float, list[str], dict]:
    """
    Score target vs source recipe.
    
    Weights: 
    - method: 0.30 (30%)
    - flavor: 0.25 (25%)
    - ingredient: 0.25 (25%)
    - protein: 0.10 (10%)
    - pairing: 0.10 (10%)
    
    Returns:
        (score, reasons, detailed_metrics)
        
        detailed_metrics contains:
        - comfort_similarity: 0-100%
        - flavor_similarity: 0-100%
        - adaptability: 0-100%
        - texture_alignment: 0-100%
        - ingredient_match: 0-100%
    """
    reasons = []
    method_w = 0.30
    flavor_w = 0.25
    ingredient_w = 0.25
    protein_w = 0.10
    pairing_w = 0.10

    # 1. Cooking Method Similarity (30%)
    src_m, tgt_m = source.get("method", ""), target.get("method", "")
    method_ok = 1.0 if src_m and src_m == tgt_m else 0.0
    if method_ok:
        reasons.append(f"✓ Same cooking method: {tgt_m}")
    else:
        reasons.append(f"Cooking style: {tgt_m} vs {src_m}")

    # 2. Flavor Profile Similarity (25%)
    flavor_sim = flavor_similarity(source.get("flavor_vector", {}), target.get("flavor_vector", {}))
    if flavor_sim >= 0.6:
        reasons.append(f"✓ Similar flavor profile (score: {flavor_sim:.2f})")
    else:
        reasons.append(f"Flavor similarity: {flavor_sim:.2f}")

    # 3. Ingredient Similarity (25%)
    ingredient_sim = ingredient_similarity(
        source.get("ingredients_extracted", []), 
        target.get("ingredients_extracted", [])
    )
    if ingredient_sim >= 0.3:
        common = set(source.get("ingredients_extracted", [])) & set(target.get("ingredients_extracted", []))
        common_list = sorted(list(common))[:3]  # Show top 3
        reasons.append(f"✓ Shared ingredients: {', '.join(common_list)}")
    else:
        reasons.append(f"Ingredient overlap: {ingredient_sim:.2f}")

    # 4. Protein Type Match (10%)
    src_p, tgt_p = source.get("protein", ""), target.get("protein", "")
    protein_ok = 1.0 if src_p and src_p == tgt_p else 0.0
    if protein_ok:
        reasons.append(f"✓ Same protein: {tgt_p}")
    else:
        if tgt_p:
            reasons.append(f"Protein: {tgt_p} vs {src_p}")

    # 5. Food Pairing Overlap (10%)
    pairing = _pairing_overlap(src_p, target.get("ingredients_extracted", []))
    if pairing >= 0.5:
        reasons.append("✓ Good food pairing compatibility")

    # Calculate weighted score
    score = (method_w * method_ok + 
             flavor_w * flavor_sim + 
             ingredient_w * ingredient_sim +
             protein_w * protein_ok + 
             pairing_w * pairing)
    
    # ===== CALCULATE DETAILED METRICS FOR FRONTEND =====
    
    # Comfort Similarity (how similar the comfort levels are)
    source_comfort = source.get("comfort_level", 0.5)
    target_comfort = target.get("comfort_level", 0.5)
    comfort_similarity = 1.0 - abs(source_comfort - target_comfort)  # Close comfort levels = high similarity
    
    # Texture Alignment (how similar the textures are)
    texture_sim = calculate_texture_similarity(
        source.get("texture_profile", {}),
        target.get("texture_profile", {})
    )
    
    # Adaptability (how easy to adapt from source to target)
    adaptability = calculate_adaptability(source, target)
    
    # Detailed metrics dictionary (all as percentages 0-100)
    detailed_metrics = {
        "comfort_similarity": round(comfort_similarity * 100, 1),
        "flavor_similarity": round(flavor_sim * 100, 1),
        "adaptability": round(adaptability * 100, 1),
        "texture_alignment": round(texture_sim * 100, 1),
        "ingredient_match": round(ingredient_sim * 100, 1),
    }
    
    return (score, reasons, detailed_metrics)


def recommend_recipes(
    source_recipe_title: str,
    target_cuisine: str,
    excluded_allergens: list[str] | None = None,
) -> dict:
    """
    Recommend target-cuisine recipes similar to source dish.
    ALWAYS returns at least some recommendations from the target region.
    """
    excluded_allergens = excluded_allergens or []

    print(f"\n{'='*60}")
    print(f"🎯 RECOMMENDATION REQUEST")
    print(f"{'='*60}")
    print(f"Source Dish: {source_recipe_title}")
    print(f"Target Cuisine: {target_cuisine}")
    print(f"Excluded Allergens: {excluded_allergens}")
    print(f"{'='*60}")

    # Step 1: Fetch source recipe from API
    source_recipe_data = fetch_recipe_by_title(source_recipe_title)
    
    if not source_recipe_data:
        # Fallback if recipe not found
        print(f"\n⚠️  Source recipe not found in API, using fallback analysis")
        src_inst = ["simmer", "cook"]
        src_method = detect_cooking_method(src_inst)
        src_protein = detect_protein(source_recipe_title)
        src_flavor = _infer_flavor_style(source_recipe_title, src_method)
        src_ingredients = _get_ingredients_from_title(source_recipe_title)
        src_ingredients_extracted = [] 
        src_comfort = 0.5  # ADD THIS LINE - Default comfort level
        src_texture = {} # No instructions to extract from
    else:
        # Get instructions for source recipe
        recipe_id = source_recipe_data.get("Recipe_id", "")
        src_inst = fetch_recipe_instructions(recipe_id) if recipe_id else []
        
        # If no instructions from API, try parsing Processes field
        if not src_inst and "Processes" in source_recipe_data:
            src_inst = _parse_processes(source_recipe_data.get("Processes", ""))
            print(f"\n📝 Using Processes field: {len(src_inst)} steps")
        
        if not src_inst:
            src_inst = ["cook"]
            print(f"\n⚠️  No instructions available, using default")
        
        # EXTRACT INGREDIENTS FROM INSTRUCTIONS
        src_ingredients_extracted = extract_ingredients_from_instructions(src_inst)
        print(f"\n🥘 Extracted {len(src_ingredients_extracted)} ingredients from instructions:")
        if src_ingredients_extracted:
            print(f"   {', '.join(src_ingredients_extracted[:10])}")
            if len(src_ingredients_extracted) > 10:
                print(f"   ... and {len(src_ingredients_extracted) - 10} more")
        
        src_method = detect_cooking_method(src_inst)
        src_title = source_recipe_data.get("Recipe_title", source_recipe_title)
        src_protein = detect_protein(src_title)
        src_flavor = _infer_flavor_style(src_title, src_method)
        src_ingredients = _get_ingredients_from_title(src_title)
        
        # Calculate comfort level and texture profile
        src_comfort = detect_comfort_level(src_title, src_inst, src_method)
        src_texture = detect_texture_profile(src_title, src_inst, src_ingredients_extracted)

    source_profile = {
        "method": src_method,
        "flavor_vector": src_flavor,
        "protein": src_protein,
        "ingredients": src_ingredients,
        "ingredients_extracted": src_ingredients_extracted,
        "instructions": src_inst,  # Store for adaptability calculation
        "comfort_level": src_comfort,
        "texture_profile": src_texture,
    }

    print(f"\n{'─'*60}")
    print(f"📊 SOURCE PROFILE ANALYSIS")
    print(f"{'─'*60}")
    print(f"Cooking Method: {src_method}")
    print(f"Protein Type: {src_protein or 'None detected'}")
    print(f"Comfort Level: {source_profile.get('comfort_level', 0) * 100:.0f}%")
    print(f"Flavor Vector: {src_flavor}")
    if source_profile.get('texture_profile'):
        texture_str = ', '.join([f"{k}: {v*100:.0f}%" for k, v in list(source_profile['texture_profile'].items())[:3]])
        print(f"Texture Profile: {texture_str}")
    print(f"Ingredients (from title): {src_ingredients}")
    print(f"Ingredients (extracted): {len(source_profile.get('ingredients_extracted', []))} found")
    if source_profile.get('ingredients_extracted'):
        ing_list = source_profile['ingredients_extracted'][:8]
        print(f"  Top ingredients: {', '.join(ing_list)}")
        if len(source_profile['ingredients_extracted']) > 8:
            print(f"  ... and {len(source_profile['ingredients_extracted']) - 8} more")

    # Step 2: Fetch target cuisine recipes from API
    target_recipes = fetch_recipes_by_region(target_cuisine, limit=100)
    
    if not target_recipes:
        print(f"\n❌ No recipes found for {target_cuisine}")
        print(f"\n💡 Tips:")
        print(f"   • Try simpler region names: 'Chinese' instead of 'Chinese and Mongolian'")
        print(f"   • Check spelling and capitalization")
        print(f"   • Try these common regions: Italian, Chinese, Mexican, Indian, French, Greek")
        
        return [{
            "recipe_title": f"No recipes found for '{target_cuisine}'",
            "final_score": 0.0,
            "explanation": [
                f"The API couldn't find recipes for '{target_cuisine}'.",
                "Try using a simpler region name like 'Chinese', 'Italian', 'Mexican', etc.",
                "Make sure the region name is capitalized correctly."
            ],
            "no_match_fallback": True,
        }]

    print(f"\n{'─'*60}")
    print(f"🔍 SCORING {len(target_recipes)} RECIPES")
    print(f"{'─'*60}")

    # Step 3: Filter by allergens and score each recipe
    scored = []
    filtered_count = 0
    
    for idx, recipe in enumerate(target_recipes):
        title = recipe.get("Recipe_title", "")
        tgt_ingredients = _get_ingredients_from_title(title)
        
        # Skip if contains allergens
        if contains_allergen(tgt_ingredients, excluded_allergens):
            filtered_count += 1
            continue
        
        # Get instructions
        recipe_id = recipe.get("Recipe_id", "")
        tgt_inst = []
        
        # Try to get instructions from API (but don't fetch for every recipe - too slow)
        # Instead, use Processes field if available
        if "Processes" in recipe:
            tgt_inst = _parse_processes(recipe.get("Processes", ""))
        
        if not tgt_inst:
            tgt_inst = ["cook"]
        
        # EXTRACT INGREDIENTS FROM TARGET RECIPE INSTRUCTIONS
        tgt_ingredients_extracted = extract_ingredients_from_instructions(tgt_inst)
        
        tgt_method = detect_cooking_method(tgt_inst)
        tgt_protein = detect_protein(title)
        tgt_flavor = _infer_flavor_style(title, tgt_method)
        
        # Calculate comfort level and texture profile for target
        tgt_comfort = detect_comfort_level(title, tgt_inst, tgt_method)
        tgt_texture = detect_texture_profile(title, tgt_inst, tgt_ingredients_extracted)

        target_profile = {
            "method": tgt_method,
            "flavor_vector": tgt_flavor,
            "protein": tgt_protein,
            "ingredients": tgt_ingredients,
            "ingredients_extracted": tgt_ingredients_extracted,
            "instructions": tgt_inst,  # For adaptability calculation
            "comfort_level": tgt_comfort,
            "texture_profile": tgt_texture,
        }

        score, reasons, detailed_metrics = score_recipe(source_profile, target_profile)
        scored.append((score, {"Recipe_title": title, "recipe": recipe, "metrics": detailed_metrics}, reasons))

    if filtered_count > 0:
        print(f"🚫 Filtered out {filtered_count} recipes due to allergens")
    
    print(f"✅ Scored {len(scored)} recipes")

    # Sort by score
    scored.sort(key=lambda x: -x[0])
    
    print(f"\n{'─'*60}")
    print(f"🏆 TOP SCORING RECIPES")
    print(f"{'─'*60}")
    
    # Show top 10 scores for debugging
    for i, (score, data, reasons) in enumerate(scored[:10], 1):
        print(f"{i}. {data['Recipe_title']}")
        print(f"   Overall Score: {score:.3f}")
        
        # Show detailed metrics if available
        if "metrics" in data:
            metrics = data["metrics"]
            print(f"   📊 Metrics:")
            print(f"      Comfort: {metrics.get('comfort_similarity', 0):.0f}% | "
                  f"Flavor: {metrics.get('flavor_similarity', 0):.0f}% | "
                  f"Adaptability: {metrics.get('adaptability', 0):.0f}%")
            print(f"      Texture: {metrics.get('texture_alignment', 0):.0f}% | "
                  f"Ingredients: {metrics.get('ingredient_match', 0):.0f}%")
        
        print(f"   {reasons[0] if reasons else 'No explanation'}")
    
    # ALWAYS return at least 3 recipes
    top_count = min(3, len(scored))
    
    if len(scored) == 0:
        # No recipes passed allergen filter - return top 3 from original list
        print(f"\n⚠️  No recipes passed filters, showing top 3 from region anyway")
        return [
            {
                "recipe_title": r.get("Recipe_title", "Unknown"),
                "final_score": 0.0,
                "explanation": ["No match found after allergen filtering. This is a popular dish in the region."],
                "no_match_fallback": True,
                "recipe_id": r.get("Recipe_id", ""),
                "calories": r.get("Calories", ""),
                "cook_time": r.get("cook_time", ""),
                "prep_time": r.get("prep_time", ""),
                "servings": r.get("servings", ""),
            }
            for r in target_recipes[:3]
        ]
    
    # Build results
    matches = [
        {
            "recipe_title": s[1]["Recipe_title"],
            "final_score": round(s[0], 3),
            "explanation": s[2],
            "recipe_id": s[1]["recipe"].get("Recipe_id", ""),
            "calories": s[1]["recipe"].get("Calories", ""),
            "cook_time": s[1]["recipe"].get("cook_time", ""),
            "prep_time": s[1]["recipe"].get("prep_time", ""),
            "servings": s[1]["recipe"].get("servings", ""),
            # NEW: Detailed similarity metrics for frontend
            "similarity_metrics": s[1].get("metrics", {
                "comfort_similarity": 0.0,
                "flavor_similarity": 0.0,
                "adaptability": 0.0,
                "texture_alignment": 0.0,
                "ingredient_match": 0.0,
            }),
        }
        for s in scored[:top_count]
    ]

    # Check if scores are very low (less than 0.2)
    if matches and matches[0]["final_score"] < 0.2:
        print(f"\n⚠️  Low match scores detected (best: {matches[0]['final_score']:.3f})")
        print(f"   Still showing top {len(matches)} recipes from the region")
        for m in matches:
            m["explanation"].insert(0, "⚠️ Low similarity - but this is a popular dish in the region")
    
    print(f"\n{'='*60}")
    print(f"✅ RETURNING {len(matches)} RECOMMENDATIONS")
    print(f"{'='*60}\n")

    return matches


recommend_recipes_new = recommend_recipes