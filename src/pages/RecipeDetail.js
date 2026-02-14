import React, { useState, useEffect } from 'react';
import { Clock, Users, Flame, ChefHat, ArrowLeft, Loader } from 'lucide-react';
import './Pages.css';

const RecipeDetail = ({ recipe, onBack }) => {
  const [instructions, setInstructions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRecipeInstructions();
  }, [recipe.Recipe_id]);

  const fetchRecipeInstructions = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `http://localhost:5000/api/recipe/details/${recipe.Recipe_id}`
      );

      if (!response.ok) {
        throw new Error('Failed to fetch recipe instructions');
      }

      const data = await response.json();
      setInstructions(data.instructions || []);
    } catch (err) {
      console.error('Error fetching instructions:', err);
      setError('Could not load recipe instructions. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="screen-content animate-fade-in">
      {/* Back Button */}
      <button onClick={onBack} className="back-button">
        <ArrowLeft size={20} style={{ marginRight: '8px' }} />
        Back to Search
      </button>

      {/* Recipe Card */}
      <div className="recipe-card">
        {/* Header */}
        <div className="recipe-header">
          <div className="recipe-title-section">
            <span className="recipe-emoji">🍽️</span>
            <div>
              <h1 className="recipe-title">{recipe.Recipe_title}</h1>
              <p style={{ fontSize: '16px', opacity: 0.9, marginTop: '4px' }}>
                {recipe.Region} • {recipe.Continent}
              </p>
            </div>
          </div>

          <div className="recipe-meta">
            {recipe.prep_time && (
              <div className="meta-item">
                <Clock size={18} />
                <span>Prep: {recipe.prep_time} min</span>
              </div>
            )}
            {recipe.cook_time && (
              <div className="meta-item">
                <Clock size={18} />
                <span>Cook: {recipe.cook_time} min</span>
              </div>
            )}
            {recipe.servings && (
              <div className="meta-item">
                <Users size={18} />
                <span>{recipe.servings} servings</span>
              </div>
            )}
            {recipe.Calories && (
              <div className="meta-item">
                <Flame size={18} />
                <span>{recipe.Calories} cal</span>
              </div>
            )}
          </div>
        </div>

        {/* Body */}
        <div className="recipe-body">
          {/* Recipe ID Info */}
          <div style={{ 
            background: '#F7F7F5', 
            padding: '12px 16px', 
            borderRadius: '8px',
            marginBottom: '24px',
            fontSize: '13px',
            color: '#6B6B6B'
          }}>
            Recipe ID: {recipe.Recipe_id}
          </div>

          {/* Instructions Section */}
          <div className="recipe-section">
            <h2 className="section-title">
              <ChefHat size={24} />
              Cooking Instructions
            </h2>

            {isLoading && (
              <div style={{ textAlign: 'center', padding: '40px' }}>
                <Loader 
                  size={40} 
                  style={{ 
                    animation: 'spin 1s linear infinite',
                    margin: '0 auto',
                    color: '#2E7D32'
                  }} 
                />
                <p style={{ marginTop: '16px', color: '#6B6B6B' }}>
                  Loading cooking instructions...
                </p>
              </div>
            )}

            {error && (
              <div className="alert-card">
                <div className="alert-icon">⚠️</div>
                <div>
                  <p className="alert-title">Error</p>
                  <p className="alert-text">{error}</p>
                </div>
              </div>
            )}

            {!isLoading && !error && instructions.length > 0 && (
              <ol className="instructions-list">
                {instructions.map((step, index) => (
                  <li key={index}>
                    <div className="step-number">{index + 1}</div>
                    <p>{step}</p>
                  </li>
                ))}
              </ol>
            )}

            {!isLoading && !error && instructions.length === 0 && (
              <div style={{ 
                textAlign: 'center', 
                padding: '40px',
                background: '#F7F7F5',
                borderRadius: '12px'
              }}>
                <ChefHat size={48} style={{ color: '#9E9E9E', margin: '0 auto 16px' }} />
                <p style={{ color: '#6B6B6B', fontSize: '15px' }}>
                  No cooking instructions available for this recipe.
                </p>
              </div>
            )}
          </div>

          {/* Additional Info */}
          {(recipe.total_time || recipe.vegan || recipe.vegetarian) && (
            <div className="recipe-section">
              <h2 className="section-title">
                📋 Additional Information
              </h2>
              
              <div style={{ 
                display: 'flex', 
                flexDirection: 'column', 
                gap: '12px' 
              }}>
                {recipe.total_time && (
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between',
                    padding: '12px 16px',
                    background: '#F7F7F5',
                    borderRadius: '8px'
                  }}>
                    <span style={{ fontWeight: 600, color: '#1E1E1E' }}>Total Time:</span>
                    <span style={{ color: '#6B6B6B' }}>{recipe.total_time} minutes</span>
                  </div>
                )}

                {recipe.vegan === '1.0' && (
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center',
                    gap: '8px',
                    padding: '12px 16px',
                    background: 'linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%)',
                    borderRadius: '8px',
                    border: '1px solid #A5D6A7'
                  }}>
                    <span style={{ fontSize: '20px' }}>🌱</span>
                    <span style={{ fontWeight: 600, color: '#2E7D32' }}>Vegan Friendly</span>
                  </div>
                )}

                {recipe.vegetarian === '1.0' && recipe.vegan !== '1.0' && (
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center',
                    gap: '8px',
                    padding: '12px 16px',
                    background: 'linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%)',
                    borderRadius: '8px',
                    border: '1px solid #A5D6A7'
                  }}>
                    <span style={{ fontSize: '20px' }}>🥬</span>
                    <span style={{ fontWeight: 600, color: '#2E7D32' }}>Vegetarian</span>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Nutrition */}
          {recipe.Calories && (
            <div className="recipe-section">
              <h2 className="section-title">
                🔥 Nutrition
              </h2>
              
              <div style={{ 
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                gap: '16px'
              }}>
                <div style={{ 
                  padding: '20px',
                  background: 'linear-gradient(135deg, #FFF9E6 0%, #FFE8B3 100%)',
                  borderRadius: '12px',
                  border: '1px solid #FFB703',
                  textAlign: 'center'
                }}>
                  <div style={{ 
                    fontSize: '32px', 
                    fontWeight: 700,
                    color: '#FFB703',
                    marginBottom: '4px'
                  }}>
                    {recipe.Calories}
                  </div>
                  <div style={{ fontSize: '14px', color: '#6B6B6B' }}>
                    Calories
                  </div>
                </div>

                {recipe.servings && (
                  <div style={{ 
                    padding: '20px',
                    background: 'linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%)',
                    borderRadius: '12px',
                    border: '1px solid #A5D6A7',
                    textAlign: 'center'
                  }}>
                    <div style={{ 
                      fontSize: '32px', 
                      fontWeight: 700,
                      color: '#2E7D32',
                      marginBottom: '4px'
                    }}>
                      {Math.round(recipe.Calories / recipe.servings)}
                    </div>
                    <div style={{ fontSize: '14px', color: '#6B6B6B' }}>
                      Cal per serving
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RecipeDetail;