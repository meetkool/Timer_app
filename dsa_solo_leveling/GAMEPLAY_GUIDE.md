# 🎮 DSA Solo Leveling - Complete Gameplay Guide

Welcome to your programming journey! Transform your DSA learning into an epic Solo Leveling adventure!

## 🚀 Getting Started

### Launch the Game
```bash
# Run this in the dsa_solo_leveling directory
python run_game.py
```

### First Launch
- You start as an **E-Rank Hunter** at Level 1
- All dungeons (learning steps) are available to explore
- Your player stats panel shows your current rank and progress

## 🏰 Main Dashboard - Dungeon Selection

### Overview
The main screen shows all available **dungeons** (DSA learning steps) arranged in cards:

1. **Learn the Basics** - Programming fundamentals
2. **Sorting Techniques** - Various sorting algorithms  
3. **Array Problems** - Easy to hard array challenges
4. **Binary Search** - Search algorithms and techniques
5. **Strings** - String manipulation problems
6. **Linked Lists** - Linked list operations
7. **Stacks & Queues** - Stack and queue problems
8. **Recursion** - Recursive problem solving
9. **Greedy Algorithms** - Greedy approach problems
10. **Dynamic Programming** - DP concepts and problems
11. **Trees** - Tree data structure and traversals
12. **Graphs** - Graph algorithms and problems
13. **Tries** - Trie data structure problems
14. **Advanced Topics** - Complex algorithms
15. **Sliding Window** - Two-pointer techniques
16. **Heaps** - Priority queue problems
17. **Segment Trees** - Advanced tree structures
18. **Additional Topics** - Miscellaneous advanced concepts

### Navigation
- **🖱️ Scroll Mouse Wheel**: Navigate through all 18 dungeons
- **🖱️ Click Cards**: Enter a dungeon to see its quests
- **📊 Progress Bars**: Each card shows completion percentage
- **👤 Player Panel**: View your rank, level, XP, and stats

## ⚔️ Quest View - Inside a Dungeon

### When You Enter a Dungeon:
1. **Step Title**: Shows which dungeon you're in
2. **Overall Progress Bar**: Your completion status for this step
3. **Sub-step Dropdown**: Choose different sub-topics
4. **Quest List**: Individual topics/questions to complete

### Sub-steps Example (for "Learn the Basics"):
- **Things to Know in C++/Java/Python** - Basic syntax
- **Build-up Logical Thinking** - Problem-solving fundamentals  
- **Learn STL/Collections** - Standard libraries
- **Know Basic Maths** - Mathematical concepts
- **Learn Basic Recursion** - Recursive thinking
- **Learn Basic Hashing** - Hash tables and maps

### Interactive Elements:
- **☐ Checkboxes**: Click to mark topics as completed
- **🔄 Status Cycling**: 
  - Empty → In Progress (yellow) → Completed (green)
- **🖱️ Mouse Wheel**: Scroll through long topic lists
- **📈 Real-time Progress**: Watch your completion percentage update

### Topic Status Colors:
- **⚪ White**: Available/Not started
- **🟡 Yellow**: In Progress  
- **🟢 Green**: Completed
- **🔴 Red**: Different difficulty levels

## 🏆 Leveling System

### Experience Points (XP):
- **Beginner (0)**: 10 XP + 5 × difficulty
- **Easy (1)**: 15 XP + 5 × difficulty  
- **Medium (2)**: 25 XP + 5 × difficulty
- **Hard (3)**: 40 XP + 5 × difficulty

### Hunter Ranks:
- **E-Rank Hunter**: Levels 1-9 (Starting rank)
- **D-Rank Hunter**: Levels 10-19
- **C-Rank Hunter**: Levels 20-29  
- **B-Rank Hunter**: Levels 30-39
- **A-Rank Hunter**: Levels 40-49
- **S-Rank Hunter**: Level 50+ (Master level!)

### Level Up Calculation:
- **Level 1**: Requires 100 XP
- **Level 2**: Requires 200 XP  
- **Level 3**: Requires 300 XP
- And so on...

## 🎯 How to Play Effectively

### 1. **Start with Basics**
- Begin with "Learn the Basics" dungeon
- Complete topics systematically
- Don't skip foundational concepts

### 2. **Track Your Progress**
- Watch your XP bar fill up
- Aim for consistent daily progress
- Try to maintain a streak

### 3. **Use External Resources** - Specific Button Functions!
- **🔗 Solve**: Opens LeetCode problem directly (`lc_link`) - **ORANGE BUTTON**
- **📺 Solution**: Opens YouTube video explanation (`yt_link`) - **RED BUTTON**  
- **📖 Blog**: Opens editorial/detailed solution (`editorial_link`) - **BLUE BUTTON**
- **📝 Tutorial**: Access tutorial posts and articles (`post_link`) - **YELLOW BUTTON**
- **🚀 Practice**: Additional practice platform (`plus_link`) - **PURPLE BUTTON**
- **🏢 Company Tags**: See which companies ask these questions (when available)

### 4. **Strategic Progression**
```
Recommended Path:
1. Learn the Basics (Master fundamentals)
2. Sorting Techniques (Essential algorithms)
3. Array Problems (Build problem-solving skills)
4. Binary Search (Learn efficient searching)
5. Strings (Text processing)
6. Linked Lists (Dynamic data structures)
7. Stacks & Queues (LIFO/FIFO concepts)
8. Recursion (Divide and conquer)
9. Advanced topics as you progress...
```

