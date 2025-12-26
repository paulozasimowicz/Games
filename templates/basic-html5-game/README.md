# Basic HTML5 Game Template

A simple starter template for creating HTML5 Canvas-based games using vanilla JavaScript.

## Features

- Basic game loop with delta time
- Keyboard input handling (Arrow keys and WASD)
- Player movement
- Scorekeeping
- Canvas rendering

## Getting Started

1. Copy this template to your game directory:
   ```bash
   cp -r templates/basic-html5-game games/my-game-name
   ```

2. Open `index.html` in a web browser to test the game

3. Start customizing:
   - Edit `src/game.js` to add your game logic
   - Add assets to the `assets/` directory
   - Modify styling in `index.html`

## File Structure

```
basic-html5-game/
├── index.html          # Main HTML file with canvas and styling
├── src/
│   └── game.js        # Game logic and engine
├── assets/
│   ├── images/        # Game images and sprites
│   └── sounds/        # Audio files
└── README.md          # This file
```

## Development

This template uses vanilla JavaScript with no external dependencies. To develop:

1. Open `index.html` directly in a browser, or
2. Use a local development server:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Node.js (if you have http-server installed)
   npx http-server
   ```

3. Access the game at `http://localhost:8000`

## Customization Ideas

- Add enemies or obstacles
- Implement collision detection
- Add power-ups or collectibles
- Create multiple levels
- Add sound effects and music
- Implement a start/pause/game over screen
- Add particle effects
- Create sprite animations

## Resources

- [MDN Canvas Tutorial](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial)
- [Game Loop Pattern](https://gameprogrammingpatterns.com/game-loop.html)
- Free game assets: [OpenGameArt.org](https://opengameart.org/)

## License

Use this template freely for your game projects!
