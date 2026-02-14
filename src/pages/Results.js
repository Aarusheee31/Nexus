import React, { useEffect, useState } from 'react';
import './Pages.css';

const RecipeModal = ({ recipeName, recipeId, onClose }) => {
  const [instructions, setInstructions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecipe = async () => {
      setLoading(true);
      setError(null);
      try {
        // Use recipe_id if available, otherwise fall back to title lookup
        let steps = [];

        if (recipeId) {
          const res = await fetch(`http://localhost:5000/api/recipe/details/${recipeId}`);
          const data = await res.json();
          if (!res.ok) throw new Error(data.error || 'Failed to fetch recipe');
          steps = data.instructions || [];
        }

        // If no steps from ID (or no ID), try by title
        if (steps.length === 0) {
          const encoded = encodeURIComponent(recipeName);
          const res = await fetch(`http://localhost:5000/api/recipe/${encoded}`);
          const data = await res.json();
          if (!res.ok) throw new Error(data.error || 'Failed to fetch recipe');
          steps = data.instructions || [];
        }

        setInstructions(steps);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipe();
  }, [recipeId, recipeName]);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">{recipeName}</h2>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>

        <div className="modal-body">
          {loading && (
            <div className="modal-loading">
              <div className="loading-spinner" />
              <p>Fetching recipe steps...</p>
            </div>
          )}

          {error && (
            <div className="modal-error">
              <p>⚠️ {error}</p>
              <p className="modal-error-hint">Try searching for this recipe manually.</p>
            </div>
          )}

          {!loading && !error && instructions.length === 0 && (
            <p className="modal-empty">No instructions found for this recipe.</p>
          )}

          {!loading && !error && instructions.length > 0 && (
            <ol className="instruction-list">
              {instructions.map((step, i) => (
                <li key={i} className="instruction-step">
                  <span className="step-number">{i + 1}</span>
                  <p className="step-text">{step}</p>
                </li>
              ))}
            </ol>
          )}
        </div>
      </div>
    </div>
  );
};


const Results = ({ 
  matchResults, 
  comfortDish,
  animateProgress,
  setAnimateProgress,
  onViewRecipe,
  onBack
}) => {
  const [activeModal, setActiveModal] = useState(null); // { name, recipeId }

  useEffect(() => {
    if (matchResults.length > 0) {
      setTimeout(() => setAnimateProgress(true), 100);
    }
  }, [matchResults, setAnimateProgress]);

  return (
    <div className="screen-content animate-fade-in">
      <div className="screen-header-center">
        <h1 className="main-title">Your Flavor Matches</h1>
        <p className="subtitle">
          Based on <span className="text-highlight">{comfortDish}</span>
        </p>
      </div>

      <div className="results-grid">
        {matchResults.map((match, index) => (
          <div 
            key={match.id}
            className="result-card"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="result-header">
              <div className="result-title-section">
                <span className="result-emoji">{match.image}</span>
                <h3 className="result-title">{match.name}</h3>
              </div>
              <div className="match-badge">
                <span className="match-score">{match.matchScore}%</span>
              </div>
            </div>

            <div className="progress-container">
              <div 
                className="progress-bar"
                style={{ width: animateProgress ? `${match.matchScore}%` : '0%' }}
              />
            </div>

            <p className="result-explanation">{match.explanation}</p>

            <div className="ingredient-tags">
              {match.ingredients.map((ingredient, i) => (
                <span key={i} className="ingredient-tag">{ingredient}</span>
              ))}
            </div>

            <div className="result-actions">
              {match.hasRecipe && (
                <button 
                  onClick={() => onViewRecipe(match.name)}
                  className="btn-primary"
                >
                  View Recipe
                </button>
              )}
              <button 
                className="btn-outline"
                onClick={() => setActiveModal({ name: match.name, recipeId: match.recipe_id || match.recipeId || null })}
              >
                Show Recipe Steps
              </button>
            </div>
          </div>
        ))}
      </div>

      <button onClick={onBack} className="back-button">
        ← Try Another Translation
      </button>

      {/* Recipe Modal */}
      {activeModal && (
        <RecipeModal
          recipeName={activeModal.name}
          recipeId={activeModal.recipeId}
          onClose={() => setActiveModal(null)}
        />
      )}
    </div>
  );
};

export default Results;