## 🎮 Controls & Shortcuts

### Mouse Controls:
- **Left Click**: Select, toggle checkboxes, navigate
- **Left Click on "Solve" buttons**: Open primary resource link instantly  
- **Left Click on tooltip buttons**: Open specific resources (Video, Code, Read, Guide, Practice)
- **Mouse Wheel**: Scroll through lists and dungeons
- **Hover**: Show detailed **clickable** tooltips with comprehensive topic information
- **Smart Click Areas**: Checkboxes, solve buttons, and tooltips all have separate click zones

### Keyboard Shortcuts:
- **ESC**: Go back to previous screen
- **ESC** (on main screen): Quit application
- **F11**: Toggle fullscreen mode
- **T**: Toggle tooltips on/off (in quest view)

## 📊 Progress Tracking

### What Gets Saved:
- ✅ Topic completion status
- 📈 Experience points and level  
- 🏆 Current rank
- 📊 Total completed topics
- 🔥 Completion streak

### Save Files:
- `progress.json`: Your topic completion data
- `player_stats.json`: Level, XP, and rank data

## 🆕 Enhanced Features

### 📋 **Detailed Topic Information**
- **🆔 Topic IDs**: Unique identifiers for each question
- **📊 Serial Numbers**: Sequential numbering within sub-steps
- **🏷️ Topic Tags**: Categorization labels (e.g., "Introduction to DSA")
- **🎯 Difficulty Badges**: Visual indicators (BGN/EZ/MED/HRD)
- **🏢 Company Indicators**: Shows when companies have asked this question

### 🖱️ **Interactive Tooltips** - NOW CLICKABLE!
- **Hover over topics** to see detailed popup with comprehensive information
- **All JSON fields displayed**: ID, step info, difficulty, status, company tags
- **✨ CLICKABLE resource buttons** in tooltip:
  - 📺 **Video** - Opens YouTube tutorial
  - 💻 **Code** - Opens LeetCode problem  
  - 📖 **Read** - Opens editorial/solution
  - 📝 **Guide** - Opens tutorial article
  - 🚀 **Practice** - Opens practice platform
- **Orange "Solve" button** - Opens primary resource (LeetCode > YouTube > Tutorial)
- **Press 'T'** to toggle tooltips on/off in quest view

### 🎯 **Quick Action Buttons**
- **"Solve" button** on each topic row - instant access to primary resource
- **Difficulty labels** showing "Beginner", "Easy", "Medium", "Hard" in color
- **Main "Solve" button** on topic detail pages (top-right corner)
- **Smart button positioning** - won't interfere with checkbox functionality

### 📈 **Enhanced Progress Tracking**
- **Completion percentages** for each sub-step with color coding
- **Difficulty distribution** showing BGN/EZ/MED/HRD counts for each sub-step
- **Better text wrapping** on dungeon cards (no more overlapping text!)
- **Scroll indicators** when content extends beyond screen
- **Serial number indicators** (#1, #2, #3...) for easy reference

### 🔗 **Complete Resource Access**
All 5 types of external links when available:
- 📺 **Video tutorials** (YouTube)
- 💻 **LeetCode problems** 
- 📖 **Editorial solutions**
- 📝 **Tutorial articles**
- 🚀 **Practice platforms**

## 💡 Pro Tips

### For Efficient Learning:
1. **Daily Consistency**: Complete at least 2-3 topics daily
2. **Mixed Difficulty**: Balance easy and challenging topics
3. **Resource Usage**: Always check external links for deeper understanding
4. **Progressive Difficulty**: Complete easier dungeons before harder ones
5. **Review Completed**: Revisit completed topics to reinforce learning

### For Fast Leveling:
1. **Focus on Hard Topics**: They give more XP
2. **Complete Full Dungeons**: Systematic completion
3. **Use Dropdown Navigation**: Quickly switch between sub-topics
4. **Track Your Rank Progress**: Aim for next rank milestone

## 🔧 Troubleshooting

### Common Issues:
- **Can't see all dungeons**: Use mouse wheel to scroll
- **Application not responding**: Check console for errors
- **Progress not saving**: Ensure write permissions in folder
- **Fonts not loading**: Restart the application

### Performance Tips:
- **Close other applications**: For smooth scrolling
- **Fullscreen mode (F11)**: Better gaming experience
- **Regular saves**: Progress saves automatically

## 🎊 Achievement Milestones

### Beginner Achievements:
- ✨ **First Steps**: Complete your first topic (10 XP)
- 🔥 **Getting Started**: Complete 10 topics
- 📚 **Knowledge Seeker**: Complete first full dungeon

### Intermediate Achievements:
- ⚡ **Speed Learner**: Reach D-Rank Hunter
- 🧠 **Problem Solver**: Complete 100 topics
- 🎯 **Focused**: Complete 3 full dungeons

### Advanced Achievements:
- 👑 **Algorithm Master**: Reach S-Rank Hunter
- 🏆 **Completionist**: Finish all 18 dungeons
- ⭐ **Solo Leveling Legend**: Max level with all topics completed

---

## 🎮 Ready to Start Your Journey?

Launch the game and begin your transformation from E-Rank to S-Rank Hunter! Remember, every expert was once a beginner. Your programming skills will grow with each topic you conquer.

**Good luck, Hunter! May your algorithms be efficient and your code bug-free!** ⚔️💻✨

---

*For technical issues or suggestions, check the README.md file or create an issue on the project repository.*