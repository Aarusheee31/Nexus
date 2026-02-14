import React from 'react';
import { User, AlertCircle, ChefHat, X } from 'lucide-react';
import { COMMON_ALLERGENS } from '../data/mockData';
import './Pages.css';

const Profile = ({ userProfile, addAllergen, removeAllergen }) => {
  return (
    <div className="screen-content animate-fade-in">
      <div className="profile-header">
        <div className="profile-avatar">
          <User size={48} />
        </div>
        <h1 className="profile-name">{userProfile.name}</h1>
        <p className="profile-email">{userProfile.email}</p>
        <p className="profile-date">Member since {userProfile.joinDate}</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card stat-card-green">
          <div className="stat-number">{userProfile.translationsCompleted}</div>
          <div className="stat-label">Translations</div>
        </div>
        <div className="stat-card stat-card-amber">
          <div className="stat-number">{userProfile.recipesViewed}</div>
          <div className="stat-label">Recipes Viewed</div>
        </div>
      </div>

      <div className="profile-section">
        <div className="section-header-red">
          <AlertCircle size={20} />
          <h3>My Allergens</h3>
        </div>
        <div className="profile-section-body">
          <div className="allergen-tags">
            {userProfile.allergens.map(allergen => (
              <div key={allergen} className="allergen-tag-removable">
                <span>{allergen}</span>
                <button onClick={() => removeAllergen(allergen)}>
                  <X size={14} />
                </button>
              </div>
            ))}
          </div>
          <select
            onChange={(e) => {
              if (e.target.value) {
                addAllergen(e.target.value);
                e.target.value = '';
              }
            }}
            className="form-select"
          >
            <option value="">Add allergen...</option>
            {COMMON_ALLERGENS.filter(a => !userProfile.allergens.includes(a)).map(allergen => (
              <option key={allergen} value={allergen}>{allergen}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="profile-section">
        <div className="section-header-green">
          <ChefHat size={20} />
          <h3>Favorite Cuisines</h3>
        </div>
        <div className="profile-section-body">
          <div className="cuisine-tags">
            {userProfile.favoriteCuisines.map(cuisine => (
              <span key={cuisine} className="cuisine-tag">{cuisine}</span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
