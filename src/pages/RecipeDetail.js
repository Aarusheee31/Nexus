import React from 'react';
import { Clock, Users, UtensilsCrossed, BookOpen } from 'lucide-react';
import './Pages.css';

const RecipeDetail = ({ recipe, onBack }) => {
  if (!recipe) return null;

  return (
    <div className="screen-content animate-fade-in">
      <button onClick={onBack} className="back-link">
        ← Back to Results
      </button>

      <div className="recipe-card">
        <div className="recipe-header">
          <div className="recipe-title-section">
            <span className="recipe-emoji">{recipe.image}</span>
            <h1 className="recipe-title">{recipe.name}</h1>
          </div>
          <div className="recipe-meta">
            <div className="meta-item">
              <Clock size={16} />
              <span>Prep: {recipe.prepTime}</span>
            </div>
            <div className="meta-item">
              <Clock size={16} />
              <span>Cook: {recipe.cookTime}</span>
            </div>
            <div className="meta-item">
              <Users size={16} />
              <span>{recipe.servings} servings</span>
            </div>
          </div>
        </div>

        <div className="recipe-body">
          <div className="recipe-section">
            <h3 className="section-title">
              <UtensilsCrossed size={20} />
              Ingredients
            </h3>
            <ul className="ingredients-list">
              {recipe.ingredients.map((ingredient, i) => (
                <li key={i}>{ingredient}</li>
              ))}
            </ul>
          </div>

          <div className="recipe-section">
            <h3 className="section-title">
              <BookOpen size={20} />
              Instructions
            </h3>
            <ol className="instructions-list">
              {recipe.instructions.map((instruction, i) => (
                <li key={i}>
                  <span className="step-number">{i + 1}</span>
                  <p>{instruction}</p>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipeDetail;
