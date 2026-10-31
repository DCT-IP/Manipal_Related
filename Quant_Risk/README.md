# QUANT//RISK

**Monte Carlo Portfolio Risk & Scenario Analysis Engine**

QUANT//RISK is a quantitative finance project for simulating portfolio outcomes, measuring downside risk, and analysing diversification under uncertainty.

It uses correlated Geometric Brownian Motion (GBM) to generate asset-price paths and Monte Carlo methods to estimate portfolio performance and risk. The project also explores sensitivity analysis, hypothetical market stress scenarios, and simulation performance.

## Features

- **Monte Carlo Simulation:** Generate correlated asset-price paths using GBM.
- **Portfolio Customization:** Configure asset parameters, correlations, and portfolio allocations.
- **Risk Metrics:** Calculate Value at Risk (VaR) at 95% and 99% confidence levels.
- **Tail Risk Analysis:** Calculate Conditional Value at Risk (CVaR), also known as Expected Shortfall.
- **Distribution Analysis:** Examine terminal portfolio values, expected returns, and probability of loss.
- **Sensitivity Analysis:** Study the effect of changing asset volatility on portfolio outcomes.
- **Stress Testing:** Evaluate portfolio behaviour under hypothetical market scenarios.
- **Interactive Dashboard:** Explore simulation results through Streamlit and Plotly visualizations.
- **Simulation Optimization:** Use chunked computation to reduce temporary memory consumption.
- **Testing and Validation:** Includes automated tests for GBM theory, correlation, numerical behaviour, and edge cases.

## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Numerical Computing | NumPy, SciPy |
| Data Processing | pandas |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Testing | pytest |
| Benchmarking | psutil, tracemalloc |

## Getting Started

### Requirements

- Python 3.11 or newer
- pip
- A modern web browser

### Installation

Clone the repository:

```bash
git clone <repository-url>
cd Quant_Risk
```

Create a virtual environment:

```bash
python -m venv .venv
```

**Activate the environment**

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL for accessing the interactive dashboard.

### Run Tests

```bash
python -m pytest
```

## Methodology
### 1. Geometric Brownian Motion
Asset prices are modelled using the Geometric Brownian Motion stochastic differential equation:

$$
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t
$$

Its exact discrete-time solution is:

$$
S_{t+\Delta t}
=
S_t \exp\left[
\left(\mu-\frac{\sigma^2}{2}\right)\Delta t
+
\sigma\sqrt{\Delta t}Z
\right]
$$

Where:
- $S_t$ is the asset price at time $t$.
- $\mu$ is the annualized drift.
- $\sigma$ is the annualized volatility.
- $\Delta t$ is the simulation time interval.
- $Z$ is a standard normally distributed random variable.
For multiple assets, correlated random shocks are generated using a correlation matrix and Cholesky decomposition.
This allows the simulation to model dependencies between portfolio assets rather than treating their price movements as independent.

### 2. Portfolio Simulation
The simulated asset prices are combined according to portfolio allocations to evaluate portfolio value over time.
The engine supports comparisons between alternative allocations and examines how asset correlations influence portfolio outcomes.

### 3. Risk Metrics

**Value at Risk (VaR)**
Estimates the loss threshold that is exceeded with a specified probability over the simulation horizon.

**Conditional Value at Risk (CVaR)**
Also known as Expected Shortfall, estimates the average loss in the worst tail of the simulated loss distribution.

**Probability of Loss**
Measures the proportion of simulated terminal portfolio values that fall below the initial portfolio value.

**Sensitivity and Stress Analysis**
Examines how changes in volatility and hypothetical market conditions affect portfolio outcomes and downside risk.

## Simulation Performance
The simulation engine uses chunked computation to reduce the memory overhead associated with large intermediate arrays.
Initial benchmarking compared the original implementation with the optimized implementation.
At 100,000 simulations, using three assets and 252 time steps:

| Metric | Original | Chunked |
|---|---:|---:|
| Runtime | 4.48 s | 1.78 s |
| Peak traced memory | 3,463 MB | 752 MB |

This represents approximately:
- 60.3% lower execution time.
- 78.3% lower peak traced memory.
Additional benchmarks examine chunk-size selection and scaling across different asset counts and time steps.
Detailed methodology and results are available in [`benchmarks/README.md`](benchmarks/README.md).

## Assumptions and Limitations
The baseline GBM model assumes:
- Constant drift over the simulation horizon.
- Constant volatility.
- Normally distributed asset log returns.
- A fixed correlation structure.
- Continuous trading and no explicit transaction costs.

Actual financial markets may exhibit fat-tailed returns, volatility clustering, sudden price jumps, liquidity constraints, and changing correlations.
Consequently, the simulation results are conditional on the selected model assumptions and input parameters.

**Important:** Model outputs are estimates, not guaranteed financial forecasts.

## Disclaimer
QUANT//RISK is an educational quantitative-finance and risk-modelling project.
It is not financial or investment advice and should not be used as the sole basis for real-world financial or trading decisions.

## License
Distributed under the MIT License. See the `LICENSE` file for details.
