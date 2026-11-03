# WILD FIRE SPREAD SIM

**Probabilistic Wildfire Propagation Simulator**

FIRE//SPREAD is a grid-based wildfire simulation project that models how fire spreads through a forest under different environmental conditions.
The simulation uses a **Cellular Automaton (CA)** to represent the forest and probabilistic rules to determine fire propagation.

### Features
- Random forest generation with configurable tree density
- Probabilistic fire propagation between neighbouring cells
- Tree burning and burnout states
- Wind direction and strength as environmental factors
- Vegetation moisture as an ignition modifier
- Visualisation of fire propagation over time
- Configurable simulation parameters

### Cell States
| State | Description |
|---|---|
| 0 | Empty land |
| 1 | Healthy tree |
| 2 | Burning tree |
| 3 | Burnt tree |

### Installation
Clone the repository:

```bash
git clone <repository-url>
cd FIRE-SPREAD
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the simulation:

```bash
python main.py
```

### Objective
The project aims to study how forest density and environmental conditions influence wildfire propagation through simulation and controlled experiments.