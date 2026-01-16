# Pygame Sprites Library

A minimal PyGame utility for extracting sprites from 2D sprite sheets.

## What is this?

A lightweight Python library that helps you extract individual sprites/tiles from sprite sheets and organize them in a 2D grid. Built specifically for PyGame with full type safety.

## Basic Usage

```python
import pygame
from spritesheet import SpriteSheet

pygame.init()

sheet = SpriteSheet("sprites.png", tile_size=(32, 32))
sprite = sheet[0, 0]  # Get sprite at row 0, column 0
```

## Features

- Extract sprites from grid-based sprite sheets
- Multiple transparency options
- Flexible indexing (coordinates, slices, integers)
- Export sprites to PNG
- Full type hints with runtime checking

## Requirements

- Python 3.8+
- PyGame 2.0+
- beartype

## License

MIT

Copyright (c) 2026 Misbahur Rahman

See [LICENSE](LICENSE) for full license text.