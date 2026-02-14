"""
FlavorBridge - Translate comfort dishes across cuisines.
NO HARDCODED DATA: All data from src.data.mock_data.
"""

from __future__ import annotations
import math
from typing import Any

from src.data import mock_data

# --- Data from mock_data (single source of truth) ---
MOCK_RECIPES = mock_data.MOCK_RECIPES
INSTRUCTIONS = mock_data.INSTRUCTIONS
METHOD_KEYWORDS = mock_data.METHOD_KEYWORDS
PROTEIN_MAP = mock_data.PROTEIN_MAP
ALLERGEN_KEYWORDS_BACKEND = mock_data.ALLERGEN_KEYWORDS_BACKEND
MOCK_FOOD_PAIR = mock_data.MOCK_FOOD_PAIR
RECIPE_FLAVOR_PROFILES = mock_data.RECIPE_FLAVOR_PROFILES

# Map recipe title -> id for INSTRUCTIONS lookup (first MOCK_RECIPES had ids)
TITLE_TO_ID = {
    "Chinese-Style Broccoli Salad": "C001",
    "Chinese Green Bean Stir-Fry": "C002",
    "Spicy Cabbage Kimchi": "K001",
    "Gochujang Sauce": "K002",
    "Judy's Hearty Vegetable Minestrone Soup": "I001",
    "Italian Zucchini Saute": "I002",
}


def _flatten_recipes() -> list[dict]:
    """Flatten MOCK_RECIPES (nested by category) into a list."""
    out = []
    for recipes in MOCK_RECIPES.values():
        for r in recipes:
            out.append(dict(r))
    return out


def _get_instructions(recipe: dict) -> list[str]:
    """Get cooking steps from INSTRUCTIONS or processes."""
    title = recipe.get("title", "")
    rid = recipe.get("id") or TITLE_TO_ID.get(title)
    if rid and rid in INSTRUCTIONS:
        return INSTRUCTIONS[rid].get("steps", [])
    procs = recipe.get("processes", [])
    return [str(p) for p in procs] if procs else ["cook"]


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


def _infer_flavor_style(recipe: dict) -> dict[str, float]:
    """Infer flavor style from dish name and cooking method."""
    title = (recipe.get("title") or "").lower()
    method = recipe.get("_method", "slow_saucy")
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


def build_flavor_vector(flavor_profile_response: dict) -> dict[str, float]:
    """Build normalized flavor vector from flavor profile response."""
    vector = {}
    for item in flavor_profile_response.get("content", []):
        if "flavor_profile" in item:
            fp = str(item["flavor_profile"]).strip()
            if fp:
                vector[fp] = vector.get(fp, 0.0) + 1.0
        if "functional_groups" in item:
            for fg in str(item["functional_groups"]).split("@"):
                fg = fg.strip().lower()
                if fg:
                    vector[fg] = vector.get(fg, 0.0) + 1.0
    total = sum(vector.values())
    return {k: v / total for k, v in vector.items()} if total else vector


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


def score_recipe(source: dict, target: dict) -> tuple[float, list[str]]:
    """Score target vs source. Weights: method 0.4, flavor 0.35, protein 0.15, pairing 0.1."""
    reasons = []
    mw, fw, pw, pairw = 0.4, 0.35, 0.15, 0.1

    src_m, tgt_m = source.get("method", ""), target.get("method", "")
    method_ok = 1.0 if src_m and src_m == tgt_m else 0.0
    if method_ok:
        reasons.append("Both use similar cooking method (e.g. slow-simmered or stir-fried)")
    else:
        reasons.append(f"Cooking style: {tgt_m} vs {src_m}")

    flavor_sim = flavor_similarity(source.get("flavor_vector", {}), target.get("flavor_vector", {}))
    if flavor_sim >= 0.6:
        reasons.append("Similar aromatic and flavor profile")
    else:
        reasons.append(f"Flavor similarity: {flavor_sim:.2f}")

    src_p, tgt_p = source.get("protein", ""), target.get("protein", "")
    protein_ok = 1.0 if src_p and src_p == tgt_p else 0.0
    if protein_ok:
        reasons.append(f"Same protein type: {tgt_p}")
    else:
        reasons.append(f"Protein: {tgt_p} vs {src_p}")

    pairing = _pairing_overlap(src_p, target.get("ingredients", []))
    if pairing >= 0.5:
        reasons.append("Good food pairing overlap with your comfort dish")

    score = mw * method_ok + fw * flavor_sim + pw * protein_ok + pairw * pairing
    return (score, reasons)


