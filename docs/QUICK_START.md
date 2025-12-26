# Quick Start Guide

Welcome to your game development workspace! This guide will help you get started quickly.

## Environment Setup

### Prerequisites

Depending on what type of games you want to create, you may need:

#### Web-Based Games (HTML5/JavaScript)
- A modern web browser (Chrome, Firefox, Safari)
- A code editor (VS Code, Sublime Text, etc.)
- Optional: Node.js for package management

#### Python Games
- Python 3.x
- pip (Python package manager)
- pygame: `pip install pygame`

#### Unity Games
- Unity Hub
- Unity Editor (latest LTS version)
- Visual Studio or VS Code

#### Godot Games
- Godot Engine (download from godotengine.org)

#### Unreal Engine
- Epic Games Launcher
- Unreal Engine
- Visual Studio (Windows) or Xcode (Mac)

## Creating Your First Game

### Option 1: Using a Template

1. Choose a template from `templates/`:
   ```bash
   ls templates/
   ```

2. Copy it to the `games/` directory:
   ```bash
   cp -r templates/basic-html5-game games/my-first-game
   ```

3. Start developing:
   ```bash
   cd games/my-first-game
   # Open index.html in a browser for HTML5 games
   # Or follow the template's README for other types
   ```

### Option 2: Starting From Scratch

1. Create a new directory:
   ```bash
   mkdir games/my-game
   cd games/my-game
   ```

2. Initialize your project (example for different types):

   **HTML5 Game:**
   ```bash
   touch index.html
   mkdir src assets
   touch src/game.js
   ```

   **Python/Pygame:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install pygame
   touch main.py
   ```

   **Node.js/TypeScript:**
   ```bash
   npm init -y
   npm install --save-dev typescript
   mkdir src
   touch src/game.ts
   ```

3. Add a README.md describing your game

## Project Structure Best Practices

Every game project should have:

```
my-game/
├── README.md           # Description, how to run, controls
├── src/               # Source code
├── assets/            # Game assets (images, sounds, etc.)
├── [config files]     # package.json, requirements.txt, etc.
└── [build files]      # Vary by platform
```

## Running Your Games

### HTML5 Games
- **Simple:** Open `index.html` directly in a browser
- **With server:** 
  ```bash
  python -m http.server 8000
  # Or
  npx http-server
  ```

### Python/Pygame
```bash
python main.py
```

### Unity
- Open project in Unity Editor
- Press Play button

### Godot
- Import project in Godot
- Press F5 or Play button

## Using Shared Resources

The `shared/` directory contains reusable content:

### Using Shared Assets
```javascript
// In your game code
const sharedImage = '../../../shared/assets/images/sprite.png';
```

### Using Shared Utils
```javascript
// Copy or import shared utilities
import { collision } from '../../../shared/utils/collision.js';
```

## Development Workflow

1. **Plan**: Sketch out your game idea
2. **Prototype**: Start with basic mechanics
3. **Iterate**: Add features incrementally
4. **Test**: Play your game frequently
5. **Polish**: Add juice, sounds, effects
6. **Document**: Keep README updated

## Tips for Success

- **Start small**: Begin with simple mechanics
- **Iterate quickly**: Get something playable fast
- **Learn incrementally**: Don't try to learn everything at once
- **Reuse code**: Use templates and shared resources
- **Have fun**: Experiment and be creative!

## Common Commands

### Git
```bash
# Check what files changed
git status

# Commit your changes
git add .
git commit -m "Add new feature"

# Push to GitHub
git push
```

### File Management
```bash
# Copy template
cp -r templates/[template] games/[new-game]

# Create new directories
mkdir -p games/my-game/{src,assets,docs}

# Remove a project
rm -rf games/old-game
```

## Resources

### Learning
- [MDN Web Games](https://developer.mozilla.org/en-US/docs/Games)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Unity Learn](https://learn.unity.com/)
- [Godot Docs](https://docs.godotengine.org/)

### Assets
- [OpenGameArt.org](https://opengameart.org/) - Free game art
- [Freesound.org](https://freesound.org/) - Free sound effects
- [Itch.io](https://itch.io/game-assets) - Game assets (free & paid)

### Communities
- Reddit: r/gamedev, r/unity3d, r/godot
- Discord: Various game dev servers
- Forums: Unity Forums, Godot Forum

## Troubleshooting

### Common Issues

**"Cannot load module" errors:**
- Check file paths
- Ensure dependencies are installed
- Use a local server for HTML5 games

**Build/compile errors:**
- Check prerequisites are installed
- Read error messages carefully
- Search the error online

**Assets not loading:**
- Verify file paths are correct
- Check file names match (case-sensitive)
- Ensure files are in the right directory

## Next Steps

1. Explore the templates in `templates/`
2. Read the documentation in `docs/`
3. Create your first game!
4. Share your progress

Happy game developing! 🎮
