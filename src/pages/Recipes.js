import React, { useState, useEffect } from 'react';
import { Search, Clock, Users, ChefHat, Loader } from 'lucide-react';
import RecipeDetail from './RecipeDetail';
import './Pages.css';

const Recipes = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);
  const [selectedRecipe, setSelectedRecipe] = useState(null);

  // Debounced search
  useEffect(() => {
    if (searchQuery.trim().length < 3) {
      setSearchResults([]);
      setHasSearched(false);
      return;
    }

    const delaySearch = setTimeout(() => {
      handleSearch();
    }, 500); // Wait 500ms after user stops typing

    return () => clearTimeout(delaySearch);
  }, [searchQuery]);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setIsLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const response = await fetch('http://localhost:5000/api/recipe/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: searchQuery
        })
      });

      if (!response.ok) {
        throw new Error('Failed to search recipes');
      }

      const data = await response.json();
      setSearchResults(data.recipes || []);
    } catch (err) {
      console.error('Search error:', err);
      setError('Failed to search recipes. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRecipeClick = (recipe) => {
    setSelectedRecipe(recipe);
  };

  const handleBackToSearch = () => {
    setSelectedRecipe(null);
  };

  // If a recipe is selected, show the detail view
  if (selectedRecipe) {
    return <RecipeDetail recipe={selectedRecipe} onBack={handleBackToSearch} />;
  }

  // Otherwise show the search interface
  return (
    <div className="screen-content animate-fade-in">
      <div className="screen-header-center">
        <h1 className="main-title">
          Recipe <span className="text-highlight">Finder</span>
        </h1>
        <p className="subtitle">Explore authentic recipes from around the world</p>
      </div>

      <div className="tip-card-main">
        <ChefHat size={24} className="tip-icon" />
        <div>
          <p className="tip-title-main">Search for any recipe</p>
          <p className="tip-text-main">
            Type the name of a dish you want to cook - like "chicken curry", "pasta", or "baklava"
          </p>
        </div>
      </div>

      <div className="search-box">
        <Search size={20} />
        <input
          type="text"
          placeholder="Search recipes... (e.g., chicken curry, pasta, baklava)"
          className="search-input"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Loading State */}
      {isLoading && (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <Loader size={40} className="spinner" style={{ animation: 'spin 1s linear infinite' }} />
          <p style={{ marginTop: '16px', color: '#6B6B6B' }}>Searching recipes...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="alert-card">
          <div className="alert-icon">⚠️</div>
          <div>
            <p className="alert-title">Error</p>
            <p className="alert-text">{error}</p>
          </div>
        </div>
      )}

      {/* No Results */}
      {!isLoading && hasSearched && searchResults.length === 0 && !error && (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <span style={{ fontSize: '48px' }}>🔍</span>
          <h3 style={{ marginTop: '16px', color: '#1E1E1E' }}>No recipes found</h3>
          <p style={{ color: '#6B6B6B', marginTop: '8px' }}>
            Try searching for something else like "chicken", "pasta", or "curry"
          </p>
        </div>
      )}

      {/* Results Grid */}
      {!isLoading && searchResults.length > 0 && (
        <>
          <div style={{ textAlign: 'center', marginBottom: '8px' }}>
            <p style={{ color: '#6B6B6B', fontSize: '14px' }}>
              Found <strong>{searchResults.length}</strong> recipe{searchResults.length !== 1 ? 's' : ''}
            </p>
          </div>

          <div className="recipes-grid">
            {searchResults.map((recipe, index) => (
              <div 
                key={recipe.Recipe_id || index}
                className="recipe-preview-card"
                onClick={() => handleRecipeClick(recipe)}
              >
                <div className="recipe-preview-header">
                  <span className="recipe-preview-emoji">🍽️</span>
                  <span className="difficulty-badge">
                    {recipe.Region || 'Recipe'}
                  </span>
                </div>
                
                <h3 className="recipe-preview-title">{recipe.Recipe_title}</h3>
                
                <div className="recipe-preview-meta">
                  {recipe.prep_time && (
                    <div className="meta-item-small">
                      <Clock size={14} />
                      <span>{recipe.prep_time} min</span>
                    </div>
                  )}
                  {recipe.servings && (
                    <div className="meta-item-small">
                      <Users size={14} />
                      <span>{recipe.servings} servings</span>
                    </div>
                  )}
                  {recipe.Calories && (
                    <div className="meta-item-small">
                      <span>🔥</span>
                      <span>{recipe.Calories} cal</span>
                    </div>
                  )}
                </div>
                
                <button className="recipe-preview-button">View Recipe</button>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Empty State (before any search) */}
      {!hasSearched && !isLoading && (
        <div style={{ textAlign: 'center', padding: '60px 20px' }}>
          <span style={{ fontSize: '64px' }}>🔍</span>
          <h3 style={{ marginTop: '16px', color: '#1E1E1E', fontSize: '20px' }}>
            Start searching for recipes
          </h3>
          <p style={{ color: '#6B6B6B', marginTop: '8px', fontSize: '14px' }}>
            Type at least 3 characters to search
          </p>
        </div>
      )}
    </div>
  );
};

// Add spinner animation
const style = document.createElement('style');
style.textContent = `
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
`;
document.head.appendChild(style);

export default Recipes;