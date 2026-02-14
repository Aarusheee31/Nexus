import React from 'react';
import { Utensils } from 'lucide-react';
import './Pages.css';

const Settings = ({ settings, updateSettings }) => {
  const SettingToggle = ({ label, description, checked, onChange }) => (
    <div className="setting-toggle-row">
      <div className="setting-toggle-info">
        <p className="setting-toggle-label">{label}</p>
        <p className="setting-toggle-description">{description}</p>
      </div>
      <button
        onClick={() => onChange(!checked)}
        className={`toggle-switch ${checked ? 'toggle-active' : ''}`}
      >
        <div className="toggle-slider" />
      </button>
    </div>
  );

  return (
    <div className="screen-content animate-fade-in">
      <div className="screen-header-center">
        <h1 className="main-title">Settings</h1>
        <p className="subtitle">Customize your experience</p>
      </div>

      <div className="settings-section">
        <div className="section-header-green">
          <h3>Preferences</h3>
        </div>
        <div className="settings-body">
          <div className="form-group">
            <label className="form-label">Spice Level</label>
            <select
              value={settings.spiceLevel}
              onChange={(e) => updateSettings({ spiceLevel: e.target.value })}
              className="form-select"
            >
              <option>Mild</option>
              <option>Medium</option>
              <option>Hot</option>
              <option>Extra Hot</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Dietary Preference</label>
            <select
              value={settings.dietaryPreference}
              onChange={(e) => updateSettings({ dietaryPreference: e.target.value })}
              className="form-select"
            >
              <option>None</option>
              <option>Vegetarian</option>
              <option>Vegan</option>
              <option>Pescatarian</option>
              <option>Gluten-Free</option>
              <option>Lactose-Free</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Language</label>
            <select
              value={settings.language}
              onChange={(e) => updateSettings({ language: e.target.value })}
              className="form-select"
            >
              <option>English</option>
              <option>Hindi</option>
            </select>
          </div>
        </div>
      </div>

      <div className="settings-section">
        <div className="section-header-green">
          <h3>Features</h3>
        </div>
        <div className="settings-body">
          <SettingToggle
            label="Push Notifications"
            description="Get updates on new recipes and restaurants"
            checked={settings.notifications}
            onChange={(checked) => updateSettings({ notifications: checked })}
          />
          <SettingToggle
            label="Show Nutrition Info"
            description="Display calories and macros in recipes"
            checked={settings.showNutrition}
            onChange={(checked) => updateSettings({ showNutrition: checked })}
          />
          <SettingToggle
            label="Auto-detect Location"
            description="Automatically find nearby restaurants"
            checked={settings.autoDetectLocation}
            onChange={(checked) => updateSettings({ autoDetectLocation: checked })}
          />
        </div>
      </div>

      <div className="about-card">
        <Utensils size={48} className="about-icon" />
        <p className="about-version">PalatePal v1.0</p>
        <p className="about-tagline">Connecting world...one ingredient at a time</p>
      </div>
    </div>
  );
};

export default Settings;
