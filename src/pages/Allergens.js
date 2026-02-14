import React, { useState } from 'react';
import { AlertCircle, Loader } from 'lucide-react';
import './Pages.css';

const Allergens = ({ commonAllergens = [], selectedAllergens, toggleAllergen }) => {
  const [substitutes, setSubstitutes] = useState({});   // { allergenName: { substitutes, category } }
  const [loading, setLoading] = useState({});           // { allergenName: true/false }
  const [errors, setErrors] = useState({});

  const handleToggleAllergen = async (allergen) => {
    toggleAllergen(allergen);

    // If we're selecting (not deselecting) and haven't fetched yet
    if (!selectedAllergens.includes(allergen) && !substitutes[allergen]) {
      setLoading(prev => ({ ...prev, [allergen]: true }));
      setErrors(prev => ({ ...prev, [allergen]: null }));

      try {
        const response = await fetch('http://localhost:5000/api/allergen/substitutes', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ allergen })
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error || 'Failed to fetch substitutes');

        setSubstitutes(prev => ({
          ...prev,
          [allergen]: {
            category: data.category,
            matched_entity: data.matched_entity,
            items: data.substitutes
          }
        }));
      } catch (err) {
        setErrors(prev => ({ ...prev, [allergen]: err.message }));
      } finally {
        setLoading(prev => ({ ...prev, [allergen]: false }));
      }
    }
  };

  return (
    <div className="screen-content animate-fade-in">
      <div className="screen-header-center">
        <h1 className="main-title">Allergen Guide</h1>
        <p className="subtitle">Find safe substitutes for your allergens</p>
      </div>

      <div className="alert-card">
        <AlertCircle size={24} className="alert-icon" />
        <div>
          <p className="alert-text">
            Always consult with healthcare professionals about allergen substitutes
          </p>
        </div>
      </div>

      <div className="allergen-selector">
        <h3 className="section-title-small">Select Allergens</h3>
        <div className="allergen-pills">
          {commonAllergens.map(allergen => (
            <button
              key={allergen}
              onClick={() => handleToggleAllergen(allergen)}
              className={`allergen-pill ${selectedAllergens.includes(allergen) ? 'allergen-pill-active' : ''}`}
            >
              {allergen}
            </button>
          ))}
        </div>
      </div>

      {selectedAllergens.length > 0 && (
        <div className="substitutes-container">
          <h3 className="section-title-small">Safe Substitutes</h3>

          {selectedAllergens.map(allergen => (
            <div key={allergen} className="substitute-card">
              <div className="substitute-header">
                <h4>Alternatives for {allergen}</h4>
                {substitutes[allergen] && (
                  <span className="category-badge">
                    {substitutes[allergen].category}
                  </span>
                )}
              </div>

              <div className="substitute-body">
                {/* Loading state */}
                {loading[allergen] && (
                  <div className="loading-state">
                    <Loader size={18} className="spin" />
                    <span>Finding alternatives for you to enjoy!</span>
                  </div>
                )}

                {/* Error state */}
                {errors[allergen] && (
                  <p className="error-text">⚠️ {errors[allergen]}</p>
                )}

                {/* Results */}
                {substitutes[allergen]?.items?.map((sub, i) => (
                  <div key={i} className="substitute-item">
                    <div className="substitute-item-header">
                      <h5>{sub.name}</h5>
                    </div>
                    <p>{sub.description}</p>
                    {sub.wikipedia && (
                      <a href={sub.wikipedia} target="_blank" rel="noopener noreferrer"
                        className="wiki-link">Learn more →</a>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Allergens;