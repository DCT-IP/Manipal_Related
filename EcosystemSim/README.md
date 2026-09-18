# Procedural World Simulator

A C++ project exploring procedural generation and emergent behavior by progressively turning mathematical models into an interactive visual simulation.

The project combines:

* Perlin Noise
* Terrain Generation
* Cellular Automata
* Conway's Game of Life
* Procedural Ecosystems
* 2D visualization

## Tech Stack

* **C++** — core implementation
* **CMake** — build system
* **SFML** — rendering and input
* **Dear ImGui** — controls and debugging UI
* **Git/GitHub** — version control

## Development Roadmap

### Phase 1 — Grid System

* [ ] Generic 2D `Grid<T>`
* [ ] Coordinate → index mapping
* [ ] Cell access and modification
* [ ] Bounds checking
* [ ] Grid utilities
* [ ] Basic SFML grid renderer

### Phase 2 — Perlin Noise

* [ ] Gradient generation
* [ ] Dot products
* [ ] Fade function
* [ ] Interpolation
* [ ] 2D Perlin Noise
* [ ] Noise normalization

### Phase 3 — Noise Visualization

* [ ] Map noise values to pixels/cells
* [ ] Noise scale
* [ ] Frequency
* [ ] Amplitude
* [ ] Octaves
* [ ] Seeded generation

### Phase 4 — Terrain Generation

* [ ] Convert noise into a height map
* [ ] Terrain thresholds
* [ ] Water
* [ ] Plains
* [ ] Forest
* [ ] Mountains
* [ ] Snow
* [ ] Terrain rendering

### Phase 5 — Cellular Automata

* [ ] Random binary grid
* [ ] Neighbor counting
* [ ] Cellular automata rules
* [ ] Iterative updates
* [ ] Cave generation
* [ ] Visualization of iterations

### Phase 6 — Conway's Game of Life

* [ ] Conway rules
* [ ] Generation updates
* [ ] Population tracking
* [ ] Pause/resume
* [ ] Step-by-step simulation
* [ ] Reset/randomize

### Phase 7 — Procedural Terrain + CA

* [ ] Apply CA to generated terrain
* [ ] Terrain smoothing
* [ ] Cave/region generation
* [ ] Combine procedural techniques

### Phase 8 — Ecosystem Simulation

* [ ] Organisms
* [ ] Terrain-dependent rules
* [ ] Birth/death
* [ ] Movement
* [ ] Population tracking
* [ ] Simulation updates

### Phase 9 — Simulation Architecture

* [ ] Separate world state from simulation
* [ ] Separate simulation from rendering
* [ ] Modular generators
* [ ] Reusable simulation components

### Phase 10 — Interactive UI

* [ ] Dear ImGui integration
* [ ] Seed controls
* [ ] Noise parameters
* [ ] CA parameters
* [ ] Simulation controls
* [ ] Statistics

### Phase 11 — Integration

* [ ] Procedural world generation pipeline
* [ ] Terrain + cellular systems
* [ ] Ecosystem simulation
* [ ] Interactive visualization

### Phase 12 — Testing & Documentation

* [ ] Unit tests
* [ ] Algorithm documentation
* [ ] Architecture documentation
* [ ] Screenshots
* [ ] Final demonstration

## Final Pipeline

```text
Mathematical Models
        ↓
C++ Algorithms
        ↓
Grid / World Data
        ↓
Procedural Generation
        ↓
Cellular Simulation
        ↓
SFML Renderer
        ↓
Interactive Visual World
```

## Project Goal

The goal is not to build a full game.

The goal is to understand how mathematical and computational models can be transformed into a complete visual system:

**Mathematics → Algorithms → Data → Simulation → Visualization**
