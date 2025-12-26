# Shared Resources

This directory contains resources that can be shared across multiple game projects.

## Structure

```
shared/
├── assets/      # Shared game assets (sprites, sounds, fonts, etc.)
├── utils/       # Utility functions and helper code
└── libs/        # Common libraries and dependencies
```

## Purpose

- **Reduce duplication**: Store commonly used assets and code in one place
- **Consistency**: Maintain consistent look and feel across games
- **Efficiency**: Don't reinvent the wheel for each game project

## Usage

### Assets (`assets/`)
Store reusable game assets like:
- Common sprites and textures
- Sound effects and music
- Fonts
- Icons
- UI elements

### Utils (`utils/`)
Store reusable utility code like:
- Math helpers (vector operations, collision detection)
- Input handlers
- Audio managers
- Save/load systems
- Common game algorithms

### Libs (`libs/`)
Store commonly used libraries:
- Game engines (if self-contained)
- Physics engines
- Particle systems
- Custom frameworks

## Best Practices

- Document all shared resources
- Version control is important here - breaking changes affect all games
- Consider creating a simple API or documentation for shared utilities
- Only add truly reusable content to avoid clutter
