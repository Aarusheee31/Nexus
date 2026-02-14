import React from 'react';
import { MapPin, Star } from 'lucide-react';
import { MOCK_RESTAURANTS } from '../data/mockData';
import './Pages.css';

const Restaurants = () => {
  return (
    <div className="screen-content animate-fade-in">
      <div className="screen-header-center">
        <h1 className="main-title">Nearby Restaurants</h1>
        <p className="subtitle">Find restaurants matching your flavor profile</p>
      </div>

      <div className="location-card">
        <MapPin size={24} className="location-icon" />
        <div>
          <p className="location-title">Location: San Francisco, CA</p>
          <p className="location-text">Showing restaurants within 5 miles</p>
        </div>
      </div>

      <div className="restaurants-grid">
        {MOCK_RESTAURANTS.map((restaurant) => (
          <div key={restaurant.id} className="restaurant-card">
            <div className="restaurant-header">
              <div className="restaurant-info">
                <span className="restaurant-emoji">{restaurant.image}</span>
                <div>
                  <h3 className="restaurant-name">{restaurant.name}</h3>
                  <p className="restaurant-cuisine">{restaurant.cuisine} • {restaurant.price}</p>
                </div>
              </div>
              <div className="match-badge-small">
                {restaurant.matchScore}%
              </div>
            </div>
            
            <div className="restaurant-meta">
              <div className="meta-item-small">
                <MapPin size={14} />
                <span>{restaurant.distance}</span>
              </div>
              <div className="meta-item-small">
                <Star size={14} fill="#FFB703" stroke="#FFB703" />
                <span>{restaurant.rating}</span>
              </div>
            </div>

            <div className="restaurant-actions">
              <button className="btn-primary-small">Get Directions</button>
              <button className="btn-outline-small">View Menu</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Restaurants;
