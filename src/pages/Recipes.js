import React from 'react';
import { Search, Clock, Users } from 'lucide-react';
import { MOCK_RECIPES } from '../data/mockData';
import './Pages.css';

const Recipes = ({ onSelectRecipe }) => {
  return (
    <div className="screen-content animate-fade-in">
      <div className="screen-header-center">
        <h1 className="main-title">Recipe Finder</h1>
        <p className="subtitle">Explore authentic recipes from around the world</p>
      </div>

      <div className="search-box">
        <Search size={20} />
        <input
          type="text"
          placeholder="Search recipes..."
          className="search-input"
        />
      </div>

      <div className="recipes-grid">
        {Object.values(MOCK_RECIPES).map((recipe, index) => (
          <div 
            key={index}
            className="recipe-preview-card"
            onClick={() => onSelectRecipe(recipe)}
          >
            <div className="recipe-preview-header">
              <span className="recipe-preview-emoji">{recipe.image}</span>
              <span className="difficulty-badge">{recipe.difficulty}</span>
            </div>
            <h3 className="recipe-preview-title">{recipe.name}</h3>
            <div className="recipe-preview-meta">
              <div className="meta-item-small">
                <Clock size={14} />
                <span>{recipe.prepTime}</span>
              </div>
              <div className="meta-item-small">
                <Users size={14} />
                <span>{recipe.servings} servings</span>
              </div>
            </div>
            <button className="recipe-preview-button">View Recipe</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recipes;
