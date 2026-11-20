# Turtle 3D Engine

3D rendering engine built with Python's `turtle` graphics library.

## Overview

This project implements a real-time 3D engine using only Python's built-in `turtle` module. It features:

- **3D Rendering**: Triangle-based rasterization with depth sorting
- **Camera Controls**: First-person style camera movement and rotation
- **Lighting**: Directional lighting with normal-based brightness calculation
- **Fog Effects**: Distance-based fog for depth perception
- **OBJ Model Loading**: Support for loading 3D models in OBJ format
- **Backface Culling**: Optimized rendering by culling back-facing triangles

## Requirements

- Python 3.x
- `turtle` module (built-in)
- `keyboard` module (for controls)
- Optional: `pygltflib` for GLTF support

## Installation

```bash
pip install keyboard
pip install pygltflib  # optional for GLTF support
```

## Usage

### Basic Rendering (OBJ Files)

```bash
python render.py
```

### Controls

- **W/A/S/D** - Move forward, left, backward, right
- **Space/Shift** - Move up/down (vertical movement)
- **Arrow Keys** - Rotate camera (up/down/left/right)

### Example Model

The repository includes a monkey model (`monkey.obj`) for demonstration. Simply run `render.py` to see it in action.

## Project Structure

```
turtle-3d-engine/
├── render.py          # Main rendering engine with camera, lighting, and drawing
├── obj_loader.py      # OBJ file loader with normal generation
├── gltf_loader.py     # GLTF file loader (requires pygltflib)
├── monkey.obj         # Sample 3D model (Torus)
├── monkey.mtl         # Material file for the model
└── README.md          # This file
```

## Key Features

### Camera System
- Horizontal and vertical rotation
- Position-based movement relative to camera orientation
- Perspective projection with configurable focal length

### Lighting
- Directional light source
- Normal-based brightness calculation
- Ambient minimum brightness (20%)
- Automatic light vector normalization

### Rendering Pipeline
1. Vertex transformation (camera space)
2. Near plane clipping
3. Perspective projection
4. Backface culling (cross product test)
5. Normal-based lighting
6. Fog calculation
7. Color blending with fog

### OBJ Loader Features
- Loads vertices and normals from OBJ files
- Automatic normal generation if normals are missing
- Triangulation of polygon faces
- Support for missing normal indices

## Technical Details

### Rendering Algorithm
- **Painter's Algorithm**: Triangles are sorted by depth and rendered farthest first
- **Perspective Projection**: `sx = (x / z) * focal_length`
- **Near Plane Clipping**: Triangles with z ≤ 0.1 are discarded
- **Backface Culling**: Uses cross product to determine triangle winding order

### Configuration
- Window size: 1280x720
- Focal length: 500
- Near plane: 0.1
- Fog factor: max(0.45, z/80)

## License

This project is provided as-is for educational purposes.
