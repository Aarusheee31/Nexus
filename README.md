# 🍽️ FlavorBridge - Taste Translator

A modern food-tech web application built with React that helps you translate your comfort food flavors into dishes from new cuisines. Perfect for hackathon demos and presentations!

## 📁 Project Structure

```
flavor-bridge-app/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/
│   │   ├── Sidebar.js          # Interactive sidebar component
│   │   └── Sidebar.css         # Sidebar styles
│   ├── pages/
│   │   ├── Home.js             # Flavor translator input
│   │   ├── Results.js          # Match results display
│   │   ├── Recipes.js          # Recipe browser
│   │   ├── RecipeDetail.js     # Individual recipe view
│   │   ├── Restaurants.js      # Restaurant finder
│   │   ├── Allergens.js        # Allergen guide
│   │   ├── Profile.js          # User profile
│   │   ├── Settings.js         # App settings
│   │   └── Pages.css           # All page styles
│   ├── data/
│   │   └── mockData.js         # Mock data and constants
│   ├── App.js                  # Main app component
│   ├── App.css                 # App layout styles
│   ├── index.js                # React entry point
│   └── index.css               # Global styles
├── package.json                # Dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file!
```

## 🚀 Features

### Core Features
- **Flavor Translator** - Input comfort dish, discover similar dishes in new cuisines
- **Recipe Finder** - Browse and view detailed recipes
- **Restaurant Finder** - Find nearby restaurants with match scores
- **Allergen Guide** - Get safe substitutes for allergens
- **Profile Management** - Track stats and manage allergens
- **Settings** - Customize preferences

### UI/UX Features
- Mobile-first responsive design
- Interactive collapsible sidebar (works like ChatGPT/Claude)
- Smooth animations and transitions
- Beautiful gradient backgrounds
- Progress bar animations
- Touch-friendly on mobile

## 📦 Installation & Setup

1. **Extract/Clone the project**
   ```bash
   cd flavor-bridge-app
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

4. **Open browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🛠️ Tech Stack

- **React 18** - UI framework
- **Lucide React** - Beautiful icon library
- **CSS3** - Custom styling with gradients & animations
- **React Scripts** - Build tooling

## 🎨 Design System

### Color Palette
- Primary Green: `#2E7D32`
- Accent Amber: `#FFB703`
- Background: `#F7F7F5` with gradients
- Text Primary: `#1E1E1E`
- Text Muted: `#6B6B6B`

### Key Components
- **Sidebar** - Reusable navigation component
- **Pages** - Separate page components for each screen
- **Mock Data** - Centralized data management

## 📱 Responsive Design

- Desktop: Full sidebar + centered content (max-width 640px)
- Mobile: Collapsible sidebar with hamburger menu
- Tablet: Optimized layouts
- Touch-friendly buttons and interactions

## 🎯 Perfect For

- Hackathon demos
- Food-tech presentations
- UI/UX portfolio projects
- React learning projects

## 📝 Available Scripts

- `npm start` - Run development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

## 🔧 Customization

### Adding New Pages
1. Create new component in `src/pages/`
2. Import in `App.js`
3. Add route handler
4. Update sidebar in `Sidebar.js`

### Modifying Data
- Edit `src/data/mockData.js` for mock data
- Add new constants or data structures as needed

### Styling
- Global styles: `src/index.css`
- Layout: `src/App.css`
- Sidebar: `src/components/Sidebar.css`
- Pages: `src/pages/Pages.css`

## 🤝 Contributing

Feel free to fork, modify, and use this project!

## 📄 License

MIT License - free to use for your projects!

---

Built with ❤️ for food lovers exploring new cuisines
