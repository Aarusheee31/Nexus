import React, { useState } from 'react';
import { UtensilsCrossed, Sparkles, ChevronRight, ChevronLeft, Check } from 'lucide-react';
import './Onboarding.css';

const ONBOARDING_STORAGE_KEY = 'palatepal_onboarding_done';
const USER_NAME_KEY = 'palatepal_user_name';
const USER_GOAL_KEY = 'palatepal_user_goal';
const USER_ALLERGENS_KEY = 'palatepal_onboarding_allergens';
const USER_HOME_FOOD_KEY = 'palatepal_home_food';
const USER_CUISINES_WANT_KEY = 'palatepal_cuisines_want_to_try';

const GOAL_OPTIONS = [
  { value: '', label: 'Select one...' },
  { value: 'explore', label: 'Explore new cuisines' },
  { value: 'comfort', label: 'Find comfort in familiar flavours' },
  { value: 'allergies', label: 'Manage dietary restrictions' },
  { value: 'cook', label: 'Discover new recipes' },
];

const HOME_FOOD_CHIPS = ['Curry', 'Pasta', 'Ramen', 'Biryani', 'Soup'];

const CUISINES_WANT_OPTIONS = ['Japanese', 'Korean', 'Middle Eastern', 'Thai', 'Mexican', 'French'];

const ALLERGEN_OPTIONS = [
  'Dairy', 'Gluten', 'Nuts', 'Shellfish', 'Eggs', 'Soy',
];

export function getOnboardingComplete() {
  try {
    return localStorage.getItem(ONBOARDING_STORAGE_KEY) === 'true';
  } catch {
    return false;
  }
}

export function getUserName() {
  try {
    return localStorage.getItem(USER_NAME_KEY) || '';
  } catch {
    return '';
  }
}

const TOTAL_STEPS = 3;

