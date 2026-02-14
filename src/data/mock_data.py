"""
FlavorBridge mock data - Edit this file to change dummy recipes, flavors, allergens, etc.
SINGLE SOURCE OF TRUTH: All app data (Python backend + React UI via API).
"""

# -----------------------------------------------------------------------------
# UI: Cuisines (Home dropdowns)
# -----------------------------------------------------------------------------

COMFORT_CUISINES = [
    "Korean",
    "Indian Subcontinent",
    "Japanese",
    "Italian",
    "Southeast Asian",
    "Middle Eastern",
]

TARGET_CUISINES = [
    "Korean",
    "Indian Subcontinent",
    "Japanese",
    "Italian",
    "Southeast Asian",
    "Middle Eastern",
]

# -----------------------------------------------------------------------------
# UI: Allergens (Allergens page, Profile, Home filter)
# -----------------------------------------------------------------------------

COMMON_ALLERGENS = [
    "papaya",
    "beans",
    "bread",
    "wort",
    "egg",
    "orange",
]

ALLERGEN_SUBSTITUTES = {
    "milk": [{"name": "Oat Milk", "description": "Creamy, neutral flavor"}],
    "garlic": [{"name": "Asafoetida", "description": "Savory depth without garlic"}],
    "egg": [{"name": "Flax Egg", "description": "1 tbsp ground flax + 3 tbsp water"}],
    "beef": [{"name": "Lentils", "description": "Rich, protein-packed substitute"}],
    "walnut": [{"name": "Sunflower Seeds", "description": "Nutty crunch"}],
    "onion": [{"name": "Shallots", "description": "Milder allium option"}],
    "almond": [{"name": "Oat Flour", "description": "Mild, versatile"}],
}

# -----------------------------------------------------------------------------
# UI: User profile & settings (Profile, Settings)
# -----------------------------------------------------------------------------

INITIAL_USER_PROFILE = {
    "name": "Kritika Tripathi",
    "email": "kritik.aaa@gmail.com",
    "joinDate": "December 2025",
    "translationsCompleted": 7,
    "recipesViewed": 19,
    "allergens": [],
    "favoriteCuisines": ["Italian", "Japanese", "Indian"],
}

INITIAL_SETTINGS = {
    "notifications": False,
    "showCalories": True,
}

# -----------------------------------------------------------------------------
# UI: Restaurants
# -----------------------------------------------------------------------------

MOCK_RESTAURANTS = [
    {
        "id": 1,
        "name": "Coffee House",
        "cuisine": "Indian",
        "price": "$",
        "matchScore": 95,
        "distance": "0.5 km",
        "rating": "4.6",
    },
    {
        "id": 2,
        "name": "Sandhu Kitchen",
        "cuisine": "Indian",
        "price": "$",
        "matchScore": 92,
        "distance": "4.5 km",
        "rating": "4.8",
    },
    {
        "id": 3,
        "name": "Moti Mahal",
        "cuisine": "Indian",
        "price": "$$$",
        "matchScore": 88,
        "distance": "0.76 km",
        "rating": "4.3",
    },
    {
        "id": 4,
        "name": "Shahi Haveli",
        "cuisine": "Indian",
        "price": "$$",
        "matchScore": 86,
        "distance": "3.2 km",
        "rating": "4.5",
    },
    {
        "id": 5,
        "name": "Dum Pukht",
        "cuisine": "Indian",
        "price": "$$",
        "matchScore": 83,
        "distance": "6.3 km",
        "rating": "4.8",
    },
    {
        "id": 6,
        "name": "Singh Dhaba",
        "cuisine": "Indian",
        "price": "$$",
        "matchScore": 78,
        "distance": "1.7 km",
        "rating": "4.0",
    },
]

# mock_recipes.py

