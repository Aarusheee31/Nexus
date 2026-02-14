

export const COMFORT_CUISINES = [
  'Southeast Asian', 
  'American', 
  'Italian', 
  'Chinese', 
  'Mexican', 
  'Japanese', 
  'Thai', 
  'French', 
  'Mediterranean'
];

export const TARGET_CUISINES = [
  'Indian', 
  'Thai', 
  'Vietnamese', 
  'Korean', 
  'Ethiopian', 
  'Moroccan', 
  'Lebanese', 
  'Turkish', 
  'Peruvian', 
  'South Indian'
];

export const COMMON_ALLERGENS = [
  'Peanuts', 
  'Tree Nuts', 
  'Milk', 
  'Eggs', 
  'Soy', 
  'Wheat', 
  'Fish', 
  'Shellfish', 
  'Sesame'
];

export const ALLERGEN_SUBSTITUTES = {
  'Peanuts': [
    { name: 'Sunflower Seed Butter', description: 'Creamy alternative with similar texture' },
    { name: 'Soy Nut Butter', description: 'Protein-rich substitute' },
    { name: 'Coconut Butter', description: 'Mild, slightly sweet option' }
  ],
  'Tree Nuts': [
    { name: 'Seeds (Sunflower, Pumpkin)', description: 'Crunchy texture, similar nutrition' },
    { name: 'Oat Flour', description: 'For baking applications' },
    { name: 'Pretzels', description: 'For crunch in recipes' }
  ],
  'Milk': [
    { name: 'Oat Milk', description: 'Creamy, neutral flavor' },
    { name: 'Almond Milk', description: 'Light, slightly nutty' },
    { name: 'Coconut Milk', description: 'Rich, great for cooking' },
    { name: 'Cashew Cream', description: 'Perfect for sauces' }
  ],
  'Eggs': [
    { name: 'Flax Eggs', description: '1 tbsp flax + 3 tbsp water per egg' },
    { name: 'Chia Seeds', description: 'Similar binding properties' },
    { name: 'Applesauce', description: '¼ cup per egg for baking' },
    { name: 'Aquafaba', description: 'Chickpea liquid, great for meringues' }
  ],
  'Soy': [
    { name: 'Coconut Aminos', description: 'Soy sauce alternative' },
    { name: 'Pea Protein', description: 'Protein powder substitute' },
    { name: 'Sunflower Lecithin', description: 'Emulsifier alternative' }
  ],
  'Wheat': [
    { name: 'Rice Flour', description: 'Versatile gluten-free option' },
    { name: 'Almond Flour', description: 'Nutty, protein-rich' },
    { name: 'Coconut Flour', description: 'High fiber, absorbs moisture' },
    { name: 'Chickpea Flour', description: 'Great for savory dishes' }
  ],
  'Fish': [
    { name: 'Seaweed/Nori', description: 'For oceanic flavor' },
    { name: 'Hearts of Palm', description: 'Texture similar to crab' },
    { name: 'Jackfruit', description: 'Flaky texture' }
  ],
  'Shellfish': [
    { name: 'Mushrooms (King Oyster)', description: 'Meaty texture' },
    { name: 'Artichoke Hearts', description: 'Similar to lobster texture' },
    { name: 'Banana Blossom', description: 'Flaky, fish-like' }
  ],
  'Sesame': [
    { name: 'Tahini Alternatives (Sunflower)', description: 'Similar creamy texture' },
    { name: 'Hemp Seeds', description: 'Nutty flavor' },
    { name: 'Poppy Seeds', description: 'Visual substitute' }
  ]
};

export const MOCK_RESTAURANTS = [
  { 
    id: 1, 
    name: 'Spice Haven', 
    cuisine: 'Indian', 
    distance: '0.5 mi', 
    rating: 4.5, 
    price: '$$', 
    matchScore: 92, 
    image: '🍛' 
  },
  { 
    id: 2, 
    name: 'Golden Curry House', 
    cuisine: 'Thai', 
    distance: '0.8 mi', 
    rating: 4.7, 
    price: '$$$', 
    matchScore: 88, 
    image: '🍜' 
  },
  { 
    id: 3, 
    name: 'Tandoori Palace', 
    cuisine: 'Indian', 
    distance: '1.2 mi', 
    rating: 4.3, 
    price: '$$', 
    matchScore: 85, 
    image: '🥘' 
  },
  { 
    id: 4, 
    name: 'Bangkok Street Kitchen', 
    cuisine: 'Thai', 
    distance: '1.5 mi', 
    rating: 4.6, 
    price: '$$', 
    matchScore: 82, 
    image: '🍲' 
  },
  { 
    id: 5, 
    name: 'Masala Magic', 
    cuisine: 'Indian', 
    distance: '2.1 mi', 
    rating: 4.4, 
    price: '$', 
    matchScore: 79, 
    image: '🍛' 
  }
];

