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
        let steps = [];

        if (recipeId) {
          const res = await fetch(`http://localhost:5000/api/recipe/details/${recipeId}`);
          const data = await res.json();
          if (!res.ok) throw new Error(data.error || 'Failed to fetch recipe');
          steps = data.instructions || [];
        }

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
  const [activeModal, setActiveModal] = useState(null);

  useEffect(() => {
    if (matchResults.length > 0) {
      setTimeout(() => setAnimateProgress(true), 100);
    }
  }, [matchResults, setAnimateProgress]);

  const generateMetrics = (matchScore) => {
    const base = matchScore;
    return {
      comfort_similarity: Math.min(100, base + Math.random() * 15),
      flavor_similarity: Math.min(100, base - 5 + Math.random() * 20),
      adaptability: Math.min(100, base - 10 + Math.random() * 25),
      ingredient_match: Math.min(100, base - 15 + Math.random() * 30),
    };
  };

  const metricLabels = {
    comfort_similarity: { label: ' Comfort Index', color: '#8B7355' },
    flavor_similarity: { label: ' Familiar Flavor', color: '#6B8E23' },
    adaptability: { label: 'Ease of Transition', color: '#CD853F' },
    ingredient_match: { label: ' Shared Ingredients', color: '#9ACD32' }
  };

  return (
    <div className="screen-content animate-fade-in">
      <div className="screen-header-center">
        <h1 className="main-title">Your Flavor Matches</h1>
        <p className="subtitle">
          Based on <span className="text-highlight">{comfortDish}</span>
        </p>
      </div>

      <div className="results-grid">
        {matchResults.map((match, index) => {
          const metrics = generateMetrics(match.matchScore); // ✅ was defined but never called

          return (
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

              <div className="emotional-metrics">
                {Object.entries(metricLabels).map(([key, config]) => {
                  const value = metrics[key];
                  return (
                    <div key={key} className="metric-row">
                      <div className="metric-label">{config.label}</div>
                      <div className="metric-bar-container">
                        <div
                          className="metric-bar"
                          style={{
                            width: animateProgress ? `${value}%` : '0%',
                            backgroundColor: config.color
                          }}
                        />
                      </div>
                      <div className="metric-value">{Math.round(value)}%</div>
                    </div>
                  );
                })}
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
            </div> // ✅ was incorrectly closed with ); instead of </div>
          );
        })}
      </div>

      <button onClick={onBack} className="back-button">
        ← Try Another Translation
      </button>

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