MOCK_RECIPES = {
    "chinese_and_mongolian": [
        {
            "id": "C001",
            "title": "Chinese-Style Broccoli Salad",
            "calories": 188.0,
            "prep_time": 0,
            "cook_time": 0,
            "total_time": 0,
            "servings": 4,
            "region": "Chinese and Mongolian",
            "continent": "Asian"
        },
        {
            "id": "C002",
            "title": "Chinese Green Bean Stir-Fry",
            "calories": 107.0,
            "prep_time": 20,
            "cook_time": 15,
            "total_time": 35,
            "servings": 40,
            "region": "Chinese and Mongolian",
            "continent": "Asian"
        }
    ],

    "korean": [
        {
            "id": "K001",
            "title": "Spicy Cabbage Kimchi",
            "calories": 12.0,
            "prep_time": 60,
            "cook_time": 0,
            "total_time": 60,
            "servings": 56,
            "region": "Korean",
            "continent": "Asian"
        },
        {
            "id": "K002",
            "title": "Gochujang Sauce",
            "calories": 38.0,
            "prep_time": 0,
            "cook_time": 0,
            "total_time": 0,
            "servings": 4,
            "region": "Korean",
            "continent": "Asian"
        }
    ],

    "italian": [
        {
            "id": "I001",
            "title": "Judy's Hearty Vegetable Minestrone Soup",
            "calories": 217.0,
            "prep_time": 20,
            "cook_time": 60,
            "total_time": 80,
            "servings": 6,
            "region": "Italian",
            "continent": "European"
        },
        {
            "id": "I002",
            "title": "Italian Zucchini Saute",
            "calories": 288.0,
            "prep_time": 15,
            "cook_time": 15,
            "total_time": 30,
            "servings": 4,
            "region": "Italian",
            "continent": "European"
        }
    ],
    "thai_chicken_curries": [
        {
            "id": "3202",
            "title": "Thai Chicken Curry in Coconut Milk",
            "calories": 269.0,
            "prep_time": 25,
            "cook_time": 10,
            "total_time": 35,
            "servings": 4,
            "region": "Thai",
            "continent": "Asian"
        },
        {
            "id": "3245",
            "title": "Thai Chicken Curry with Pineapple",
            "calories": 409.0,
            "prep_time": 25,
            "cook_time": 35,
            "total_time": 60,
            "servings": 4,
            "region": "Thai",
            "continent": "Asian"
        },
        {
            "id": "3296",
            "title": "Thai Red Chicken Curry",
            "calories": 271.0,
            "prep_time": 10,
            "cook_time": 10,
            "total_time": 20,
            "servings": 4,
            "region": "Thai",
            "continent": "Asian"
        }
    ],

    "lentil_soups": [
        {
            "id": "2683",
            "title": "Moroccan Lentil Soup with Veggies",
            "calories": 390.0,
            "prep_time": 15,
            "cook_time": 60,
            "total_time": 75,
            "servings": 7,
            "region": "Northern Africa",
            "continent": "African"
        },
        {
            "id": "2610",
            "title": "Egyptian Lentil Soup",
            "calories": 196.0,
            "prep_time": 15,
            "cook_time": 30,
            "total_time": 45,
            "servings": 4,
            "region": "Middle Eastern",
            "continent": "African"
        },
        {
            "id": "4853",
            "title": "Turkish Red Lentil Soup with Mint",
            "calories": 168.0,
            "prep_time": 15,
            "cook_time": 45,
            "total_time": 60,
            "servings": 6,
            "region": "Middle Eastern",
            "continent": "Asian"
        }
    ],

    "biryani": [
        {
            "id": "4018",
            "title": "Vegetable Biryani",
            "calories": 277.0,
            "prep_time": 10,
            "cook_time": 20,
            "total_time": 30,
            "servings": 4,
            "region": "Indian Subcontinent",
            "continent": "Asian"
        },
        {
            "id": "51478",
            "title": "Vegetable Biryani (South Africa)",
            "calories": 383.9,
            "prep_time": 0,
            "cook_time": 0,
            "total_time": 80,
            "servings": 12,
            "region": "Rest Africa",
            "continent": "African"
        },
        {
            "id": "65701",
            "title": "Chicken and Vegetable Biryani",
            "calories": 429.9,
            "prep_time": 0,
            "cook_time": 0,
            "total_time": 75,
            "servings": 6,
            "region": "Indian Subcontinent",
            "continent": "Asian"
        }
    ]
}

# mock_recipes_extended.py

MOCK_RECIPES = {
    "chinese_and_mongolian": [
        {
            "title": "Chinese-Style Broccoli Salad",
            "calories": 188.0,
            "prep_time": 0,
            "cook_time": 0,
            "servings": 4,
            "region": "Chinese and Mongolian",
            "continent": "Asian",
            "processes": ["separate", "peel", "boil", "add", "boil"],
            "diet": {
                "vegan": True,
                "pescetarian": True,
                "ovo_vegetarian": False,
                "lacto_vegetarian": False,
                "ovo_lacto_vegetarian": False
            }
        },
        {
            "title": "Chinese Green Bean Stir-Fry",
            "calories": 107.0,
            "prep_time": 20,
            "cook_time": 15,
            "servings": 40,
            "region": "Chinese and Mongolian",
            "continent": "Asian",
            "processes": ["heat", "stir", "cook", "season"],
            "diet": {
                "vegan": True,
                "pescetarian": True,
                "ovo_vegetarian": False,
                "lacto_vegetarian": False,
                "ovo_lacto_vegetarian": False
            }
        }
    ],

    "korean": [
        {
            "title": "Spicy Cabbage Kimchi",
            "calories": 12.0,
            "prep_time": 60,
            "cook_time": 0,
            "servings": 56,
            "region": "Korean",
            "continent": "Asian",
            "processes": [
                "cut", "rinse", "sprinkle", "seal",
                "drain", "squeeze", "stir", "cool", "refrigerate"
            ],
            "diet": {
                "vegan": True,
                "pescetarian": True,
                "ovo_vegetarian": False,
                "lacto_vegetarian": False,
                "ovo_lacto_vegetarian": False
            }
        },
        {
            "title": "Gochujang Sauce",
            "calories": 38.0,
            "prep_time": 0,
            "cook_time": 0,
            "servings": 4,
            "region": "Korean",
            "continent": "Asian",
            "processes": ["whisk", "smooth"],
            "diet": {
                "vegan": True,
                "pescetarian": True,
                "ovo_vegetarian": False,
                "lacto_vegetarian": False,
                "ovo_lacto_vegetarian": False
            }
        }
    ],

    "italian": [
        {
            "title": "Judy's Hearty Vegetable Minestrone Soup",
            "calories": 217.0,
            "prep_time": 20,
            "cook_time": 60,
            "servings": 6,
            "region": "Italian",
            "continent": "European",
            "processes": ["heat", "cook", "stir", "season", "simmer", "add"],
            "diet": {
                "vegan": True,
                "pescetarian": True,
                "ovo_vegetarian": False,
                "lacto_vegetarian": False,
                "ovo_lacto_vegetarian": False
            }
        },
        {
            "title": "Italian Zucchini Saute",
            "calories": 288.0,
            "prep_time": 15,
            "cook_time": 15,
            "servings": 4,
            "region": "Italian",
            "continent": "European",
            "processes": ["heat", "stir", "cook", "mix", "season", "taste"],
            "diet": {
                "vegan": True,
                "pescetarian": True,
                "ovo_vegetarian": False,
                "lacto_vegetarian": False,
                "ovo_lacto_vegetarian": False
            }
        }
    ]
}

