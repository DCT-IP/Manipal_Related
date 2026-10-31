# QUANT//RISK — Default Configuration

"""Central defaults for the Monte Carlo portfolio risk simulator."""

# Portfolio
INITIAL_CAPITAL = 100_000.0

# Monte Carlo simulation
DEFAULT_SIMULATIONS = 10_000
DEFAULT_TIME_HORIZON = 1.0
DEFAULT_STEPS = 252
DEFAULT_RANDOM_SEED = 42
# Simulation performance
DEFAULT_CHUNK_SIZE = 1_000
# Risk analysis
DEFAULT_CONFIDENCE_LEVELS = (0.95, 0.99)

# Default asset universe
DEFAULT_ASSETS = ["Asset A", "Asset B", "Asset C"]

# Numerical tolerance
NUMERICAL_TOLERANCE = 1e-8
