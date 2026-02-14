import React, { useState, useEffect } from 'react';
import { Menu, UtensilsCrossed } from 'lucide-react';
import Sidebar from './components/Sidebar';
import Home from './pages/Home';
import Results from './pages/Results';
import Recipes from './pages/Recipes';
import RecipeDetail from './pages/RecipeDetail';
import Restaurants from './pages/Restaurants';
import Allergens from './pages/Allergens';
import Profile from './pages/Profile';
import Settings from './pages/Settings';
import './App.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

function transformResults(raw, recipes) {
  return raw.map((r, i) => ({
    id: i + 1,
    name: r.recipe_title,
    image: '🍽️',
    matchScore: Math.round(r.final_score * 100),
    explanation: Array.isArray(r.explanation) ? r.explanation.join(' • ') : r.explanation,
    ingredients: recipes[r.recipe_title]?.ingredients ?? [],
    hasRecipe: !!recipes[r.recipe_title],
  }));
}

function App() {
  const [currentScreen, setCurrentScreen] = useState('home');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [dataLoading, setDataLoading] = useState(true);
  const [dataError, setDataError] = useState(null);

  const [comfortCuisines, setComfortCuisines] = useState([]);
  const [targetCuisines, setTargetCuisines] = useState([]);
  const [recipes, setRecipes] = useState({});
  const [restaurants, setRestaurants] = useState([]);
  const [commonAllergens, setCommonAllergens] = useState([]);
  const [allergenSubstitutes, setAllergenSubstitutes] = useState({});

  const [comfortCuisine, setComfortCuisine] = useState('');
  const [comfortDish, setComfortDish] = useState('');
  const [targetCuisine, setTargetCuisine] = useState('');
  const [allergenFilter, setAllergenFilter] = useState(false);

  const [matchResults, setMatchResults] = useState([]);
  const [animateProgress, setAnimateProgress] = useState(false);
  const [translateLoading, setTranslateLoading] = useState(false);
  const [translateError, setTranslateError] = useState(null);

  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [selectedAllergens, setSelectedAllergens] = useState([]);
  const [userProfile, setUserProfile] = useState({ allergens: [], favoriteCuisines: [] });
  const [settings, setSettings] = useState({});

  useEffect(() => {
    fetch(`${API_BASE}/api/data`)
      .then((res) => res.json())
      .then((data) => {
        setComfortCuisines(data.comfortCuisines ?? []);
        setTargetCuisines(data.targetCuisines ?? []);
        setRecipes(data.recipes ?? {});
        setRestaurants(data.restaurants ?? []);
        setCommonAllergens(data.commonAllergens ?? []);
        setAllergenSubstitutes(data.allergenSubstitutes ?? {});
        setUserProfile(data.initialUserProfile ?? {});
        setSettings(data.initialSettings ?? {});
      })
      .catch(() => setDataError("Start the Python API: run 'python api.py' in a terminal"))
      .finally(() => setDataLoading(false));
  }, []);

  const handleTranslate = async () => {
    setTranslateLoading(true);
    setTranslateError(null);
    const excluded = allergenFilter ? selectedAllergens : [];
    try {
      const res = await fetch(`${API_BASE}/api/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          comfortDish: comfortDish,
          targetCuisine: targetCuisine,
          excludedAllergens: excluded,
        }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || `API error ${res.status}`);
      }
      const raw = await res.json();
      const results = transformResults(raw, recipes);
      setMatchResults(results);
      setAnimateProgress(false);
      setCurrentScreen('results');
      setSidebarOpen(false);
    } catch (err) {
      const msg = err.message || 'Failed to fetch';
      setTranslateError(
        msg.toLowerCase().includes('fetch')
          ? "Start the Python API: run 'python api.py' in a terminal"
          : msg
      );
    } finally {
      setTranslateLoading(false);
    }
  };

  const handleViewRecipe = (recipeName) => {
    setSelectedRecipe(recipes[recipeName]);
    setCurrentScreen('recipe-detail');
  };

  const handleSelectRecipe = (recipe) => {
    setSelectedRecipe(recipe);
    setCurrentScreen('recipe-detail');
  };

  const toggleAllergen = (allergen) => {
    setSelectedAllergens(prev => 
      prev.includes(allergen) 
        ? prev.filter(a => a !== allergen)
        : [...prev, allergen]
    );
  };

  const addUserAllergen = (allergen) => {
    if (!userProfile.allergens.includes(allergen)) {
      setUserProfile(prev => ({
        ...prev,
        allergens: [...prev.allergens, allergen]
      }));
    }
  };

  const removeUserAllergen = (allergen) => {
    setUserProfile(prev => ({
      ...prev,
      allergens: prev.allergens.filter(a => a !== allergen)
    }));
  };

  const updateSettings = (newSettings) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
  };

  if (dataLoading) return <div className="app-container" style={{ padding: 40, textAlign: 'center' }}>Loading...</div>;
  if (dataError) return <div className="app-container" style={{ padding: 40, textAlign: 'center', color: '#e74c3c' }}>{dataError}</div>;

  return (
    <div className="app-container">
      <Sidebar 
        currentScreen={currentScreen}
        setCurrentScreen={setCurrentScreen}
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
      />
      
      <div className="main-wrapper">
        {/* Mobile header */}
        <div className="mobile-header">
          <button
            onClick={() => setSidebarOpen(true)}
            className="menu-button"
          >
            <Menu size={24} />
          </button>
          <div className="mobile-logo">
            <UtensilsCrossed size={24} />
            <span>PalatePal</span>
          </div>
          <div className="mobile-spacer" />
        </div>

        {/* Main content */}
        <div className="main-content">
          <div className="content-wrapper">
            {currentScreen === 'home' && (
              <Home 
                comfortCuisines={comfortCuisines}
                targetCuisines={targetCuisines}
                comfortCuisine={comfortCuisine}
                setComfortCuisine={setComfortCuisine}
                comfortDish={comfortDish}
                setComfortDish={setComfortDish}
                targetCuisine={targetCuisine}
                setTargetCuisine={setTargetCuisine}
                allergenFilter={allergenFilter}
                setAllergenFilter={setAllergenFilter}
                onTranslate={handleTranslate}
                loading={translateLoading}
                error={translateError}
              />
            )}
            
            {currentScreen === 'results' && (
              <Results 
                matchResults={matchResults}
                comfortDish={comfortDish}
                animateProgress={animateProgress}
                setAnimateProgress={setAnimateProgress}
                onViewRecipe={handleViewRecipe}
                onBack={() => setCurrentScreen('home')}
              />
            )}
            
            {currentScreen === 'recipes' && (
              <Recipes 
                recipes={recipes}
                onSelectRecipe={handleSelectRecipe}
              />
            )}
            
            {currentScreen === 'recipe-detail' && (
              <RecipeDetail 
                recipe={selectedRecipe}
                onBack={() => setCurrentScreen(matchResults.length > 0 ? 'results' : 'recipes')}
              />
            )}
            
            {currentScreen === 'restaurants' && (
              <Restaurants restaurants={restaurants} />
            )}
            
            {currentScreen === 'allergens' && (
              <Allergens 
                commonAllergens={commonAllergens}
                allergenSubstitutes={allergenSubstitutes}
                selectedAllergens={selectedAllergens}
                toggleAllergen={toggleAllergen}
              />
            )}
            
            {currentScreen === 'profile' && (
              <Profile 
                userProfile={userProfile}
                commonAllergens={commonAllergens}
                addAllergen={addUserAllergen}
                removeAllergen={removeUserAllergen}
              />
            )}
            
            {currentScreen === 'settings' && (
              <Settings 
                settings={settings}
                updateSettings={updateSettings}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
