import React from 'react';
import { Lightbulb, AlertCircle, Apple } from 'lucide-react';
import { COMFORT_CUISINES, TARGET_CUISINES } from '../data/mockData';
import './Pages.css';

const Home = ({ 
  comfortCuisine, 
  setComfortCuisine,
  comfortDish,
  setComfortDish,
  targetCuisine,
  setTargetCuisine,
  allergenFilter,
  setAllergenFilter,
  onTranslate
}) => {
  return (
    <div className="screen-content animate-fade-in">
      <div className="screen-header-center">
        <h1 style={{ fontSize: '25px', fontWeight: 'bold', fontFamily: 'sans-serif' }} className="main-title">
          Helping You Find Comfort in <span className="text-highlight">New Cuisines</span>
        </h1>
        <p style={{ fontSize: '14px', color: '#6B6B6B' }} className="subtitle">Translate your familiar flavours into local dishes!</p>
      </div>

      <div className="tip-card-main">
        <Apple size={24} className="tip-icon" />
        <div>
          <p className="tip-title-main">How it works</p>
          <p className="tip-text-main">
           We decode the flavour DNA of your comfort dish and match it to local ingredients that recreate the same taste experience
          </p>
        </div>
      </div>

      <div className="form-container">
        <div className="form-group">
          <label className="form-label">Cuisine You Are Missing:</label>
          <select
            value={comfortCuisine}
            onChange={(e) => setComfortCuisine(e.target.value)}
            className="form-select"
          >
            <option value="">Select cuisine...</option>
            {COMFORT_CUISINES.map(cuisine => (
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
            placeholder="e.g., Chicken Curry, Tacos..."
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Cuisine Near You?</label>
          <select
            value={targetCuisine}
            onChange={(e) => setTargetCuisine(e.target.value)}
            className="form-select"
          >
            <option value="">Select cuisine...</option>
            {TARGET_CUISINES.map(cuisine => (
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

      <button
        onClick={onTranslate}
        disabled={!comfortCuisine || !comfortDish || !targetCuisine}
        className="cta-button"
      >
        Translate My Palate
      </button>
    </div>
  );
};

export default Home;
