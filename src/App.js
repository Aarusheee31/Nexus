import React, { useState } from 'react';
import { Utensils, Menu } from 'lucide-react';
import Sidebar from './components/Sidebar';
import Home from './pages/Home';
import Results from './pages/Results';
import Recipes from './pages/Recipes';
import RecipeDetail from './pages/RecipeDetail';
import Restaurants from './pages/Restaurants';
import Allergens from './pages/Allergens';
import Profile from './pages/Profile';
import Settings from './pages/Settings';
import { MOCK_MATCH_RESULTS, MOCK_RECIPES, INITIAL_USER_PROFILE, INITIAL_SETTINGS } from './data/mockData';
import './App.css';

function App() {
  const [currentScreen, setCurrentScreen] = useState('home');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  // Home screen state
  const [comfortCuisine, setComfortCuisine] = useState('');
  const [comfortDish, setComfortDish] = useState('');
  const [targetCuisine, setTargetCuisine] = useState('');
  const [allergenFilter, setAllergenFilter] = useState(false);
  
  // Results state
  const [matchResults, setMatchResults] = useState([]);
  const [animateProgress, setAnimateProgress] = useState(false);
  
  // Recipe state
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  
  // Allergens state
  const [selectedAllergens, setSelectedAllergens] = useState([]);
  
  // Profile state
  const [userProfile, setUserProfile] = useState(INITIAL_USER_PROFILE);
  
  // Settings state
  const [settings, setSettings] = useState(INITIAL_SETTINGS);

  const handleTranslate = () => {
    setMatchResults(MOCK_MATCH_RESULTS);
    setAnimateProgress(false);
    setCurrentScreen('results');
    setSidebarOpen(false);
  };

  const handleViewRecipe = (recipeName) => {
    setSelectedRecipe(MOCK_RECIPES[recipeName]);
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
            <Utensils size={24} />
            <span>PalatePal</span>
          </div>
          <div className="mobile-spacer" />
        </div>

        {/* Main content */}
        <div className="main-content">
          <div className="content-wrapper">
            {currentScreen === 'home' && (
              <Home 
                comfortCuisine={comfortCuisine}
                setComfortCuisine={setComfortCuisine}
                comfortDish={comfortDish}
                setComfortDish={setComfortDish}
                targetCuisine={targetCuisine}
                setTargetCuisine={setTargetCuisine}
                allergenFilter={allergenFilter}
                setAllergenFilter={setAllergenFilter}
                onTranslate={handleTranslate}
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
              <Restaurants />
            )}
            
            {currentScreen === 'allergens' && (
              <Allergens 
                selectedAllergens={selectedAllergens}
                toggleAllergen={toggleAllergen}
              />
            )}
            
            {currentScreen === 'profile' && (
              <Profile 
                userProfile={userProfile}
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
