import React from 'react';
import { Lightbulb, AlertCircle } from 'lucide-react';
import './Pages.css';

const Home = ({ 
  comfortCuisines = [],
  targetCuisines = [],
  comfortCuisine, 
  setComfortCuisine,
  comfortDish,
  setComfortDish,
  targetCuisine,
  setTargetCuisine,
  allergenFilter,
  setAllergenFilter,
  onTranslate,
  loading = false,
  error = null,
}) => {
  return (
    <div className="screen-content animate-fade-in">
      <div className="screen-header-center">
        <h1 className="main-title">
          Find Comfort in <span className="text-highlight">New Cuisines</span>
        </h1>
        <p className="subtitle">Translate your familiar flavors into local dishes</p>
      </div>

      <div className="tip-card-main">
        <Lightbulb size={24} className="tip-icon" />
        <div>
          <p className="tip-title-main">How it works</p>
          <p className="tip-text-main">
            We analyze flavor profiles, textures, and comfort factors to find dishes that feel familiar in new cuisines
          </p>
        </div>
      </div>

      <div className="form-container">
        <div className="form-group">
          <label className="form-label">Your Comfort Cuisine</label>
          <select
            value={comfortCuisine}
            onChange={(e) => setComfortCuisine(e.target.value)}
            className="form-select"
          >
            <option value="">Select cuisine...</option>
            {comfortCuisines.map(cuisine => (
              <option key={cuisine} value={cuisine}>{cuisine}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Your Comfort Dish</label>
          <input
            type="text"
            value={comfortDish}
            onChange={(e) => setComfortDish(e.target.value)}
            placeholder="e.g., Rajma Chawal, Mac and Cheese..."
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Discover in Cuisine</label>
          <select
            value={targetCuisine}
            onChange={(e) => setTargetCuisine(e.target.value)}
            className="form-select"
          >
            <option value="">Select target cuisine...</option>
            {targetCuisines.map(cuisine => (
              <option key={cuisine} value={cuisine}>{cuisine}</option>
            ))}
          </select>
        </div>

        <div className="toggle-container">
          <div className="toggle-info">
            <AlertCircle size={20} />
            <span>Apply Allergen Filter</span>
          </div>
          <button
            onClick={() => setAllergenFilter(!allergenFilter)}
            className={`toggle-switch ${allergenFilter ? 'toggle-active' : ''}`}
          >
            <div className="toggle-slider" />
          </button>
        </div>
      </div>

      {error && (
        <p className="error-message" style={{ color: '#e74c3c', marginBottom: 16 }}>
          {error}
        </p>
      )}
      <button
        onClick={onTranslate}
        disabled={!comfortCuisine || !comfortDish || !targetCuisine || loading}
        className="cta-button"
      >
        {loading ? 'Finding matches...' : 'Translate My Palate'}
      </button>
    </div>
  );
};

export default Home;
