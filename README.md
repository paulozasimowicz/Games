# Games

A workspace for creating and experimenting with game ideas from scratch. This repository provides an organized structure to easily work on different game projects.

## 📁 Repository Structure

```
Games/
├── games/          # Your individual game projects
├── templates/      # Starter templates for quick project setup
├── shared/         # Shared resources across projects
│   ├── assets/    # Common images, sounds, fonts
│   ├── utils/     # Reusable utility code
│   └── libs/      # Shared libraries
├── docs/          # Documentation and guides
└── .gitignore     # Ignores build artifacts, dependencies, etc.
```

## 🚀 Getting Started

### Creating a New Game

1. **Use a template** (recommended for beginners):
   ```bash
   cp -r templates/basic-html5-game games/my-awesome-game
   cd games/my-awesome-game
   ```

2. **Start from scratch**:
   ```bash
   mkdir games/my-new-game
   cd games/my-new-game
   # Add your game files here
   ```

3. **Check the templates directory** for different starter projects

### Available Templates

- **basic-html5-game**: A simple HTML5 Canvas game with player movement and game loop

More templates coming soon!

## 📚 Documentation

Check the `docs/` directory for:
- Development guides
- Best practices
- Tutorials and resources

## 🎮 Games Directory

Each game project should be self-contained with its own:
- Source code
- Assets
- Dependencies
- Documentation
- Build/run instructions

See `games/README.md` for more details.

## 🔧 Shared Resources

The `shared/` directory contains reusable resources:
- **assets/**: Common sprites, sounds, and other media
- **utils/**: Helper functions and common game code
- **libs/**: Shared libraries and frameworks

## 📝 Best Practices

- Keep each game project independent
- Use meaningful names for your projects
- Include a README.md in each game
- Reuse shared resources when possible
- Document your code and design decisions

## 🤝 Contributing

This is a personal workspace for game development experimentation. Feel free to:
- Try different game engines
- Experiment with new ideas
- Learn and improve

## 📄 License

See LICENSE file for details.
