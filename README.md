# Options Pricing & Hedging Simulator

A lightweight, accurate options pricing and hedging simulator for quant researchers, traders, and students. Price vanilla options, simulate hedging strategies, and visualize portfolio risk exposures in near real-time.

## Features

### Phase 1: Options Pricing Engine ✓
- **Black-Scholes Model** for European options (calls & puts)
- **Binomial Tree Model** for American options with early exercise
- **Accuracy**: ≤ 0.5% error vs benchmark data
- **Greeks Computation**: Delta, Gamma, Vega, Theta, Rho

### Phase 2: Hedging Simulator ✓
- **Delta-neutral hedging** using stock positions
- **Gamma-neutral hedging** using options
- **Monte Carlo simulation** across 1,000+ market scenarios
- **Variance reduction tracking** and effectiveness metrics
- **Portfolio Greeks** aggregation

### Phase 3: Visualization Dashboard ✓
- **Interactive Plotly Dash interface** with professional dark theme
- **Real-time pricing** and Greeks computation
- **Payoff diagrams** showing profit/loss profiles
- **3D Delta surface** visualization
- **Hedging simulation** with PnL distribution histograms
- **Performance**: < 1s update latency

### Phase 4: Performance Optimization ✓
- **Numba JIT compilation** for critical functions
- **Vectorized operations** with NumPy
- **Parallel execution** for Monte Carlo simulations
- **Fast approximations** for normal distribution
- **Performance**: 40%+ faster, 10,000 paths in < 2s

## Quick Start

### Installation

\`\`\`bash
# Install dependencies
pip install -r requirements.txt
\`\`\`

### Launch Dashboard

\`\`\`bash
python scripts/run_dashboard.py
\`\`\`

Then open your browser to: **http://127.0.0.1:8050**

### Docker Deployment

\`\`\`bash
# Build image
docker build -t options-simulator .

# Run container
docker run -p 8050:8050 options-simulator
\`\`\`

## Performance Benchmarks

Run the performance benchmark suite:

\`\`\`bash
python scripts/benchmark_performance.py
\`\`\`

**Expected Results:**
- Single option pricing: 50-60% faster
- Greeks calculation: 40-50% faster
- Vectorized pricing (10,000 prices): 80-90% faster
- Monte Carlo (10,000 paths): < 2s

**Optimization Techniques:**
- Numba JIT compilation with caching
- Parallel loops with `prange`
- Fast normal distribution approximations
- Vectorized array operations
- Memory-efficient algorithms

## API Usage

### Optimized Pricing Engine

\`\`\`python
from pricing_optimized import OptimizedPricingEngine, OptionParams

# Initialize engine
engine = OptimizedPricingEngine()

# Price a single option
params = OptionParams(
    spot=100, strike=100, volatility=0.25,
    rate=0.05, maturity=1.0, option_type='call'
)

price = engine.price(params)
greeks = engine.greeks(params)

print(f"Price: ${price:.2f}")
print(f"Delta: {greeks['delta']:.4f}")
\`\`\`

### Vectorized Pricing

\`\`\`python
import numpy as np

# Price options for multiple spot prices
spot_array = np.linspace(80, 120, 1000)
prices = engine.price_multiple(spot_array, params)

# Fast computation for 1,000 prices
\`\`\`

### Monte Carlo Simulation

\`\`\`python
# Simulate 10,000 price paths
paths = engine.simulate_paths(
    S0=100,           # Initial price
    sigma=0.25,       # Volatility
    r=0.05,           # Risk-free rate
    T=1.0,            # Time horizon
    n_paths=10000,    # Number of paths
    n_steps=252       # Daily steps
)

# Completes in < 2 seconds
\`\`\`

## Project Structure

\`\`\`
options-simulator/
├── pricing.py              # Baseline pricing engine
├── pricing_optimized.py    # Optimized engine (Numba JIT)
├── validation.py           # Accuracy validation
├── hedging.py              # Hedging strategies
├── dashboard.py            # Plotly Dash dashboard
├── scripts/
│   ├── test_pricing.py     # Pricing validation
│   ├── test_hedging.py     # Hedging simulation
│   ├── run_dashboard.py    # Launch dashboard
│   └── benchmark_performance.py  # Performance benchmarks
├── Dockerfile              # Container deployment
├── requirements.txt        # Python dependencies
└── README.md
\`\`\`

## Technical Details

### Optimization Strategies

**1. Numba JIT Compilation**
- Compiles Python functions to machine code
- 10-100x speedup for numerical code
- Caching for faster subsequent runs

**2. Vectorization**
- NumPy array operations
- Eliminates Python loops
- SIMD instructions on modern CPUs

**3. Parallel Execution**
- Multi-core processing with `prange`
- Independent path simulations
- Near-linear scaling with cores

**4. Fast Approximations**
- Tanh-based normal CDF approximation
- Reduces scipy dependency overhead
- Maintains accuracy within 0.1%

### Black-Scholes Model
Analytical solution for European options:
- **Call**: C = S·N(d₁) - K·e^(-rT)·N(d₂)
- **Put**: P = K·e^(-rT)·N(-d₂) - S·N(-d₁)

### Binomial Tree Model
Discrete-time model supporting American options:
- Backward induction through price tree
- Early exercise optimization
- Configurable time steps (default: 100)

### Greeks
First and second-order sensitivities:
- **Delta**: ∂V/∂S (price sensitivity)
- **Gamma**: ∂²V/∂S² (delta sensitivity)
- **Vega**: ∂V/∂σ (volatility sensitivity)
- **Theta**: ∂V/∂t (time decay)
- **Rho**: ∂V/∂r (rate sensitivity)

## Success Metrics

- ✓ Pricing accuracy: ≤ 0.5% error vs benchmarks
- ✓ Hedge simulation: ≥ 15% variance reduction
- ✓ Dashboard latency: < 1s updates
- ✓ Runtime: 40%+ faster, 10,000 paths in < 2s

## Roadmap

- [x] **Phase 1**: Pricing Core (Weeks 1-2)
- [x] **Phase 2**: Greeks & Hedging (Weeks 3-4)
- [x] **Phase 3**: Visualization Layer (Week 5)
- [x] **Phase 4**: Optimization & Packaging (Week 6)

## Tech Stack

- **Core**: Python, NumPy, SciPy
- **Optimization**: Numba JIT
- **Visualization**: Plotly Dash
- **Packaging**: Docker

## Running Tests

\`\`\`bash
# Test pricing accuracy
python scripts/test_pricing.py

# Test hedging simulator
python scripts/test_hedging.py

# Benchmark performance
python scripts/benchmark_performance.py

# Launch interactive dashboard
python scripts/run_dashboard.py
\`\`\`

## Requirements

\`\`\`
numpy>=1.24.0
scipy>=1.10.0
plotly>=5.14.0
dash>=2.9.0
pandas>=2.0.0
numba>=0.57.0
\`\`\`

## License

MIT License - Free for academic and commercial use

## Contributing

Contributions welcome! Areas for enhancement:
- Additional option types (Asian, Barrier, etc.)
- More hedging strategies (Vega hedging, etc.)
- Real-time market data integration
- Machine learning for volatility forecasting
