import React from 'react';
import { AlertCircle } from 'lucide-react';
import './Pages.css';

const Allergens = ({ commonAllergens = [], allergenSubstitutes = {}, selectedAllergens, toggleAllergen }) => {
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
              onClick={() => toggleAllergen(allergen)}
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
              </div>
              <div className="substitute-body">
                {allergenSubstitutes[allergen]?.map((substitute, index) => (
                  <div key={index} className="substitute-item">
                    <h5>{substitute.name}</h5>
                    <p>{substitute.description}</p>
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
