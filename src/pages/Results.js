import React, { useEffect } from 'react';
import './Pages.css';



const Results = ({ 
  matchResults, 
  comfortDish,
  animateProgress,
  setAnimateProgress,
  onViewRecipe,
  onBack
}) => {
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
              <button className="btn-outline">Find Nearby</button>
            </div>
          </div>
        ))}
      </div>

      <button onClick={onBack} className="back-button">
        ← Try Another Translation
      </button>
    </div>
  );
};

export default Results;
