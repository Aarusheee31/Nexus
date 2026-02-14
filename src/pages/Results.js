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
          const metrics = generateMetrics(match.matchScore);
          
          return (
            <div 
              key={match.id || index}
              className="result-card"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="result-header">
                <div className="result-title-section">
                  <span className="result-emoji">{match.image || '🍽️'}</span>
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
              </div>
            </div>
          );
        })}
      </div>

      <button onClick={onBack} className="back-button">
        ← Try Another Translation
      </button>
    </div>
  );
};

export default Results;