# 🎮 DSA Solo Leveling

A gamified Data Structures and Algorithms learning application inspired by the popular manhwa "Solo Leveling". Transform your programming journey into an epic adventure where you level up by conquering algorithmic challenges!

## 🌟 Features

### 🏰 Dungeon System (Learning Modules)
- **Step-based Learning**: Progress through structured learning paths
- **Sub-dungeons**: Each step contains multiple sub-topics to master
- **Quest System**: Individual topics presented as conquerable quests

### 📊 Progress Tracking
- **Visual Progress Bars**: See your completion status at a glance
- **Checklist System**: Mark topics as completed, in-progress, or pending
- **Persistent Progress**: Your achievements are saved automatically

### 🏆 Solo Leveling Experience
- **Hunter Ranking System**: Start as E-Rank and climb to S-Rank
- **Experience Points**: Gain XP by completing topics
- **Level Progression**: Level up and unlock new ranks
- **Statistics Dashboard**: Track your learning journey

### 🎨 Immersive UI
- **Dark Theme**: Solo Leveling-inspired color scheme
- **Interactive Components**: Hover effects and smooth animations
- **Responsive Design**: Clean and intuitive interface
- **Dropdown Navigation**: Easy access to different learning modules

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pygame library

### Installation

1. **Clone or download** the project to your computer
2. **Navigate** to the `dsa_solo_leveling` directory
3. **Run the launcher**:
   ```bash
   python run_game.py
   ```

The launcher will automatically:
- Install required dependencies (pygame)
- Copy the DSA questions data file
- Launch the application

### Manual Installation
If you prefer manual setup:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure `dsa_queastions.json` is in the project directory

3. Run the application:
   ```bash
   python main.py
   ```

## 🎮 How to Play

### 🏠 Main Dashboard
- View all available learning modules (dungeons)
- See your current rank and level
- Check overall progress for each step
- Click on any step card to enter that dungeon

### 🗡️ Quest View (Step Details)
- Browse topics within the selected step
- Use dropdown to switch between sub-steps
- Click checkboxes to mark topics as completed
- Scroll through long lists of topics
- Track sub-step progress with visual indicators

### 📚 Topic Details
- View detailed information about specific topics
- Access external resources (YouTube, LeetCode, Editorial links)
- Quick navigation back to quest view

### 🎯 Controls
- **Mouse**: Navigate and interact with all elements
- **Mouse Wheel**: Scroll through topic lists
- **ESC**: Go back to previous screen or quit
- **F11**: Toggle fullscreen mode

## 🏗️ Architecture (SOLID Principles)

This project follows SOLID principles for clean, maintainable code:

### Single Responsibility Principle
- `DataLoader`: Handles JSON data loading
- `ProgressTracker`: Manages progress persistence  
- `PlayerStats`: Handles player statistics
- Each UI component has a specific purpose

### Open/Closed Principle
- `UIComponent` base class allows easy extension
- `DataLoader` abstract class supports different data sources
- Views can be extended without modifying existing code

### Liskov Substitution Principle
- All UI components inherit properly from `UIComponent`
- View classes can be substituted seamlessly

### Interface Segregation Principle
- Focused interfaces for different responsibilities
- Components only depend on methods they use

### Dependency Inversion Principle
- High-level modules depend on abstractions
- Easy to swap implementations (e.g., data sources)

## 📁 Project Structure

```
dsa_solo_leveling/
├── models/
│   └── data_models.py      # Data structures and business logic
├── ui/
│   ├── components.py       # Reusable UI components
│   ├── views.py           # Main application screens
│   └── theme.py           # Visual styling and effects
├── main.py                # Main application entry point
├── run_game.py           # Launcher script
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## 🎨 Theming

The application uses a dark, cyberpunk-inspired theme reminiscent of Solo Leveling:

- **Color Scheme**: Dark backgrounds with blue accents
- **Typography**: Clean, readable fonts
- **Visual Effects**: Subtle gradients and hover effects
- **Rank Colors**: Different colors for each hunter rank
- **Progress Indicators**: Color-coded based on completion status

## 💾 Data Persistence

- **Progress Tracking**: Automatically saves topic completion status
- **Player Stats**: Persistent level, experience, and rank data
- **Files Created**: `progress.json`, `player_stats.json`

## 🔧 Customization

### Adding New Themes
Modify `ui/theme.py` to create new color schemes and visual effects.

### Extending Components
Create new UI components by inheriting from `UIComponent` in `ui/components.py`.

### Custom Data Sources
Implement the `DataLoader` interface to support different data formats.

## 🤝 Contributing

This project demonstrates SOLID principles and clean architecture. Feel free to:
- Add new features following the established patterns
- Improve the visual design
- Optimize performance
- Add new data sources

## 📜 License

This project is for educational purposes. The Solo Leveling theme is inspired by the manhwa but this is an independent learning tool.

## 🎖️ Rank System

- **E-Rank Hunter**: Levels 1-9 (Beginner)
- **D-Rank Hunter**: Levels 10-19 (Getting Started)
- **C-Rank Hunter**: Levels 20-29 (Intermediate)
- **B-Rank Hunter**: Levels 30-39 (Advanced)
- **A-Rank Hunter**: Levels 40-49 (Expert)
- **S-Rank Hunter**: Level 50+ (Master)

## 🎯 Learning Path

The application covers comprehensive DSA topics:
1. **Learn the Basics**: Fundamentals and basic programming concepts
2. **Sorting Techniques**: Various sorting algorithms
3. **Array Problems**: Easy to hard array challenges
4. **Binary Search**: Search algorithms and techniques
5. **And many more!**

Start your journey and become the strongest programmer! 💪⚔️