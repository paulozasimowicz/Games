# Games

This directory contains individual game projects. Each game should have its own subdirectory.

## Structure

```
games/
├── my-game-1/
│   ├── src/
│   ├── assets/
│   ├── README.md
│   └── ...
├── my-game-2/
│   ├── src/
│   ├── assets/
│   ├── README.md
│   └── ...
```

## Getting Started

1. Create a new folder for your game project
2. Copy a template from the `../templates/` directory or start from scratch
3. Add your game-specific code, assets, and documentation
4. Each game should be self-contained with its own dependencies and build configuration

## Best Practices

- Keep each game project independent and self-contained
- Use meaningful names for your game directories
- Include a README.md in each game with:
  - Game description
  - How to build/run
  - Dependencies
  - Controls/gameplay instructions
- Reuse shared resources from the `../shared/` directory when possible
