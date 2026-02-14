import React from 'react';
import { AlertCircle, Lightbulb } from 'lucide-react';
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
        <h1 
          style={{ fontSize: '25px', fontWeight: 'bold', fontFamily: 'sans-serif' }} 
          className="main-title"
        >
          Helping You Find Comfort in <span className="text-highlight">New Cuisines</span>
        </h1>

        <p 
          style={{ fontSize: '14px', color: '#6B6B6B' }} 
          className="subtitle"
        >
          Translate your familiar flavours into local dishes!
        </p>
      </div>

      <div className="tip-card-main">
        <Lightbulb size={24} className="tip-icon" />
        <div>
          <p className="tip-title-main">How it works</p>
          <p className="tip-text-main">
            We decode the flavour DNA of your comfort dish and match it to local ingredients that recreate the same taste experience
          </p>
        </div>
      </div>

      <h1>Hi Kritika!</h1>

      <div className="form-group">
        <label className="form-label">
          What Comfort Dish are you missing today?
        </label>
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
          <option value="">Select target cuisine...</option>
          {targetCuisines.map(cuisine => (
            <option key={cuisine} value={cuisine}>
              {cuisine}
            </option>
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

      {error && (
        <p 
          className="error-message"
          style={{ color: '#e74c3c', marginBottom: 16 }}
        >
          {error}
        </p>
      )}

      <button
        onClick={onTranslate}
        disabled={!comfortDish || !targetCuisine || loading}
        className="cta-button"
      >
        {loading ? 'Finding matches...' : 'Translate My Palate'}
      </button>

    </div>
  );
};

export default Home;