const Onboarding = ({ onComplete }) => {
  const [step, setStep] = useState(1);
  const [name, setName] = useState('');
  const [goal, setGoal] = useState('');
  const [homeFoodChip, setHomeFoodChip] = useState('');
  const [homeFoodOther, setHomeFoodOther] = useState('');
  const [cuisinesWantToTry, setCuisinesWantToTry] = useState([]);
  const [selectedAllergens, setSelectedAllergens] = useState([]);
  const [touched, setTouched] = useState(false);

  const toggleAllergen = (allergen) => {
    setSelectedAllergens((prev) =>
      prev.includes(allergen) ? prev.filter((a) => a !== allergen) : [...prev, allergen]
    );
  };

  const toggleCuisineWant = (cuisine) => {
    setCuisinesWantToTry((prev) =>
      prev.includes(cuisine) ? prev.filter((c) => c !== cuisine) : [...prev, cuisine]
    );
  };

  const canNextStep1 = name.trim().length > 0;
  const handleNext = () => {
    if (step === 1 && !canNextStep1) {
      setTouched(true);
      return;
    }
    if (step < TOTAL_STEPS) setStep(step + 1);
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  const handleFinish = () => {
    try {
      localStorage.setItem(ONBOARDING_STORAGE_KEY, 'true');
      localStorage.setItem(USER_NAME_KEY, name.trim());
      if (goal) localStorage.setItem(USER_GOAL_KEY, goal);
      const homeFood = homeFoodOther.trim() || homeFoodChip || '';
      if (homeFood) localStorage.setItem(USER_HOME_FOOD_KEY, homeFood);
      if (cuisinesWantToTry.length > 0) {
        localStorage.setItem(USER_CUISINES_WANT_KEY, JSON.stringify(cuisinesWantToTry));
      }
      if (selectedAllergens.length > 0) {
        localStorage.setItem(USER_ALLERGENS_KEY, JSON.stringify(selectedAllergens));
      }
    } catch (err) {
      console.warn('localStorage not available', err);
    }
    onComplete?.();
  };

  const showError = touched && !name.trim();

  return (
    <div className="onboarding-wrap">
      <div className="onboarding-card">
        {/* Progress at top – same for all steps */}
        <div className="onboarding-progress-wrap">
          <div className="onboarding-progress">
            {[1, 2, 3].map((s) => (
              <React.Fragment key={s}>
                <div
                  className={`onboarding-dot ${s === step ? 'onboarding-dot-active' : ''} ${s < step ? 'onboarding-dot-done' : ''}`}
                >
                  {s < step ? <Check size={16} /> : s}
                </div>
                {s < 3 && (
                  <div
                    className={`onboarding-progress-line ${s < step ? 'onboarding-progress-line-done' : ''}`}
                  />
                )}
              </React.Fragment>
            ))}
          </div>
          <p className="onboarding-step-label">Step {step} of {TOTAL_STEPS}</p>
        </div>

        {/* Step 1: Welcome + name */}
        {step === 1 && (
          <div className="onboarding-step animate-onboarding-step">
            <div className="onboarding-hero">
              <div className="onboarding-logo">
                <UtensilsCrossed size={28} />
              </div>
              <h1 className="onboarding-title">
                Welcome to <span className="onboarding-title-accent">PalatePal</span>
              </h1>
              <p className="onboarding-subtitle">
                Let's get to know you. What should we call you?
              </p>
            </div>
            <div className="onboarding-form">
              <div className="onboarding-form-group">
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  onBlur={() => setTouched(true)}
                  placeholder="Your name"
                  className={`onboarding-input ${showError ? 'onboarding-input-error' : ''}`}
                  autoFocus
                />
                {showError && (
                  <span className="onboarding-error">Please enter your name</span>
                )}
              </div>
              <div className="onboarding-form-group">
                <label className="onboarding-label">What food feels like home to you?</label>
                <div className="onboarding-pills">
                  {HOME_FOOD_CHIPS.map((chip) => (
                    <button
                      key={chip}
                      type="button"
                      onClick={() => setHomeFoodChip(homeFoodChip === chip ? '' : chip)}
                      className={`onboarding-pill onboarding-pill-chip ${homeFoodChip === chip ? 'onboarding-pill-active' : ''}`}
                    >
                      {chip}
                    </button>
                  ))}
                </div>
                <input
                  type="text"
                  value={homeFoodOther}
                  onChange={(e) => setHomeFoodOther(e.target.value)}
                  placeholder="Or type your own..."
                  className="onboarding-input onboarding-input-small"
                />
              </div>
              <button
                type="button"
                onClick={handleNext}
                className="onboarding-cta"
              >
                Continue <ChevronRight size={22} />
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Goal */}
        {step === 2 && (
          <div className="onboarding-step animate-onboarding-step">
            <div className="onboarding-header onboarding-header-step">
              <h1 className="onboarding-title">
                Hi, <span className="onboarding-title-accent">{name.trim() || 'there'}</span>!
              </h1>
              <p className="onboarding-subtitle">
                What brings you to PalatePal today?
              </p>
            </div>
            <div className="onboarding-form">
              <div className="onboarding-form-group">
                <label className="onboarding-label">What brings you to PalatePal?</label>
                <select
                  value={goal}
                  onChange={(e) => setGoal(e.target.value)}
                  className="onboarding-select"
                >
                  {GOAL_OPTIONS.map((opt) => (
                    <option key={opt.value || 'empty'} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </div>
              <div className="onboarding-form-group">
                <label className="onboarding-label">Any cuisines you want to like but don't know how to start?</label>
                <div className="onboarding-pills">
                  {CUISINES_WANT_OPTIONS.map((cuisine) => (
                    <button
                      key={cuisine}
                      type="button"
                      onClick={() => toggleCuisineWant(cuisine)}
                      className={`onboarding-pill ${cuisinesWantToTry.includes(cuisine) ? 'onboarding-pill-active' : ''}`}
                    >
                      {cuisine}
                    </button>
                  ))}
                </div>
                <p className="onboarding-hint">Pick any that interest you.</p>
              </div>
              <div className="onboarding-actions">
                <button type="button" onClick={handleBack} className="onboarding-btn-back">
                  <ChevronLeft size={20} /> Back
                </button>
                <button type="button" onClick={handleNext} className="onboarding-cta">
                  Continue <ChevronRight size={20} />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Allergens + Finish */}
        {step === 3 && (
          <div className="onboarding-step animate-onboarding-step">
            <div className="onboarding-header onboarding-header-step">
              <h1 className="onboarding-title">
                Almost there
              </h1>
              <p className="onboarding-subtitle">
                Any dietary restrictions we should remember? We'll use this to tailor your recommendations.
              </p>
            </div>
            <div className="onboarding-form">
              <div className="onboarding-pills">
                {ALLERGEN_OPTIONS.map((allergen) => (
                  <button
                    key={allergen}
                    type="button"
                    onClick={() => toggleAllergen(allergen)}
                    className={`onboarding-pill ${selectedAllergens.includes(allergen) ? 'onboarding-pill-active' : ''}`}
                  >
                    {allergen}
                  </button>
                ))}
              </div>
              <p className="onboarding-hint">Select any that apply, or skip.</p>
              <div className="onboarding-actions">
                <button type="button" onClick={handleBack} className="onboarding-btn-back">
                  <ChevronLeft size={20} /> Back
                </button>
                <button type="button" onClick={handleFinish} className="onboarding-cta">
                  <Sparkles size={20} />
                  Get started
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Onboarding;