export const MOCK_RECIPES = {
  'Butter Chicken': {
    name: 'Butter Chicken (Murgh Makhani)',
    image: '🍗',
    prepTime: '20 min',
    cookTime: '40 min',
    servings: 4,
    difficulty: 'Medium',
    cuisine: 'Indian',
    ingredients: [
      '500g chicken breast, cubed',
      '1 cup yogurt',
      '2 tbsp ginger-garlic paste',
      '1 cup tomato puree',
      '1/2 cup heavy cream',
      '3 tbsp butter',
      '1 tsp garam masala',
      '1 tsp red chili powder',
      'Fresh cilantro for garnish'
    ],
    instructions: [
      'Marinate chicken in yogurt, ginger-garlic paste, and spices for 30 minutes',
      'Heat butter in a pan and cook marinated chicken until golden',
      'Add tomato puree and simmer for 15 minutes',
      'Stir in heavy cream and garam masala',
      'Cook for another 5-7 minutes until thick',
      'Garnish with fresh cilantro and serve with naan or rice'
    ]
  },
  'Pad Thai': {
    name: 'Authentic Pad Thai',
    image: '🍝',
    prepTime: '15 min',
    cookTime: '15 min',
    servings: 2,
    difficulty: 'Easy',
    cuisine: 'Thai',
    ingredients: [
      '200g rice noodles',
      '2 eggs',
      '200g shrimp or tofu',
      '3 tbsp tamarind paste',
      '2 tbsp fish sauce',
      '1 tbsp palm sugar',
      'Bean sprouts',
      'Peanuts, crushed',
      'Lime wedges'
    ],
    instructions: [
      'Soak rice noodles in warm water for 30 minutes',
      'Heat oil in wok, scramble eggs and set aside',
      'Stir-fry protein until cooked',
      'Add drained noodles and sauce mixture',
      'Toss everything together for 2-3 minutes',
      'Serve topped with peanuts, bean sprouts, and lime'
    ]
  },
  'Sambar Rice': {
    name: 'Sambar Rice',
    image: '🍚',
    prepTime: '15 min',
    cookTime: '30 min',
    servings: 4,
    difficulty: 'Easy',
    cuisine: 'South Indian',
    ingredients: [
      '1 cup rice',
      '1/2 cup toor dal',
      '2 cups mixed vegetables',
      '2 tbsp sambar powder',
      '1 tbsp tamarind paste',
      'Curry leaves',
      'Mustard seeds',
      '2 dried red chilies',
      'Salt to taste'
    ],
    instructions: [
      'Cook rice and dal separately',
      'Prepare sambar with vegetables, tamarind, and spices',
      'Mix cooked rice with sambar',
      'Temper with mustard seeds, curry leaves, and chilies',
      'Simmer for 5 minutes',
      'Serve hot with papad'
    ]
  }
};

export const INITIAL_USER_PROFILE = {
  name: 'Shreya Tripathi',
  email: 'shrey.aaa@gmail.com',
  joinDate: 'December 2025',
  allergens: [],
  favoriteCuisines: ['Indian', 'Mexican', 'Italian'],
  translationsCompleted: 12,
  recipesViewed: 52
};

export const INITIAL_SETTINGS = {
  spiceLevel: 'Medium',
  dietaryPreference: 'None',
  notifications: true,
  showNutrition: true,
  autoDetectLocation: true,
  language: 'English'
};

export const MOCK_MATCH_RESULTS = [
  {
    id: 1,
    name: 'Sambar Rice',
    matchScore: 92,
    explanation: 'Shares warm lentils, aromatic spices, and savory depth with your comfort dish',
    ingredients: ['Lentils', 'Turmeric', 'Cumin', 'Curry Leaves'],
    hasRecipe: true,
    image: '🍚'
  },
  {
    id: 2,
    name: 'Bisi Bele Bath',
    matchScore: 87,
    explanation: 'Similar comfort food profile with rice, lentils, and warming spices',
    ingredients: ['Rice', 'Lentils', 'Tamarind', 'Mixed Spices'],
    hasRecipe: false,
    image: '🍛'
  },
  {
    id: 3,
    name: 'Curd Rice',
    matchScore: 83,
    explanation: 'Mild, comforting rice dish with cooling properties and subtle spices',
    ingredients: ['Rice', 'Yogurt', 'Tempering', 'Curry Leaves'],
    hasRecipe: false,
    image: '🍚'
  }
];