INSTRUCTIONS = {
    "C001": {
        "recipe_id": "C001",
        "steps": [
            "separate the broccoli into florets",
            "peel and prepare remaining vegetables",
            "boil water in a pot",
            "add broccoli and cook briefly until tender",
            "drain and let cool",
            "combine with dressing ingredients",
            "toss well",
            "serve chilled or at room temperature"
        ]
    },

    "C002": {
        "recipe_id": "C002",
        "steps": [
            "wash and trim green beans",
            "heat oil in a wok over high heat",
            "add green beans and stir-fry",
            "cook until slightly blistered",
            "season with sauce and spices",
            "stir well to coat evenly",
            "remove from heat",
            "serve hot"
        ]
    },

    "K001": {
        "recipe_id": "K001",
        "steps": [
            "cut cabbage into large pieces",
            "rinse thoroughly and drain",
            "sprinkle salt over cabbage and let stand",
            "drain excess liquid",
            "mix with seasoning ingredients",
            "pack tightly into a container",
            "seal and refrigerate",
            "serve chilled"
        ]
    },

    "K002": {
        "recipe_id": "K002",
        "steps": [
            "combine all sauce ingredients in a bowl",
            "whisk until smooth",
            "taste and adjust seasoning",
            "transfer to a container",
            "cover tightly",
            "store in the refrigerator",
            "use as needed"
        ]
    },

    "I001": {
        "recipe_id": "I001",
        "steps": [
            "heat oil in a large pot over medium heat",
            "add vegetables and cook until softened",
            "stir occasionally to prevent sticking",
            "add seasoning and broth",
            "bring to a boil",
            "reduce heat and simmer",
            "cook until vegetables are tender",
            "serve hot"
        ]
    },

    "I002": {
        "recipe_id": "I002",
        "steps": [
            "slice zucchini evenly",
            "heat oil in a pan over medium heat",
            "add zucchini and stir frequently",
            "cook until lightly browned",
            "season with salt and herbs",
            "taste and adjust seasoning",
            "remove from heat",
            "serve warm"
        ]
    }
}

# Backend: flavor_bridge lookup maps
METHOD_KEYWORDS = {
    "slow_saucy": ["simmer", "reduce", "cook", "boil", "stew"],
    "stir_fry": ["stir", "sizzle", "toss", "heat"],
    "roast_bake": ["bake", "roast"],
    "raw_mix": ["mix", "season", "whisk"],
    "fry": ["fry", "deep fry"],
}
PROTEIN_MAP = {
    "chicken": ["chicken"],
    "seafood": ["fish", "shrimp", "prawn"],
    "red_meat": ["beef", "lamb", "mutton"],
    "plant_protein": ["lentil", "bean", "chickpea", "soy", "vegetable"],
    "mushroom": ["mushroom"],
}
ALLERGEN_KEYWORDS_BACKEND = {
    "dairy": ["milk", "cream", "cheese", "butter"],
    "nuts": ["peanut", "almond", "cashew"],
    "seafood": ["fish", "shrimp", "prawn"],
    "soy": ["soy", "soybean"],
}
MOCK_FOOD_PAIR = {
    "entityId": "chicken",
    "topSimilarEntities": [
        {"entityName": "Tomato", "category": "Vegetable Fruit", "similarMolecules": 146},
        {"entityName": "Mushroom", "category": "Fungus", "similarMolecules": 144},
        {"entityName": "Cheese", "category": "Dairy", "similarMolecules": 142},
    ],
}
RECIPE_FLAVOR_PROFILES = {"default": {"content": [{"flavor_profile": "savory", "functional_groups": "umami"}]}}