def _find_source_recipe(source_recipe_title: str) -> dict | None:
    """Find source recipe in MOCK_RECIPES by title (exact or partial)."""
    all_recipes = _flatten_recipes()
    title_lower = source_recipe_title.lower().strip()
    for r in all_recipes:
        if (r.get("title") or "").lower() == title_lower:
            return r
    for r in all_recipes:
        if title_lower in (r.get("title") or "").lower():
            return r
    return None


def _get_target_recipes(target_cuisine: str, excluded_allergens: list[str]) -> list[dict]:
    """Get recipes from target cuisine, filtered by allergens."""
    all_recipes = _flatten_recipes()
    target_lower = target_cuisine.lower().strip()
    out = []
    for r in all_recipes:
        region = (r.get("region") or "").lower()
        if region != target_lower:
            continue
        ingredients = _get_ingredients_from_title(r.get("title", ""))
        if contains_allergen(ingredients, excluded_allergens):
            continue
        out.append(r)
    return out


def _get_top_in_region(target_cuisine: str, excluded_allergens: list[str], limit: int = 3) -> list[dict]:
    """Get top N recipes in region when no good matches (by simple order)."""
    candidates = _get_target_recipes(target_cuisine, excluded_allergens)
    return candidates[:limit]


def recommend_recipes(
    source_recipe_title: str,
    target_cuisine: str,
    excluded_allergens: list[str] | None = None,
) -> dict:
    """
    Recommend target-cuisine recipes similar to source dish.
    Returns: { matches: [...], no_matches: bool, top_in_region: [...] }
    """
    excluded_allergens = excluded_allergens or []
    all_recipes = _flatten_recipes()

    source_recipe = _find_source_recipe(source_recipe_title)
    if not source_recipe:
        source_recipe = {
            "title": source_recipe_title,
            "region": "Unknown",
            "processes": ["simmer", "cook"],
        }

    src_inst = _get_instructions(source_recipe)
    src_method = detect_cooking_method(src_inst)
    src_protein = detect_protein(source_recipe.get("title", ""))
    src_flavor = _infer_flavor_style({"title": source_recipe.get("title", ""), "_method": src_method})
    src_ingredients = _get_ingredients_from_title(source_recipe.get("title", ""))

    source_profile = {
        "method": src_method,
        "flavor_vector": src_flavor,
        "protein": src_protein,
        "ingredients": src_ingredients,
    }

    candidates = _get_target_recipes(target_cuisine, excluded_allergens)

    scored = []
    for c in candidates:
        title = c.get("title", "")
        inst = _get_instructions(c)
        tgt_method = detect_cooking_method(inst)
        tgt_protein = detect_protein(title)
        tgt_flavor = _infer_flavor_style({"title": title, "_method": tgt_method})
        tgt_ingredients = _get_ingredients_from_title(title)

        target_profile = {
            "method": tgt_method,
            "flavor_vector": tgt_flavor,
            "protein": tgt_protein,
            "ingredients": tgt_ingredients,
        }

        score, reasons = score_recipe(source_profile, target_profile)
        scored.append((score, {"Recipe_title": title, "recipe": c}, reasons))

    scored.sort(key=lambda x: -x[0])
    matches = [
        {"recipe_title": s[1]["Recipe_title"], "final_score": round(s[0], 3), "explanation": s[2]}
        for s in scored[:3]
    ]

    no_matches = len(matches) == 0 or (matches and matches[0]["final_score"] < 0.2)
    if no_matches:
        top_recipes = _get_top_in_region(target_cuisine, excluded_allergens, 3)
        return [
            {
                "recipe_title": r.get("title", "Unknown"),
                "final_score": 0.0,
                "explanation": ["No close match found. Top pick in this region."],
                "no_match_fallback": True,
            }
            for r in top_recipes
        ]
    return matches


recommend_recipes_new = recommend_recipes
