import React from 'react';
import { UtensilsCrossed, Home, BookOpen, MapPin, AlertCircle, User, Settings, X, Lightbulb } from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ currentScreen, setCurrentScreen, sidebarOpen, setSidebarOpen }) => {
  const navItems = [
    { id: 'home', label: 'Flavour Translator', icon: <Home size={20} /> },
    { id: 'recipes', label: 'Recipe Finder', icon: <BookOpen size={20} /> },
    { id: 'restaurants', label: 'Restaurants', icon: <MapPin size={20} /> },
    { id: 'allergens', label: 'Allergen Guide', icon: <AlertCircle size={20} /> },
    { id: 'profile', label: 'Profile', icon: <User size={20} /> },
    { id: 'settings', label: 'Settings', icon: <Settings size={20} /> }
  ];

  const handleNavClick = (screenId) => {
    setCurrentScreen(screenId);
    setSidebarOpen(false);
  };

  return (
    <>
      
      {sidebarOpen && (
        <div 
          className="mobile-overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}
      
     
      <div className={`sidebar ${sidebarOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-content">
          
          <div className="sidebar-header">
            <div className="sidebar-logo">
              <div className="logo-icon">
                <UtensilsCrossed size={30} />
              </div>
              <div className="logo-text">
                <h2>PalatePal</h2>
                <p>Translating Taste</p>
              </div>
            </div>
            <button 
              onClick={() => setSidebarOpen(false)}
              className="sidebar-close"
            >
              <X size={15} />
            </button>
          </div>

          
          <nav className="nav-items">
            {navItems.map(item => (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`nav-item ${currentScreen === item.id ? 'nav-item-active' : ''}`}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </button>
            ))}
          </nav>

          
          <div className="sidebar-footer">
            <div className="tip-card-sidebar">
              <Lightbulb size={18} />
              <div>
                <p className="tip-title">Pro Tip</p>
                <p className="tip-text">Try translating comfort foods from your childhood!</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
