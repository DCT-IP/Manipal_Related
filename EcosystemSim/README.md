# Procedural World Simulator

A C++ project exploring procedural generation and emergent behavior by progressively turning mathematical and computational models into an interactive visual simulation.

The project is built around the progression:

**Mathematics → Algorithms → Data → Simulation → Visualization**

The goal is not to build a full game, but to understand how systems such as noise, cellular automata, terrain models, and ecosystems can be implemented and visualized from scratch.

## Tech Stack

* **C++17** — core implementation
* **CMake** — build system
* **SFML 2.6** — rendering, windows, and input
* **Dear ImGui** — controls and debugging UI
* **Git/GitHub** — version control

---

## Development Roadmap

### Prerequisite Track

Before implementing the main procedural systems, the project covers the fundamentals required to build and visualize them.

#### P0 — CMake ✓

* [x] Basic CMake project structure
* [x] Targets and executable configuration
* [x] Build directory workflow
* [x] SFML integration with CMake

#### P1 — SFML Fundamentals

* [x] Window creation
* [x] Event loop
* [x] Basic shapes
* [x] Game loop
* [x] Delta time
* [x] Movement
* [ ] Coordinates and transformations
* [ ] Keyboard and mouse input
* [ ] Multiple objects
* [ ] Grid rendering
* [ ] Data/rendering separation
* [ ] Numerical values → colors
* [ ] Scalar field visualization
* [ ] Basic camera/view
* [ ] Simulation/update architecture
* [ ] SFML mini-project

#### P2 — Simulation Fundamentals

* [ ] Update vs render
* [ ] Simulation state
* [ ] Time-stepped simulation
* [ ] Spatial representation
* [ ] World vs screen coordinates
* [ ] Basic spatial partitioning concepts

#### P3 — Mathematical Visualization

* [ ] Scalar fields
* [ ] Vectors
* [ ] Gradients
* [ ] Dot products
* [ ] Normalization
* [ ] Interpolation
* [ ] Numerical values → visual representation

#### P4 — Grid & Spatial Data

* [ ] Generic `Grid<T>`
* [ ] Coordinate → index mapping
* [ ] Bounds checking
* [ ] Cell access/modification
* [ ] Grid utilities
* [ ] Grid visualization

---

# Main Simulator

## Phase 1 — Grid System

* [ ] Generic 2D `Grid<T>`
* [ ] Coordinate → index mapping
* [ ] Cell access and modification
* [ ] Bounds checking
* [ ] Grid utilities
* [ ] Basic SFML grid renderer

## Phase 2 — Perlin Noise

* [ ] Gradient generation
* [ ] Dot products
* [ ] Fade function
* [ ] Interpolation
* [ ] 2D Perlin Noise
* [ ] Noise normalization

## Phase 3 — Noise Visualization

* [ ] Map noise values to cells/pixels
* [ ] Noise scale
* [ ] Frequency
* [ ] Amplitude
* [ ] Octaves
* [ ] Seeded generation
* [ ] Interactive visualization

## Phase 4 — Terrain Generation

* [ ] Convert noise into a height map
* [ ] Terrain thresholds
* [ ] Water
* [ ] Plains
* [ ] Forest
* [ ] Mountains
* [ ] Snow
* [ ] Terrain rendering

## Phase 5 — Cellular Automata

* [ ] Random binary grid
* [ ] Neighbor counting
* [ ] Cellular automata rules
* [ ] Iterative updates
* [ ] Cave generation
* [ ] Visualization of iterations

## Phase 6 — Conway's Game of Life

* [ ] Conway's rules
* [ ] Generation updates
* [ ] Population tracking
* [ ] Pause/resume
* [ ] Step-by-step simulation
* [ ] Reset/randomize
* [ ] Interactive visualization

## Phase 7 — Procedural Terrain + CA

* [ ] Apply CA to generated terrain
* [ ] Terrain smoothing
* [ ] Cave/region generation
* [ ] Combine procedural techniques

## Phase 8 — Ecosystem Simulation

* [ ] Organisms
* [ ] Terrain-dependent rules
* [ ] Birth/death
* [ ] Movement
* [ ] Resource interaction
* [ ] Population tracking
* [ ] Simulation updates

## Phase 9 — Simulation Architecture

* [ ] Separate world state from simulation
* [ ] Separate simulation from rendering
* [ ] Modular generators
* [ ] Reusable simulation components
* [ ] Clear update pipeline

## Phase 10 — Interactive UI

* [ ] Dear ImGui integration
* [ ] Seed controls
* [ ] Noise parameters
* [ ] CA parameters
* [ ] Simulation controls
* [ ] Population statistics
* [ ] Debug information

## Phase 11 — Integration

* [ ] Procedural world generation pipeline
* [ ] Terrain + cellular systems
* [ ] Ecosystem simulation
* [ ] Interactive visualization
* [ ] Complete simulation loop

## Phase 12 — Testing & Documentation

* [ ] Unit tests
* [ ] Algorithm documentation
* [ ] Architecture documentation
* [ ] Performance testing
* [ ] Screenshots
* [ ] Final demonstration

---

## Project Pipeline

```text
                    MATHEMATICS
                         ↓
                    C++ Algorithms
                         ↓
                    Grid / World Data
                         ↓
                 Procedural Generation
                         ↓
                  Cellular Simulation
                         ↓
                  Ecosystem Simulation
                         ↓
                   SFML Visualization
                         ↓
                  Interactive World
```

The development philosophy is to build each layer independently and then connect them.

---

## Current Development

The project is currently in the **SFML fundamentals stage**.

Completed:

* Basic CMake setup
* SFML 2.6.1 integration
* SFML window creation
* Event handling
* Basic shape rendering
* SFML reference notes

Next:

**Game Loop + Movement**

```text
Input
  ↓
Update
  ↓
Render
```

---

## Build

Configure the project:

```bash
cmake -S . -B build
```

Build:

```bash
cmake --build build
```

Run the generated executable from the appropriate build output directory.

---

## Project Goal

The goal is not to build a full game.

The goal is to understand how mathematical and computational models can be transformed into a complete visual system:

**Mathematics → Algorithms → Data → Simulation → Visualization**
