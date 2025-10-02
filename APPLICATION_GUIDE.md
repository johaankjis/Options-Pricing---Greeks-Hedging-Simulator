# Options Pricing & Hedging Simulator - Application Guide

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Pricing Models](#pricing-models)
5. [Greeks Computation](#greeks-computation)
6. [Hedging Strategies](#hedging-strategies)
7. [Interactive Dashboard](#interactive-dashboard)
8. [Performance Optimization](#performance-optimization)
9. [Getting Started](#getting-started)
10. [API Reference](#api-reference)
11. [Use Cases](#use-cases)

---

## Overview

The Options Pricing & Hedging Simulator is a professional-grade application designed for quantitative researchers, traders, and finance students. It provides accurate options pricing, real-time Greeks computation, and sophisticated hedging strategy simulation capabilities.

### Key Capabilities
- **Accurate Pricing**: ≤ 0.5% error vs benchmark data
- **Real-Time Analysis**: < 1 second dashboard update latency
- **High Performance**: 10,000 Monte Carlo paths computed in < 2 seconds
- **Comprehensive Greeks**: Delta, Gamma, Vega, Theta, and Rho
- **Advanced Hedging**: Delta-neutral and Gamma-neutral strategies
- **Monte Carlo Simulation**: Stress testing across 1,000+ market scenarios

### Target Users
- **Quantitative Researchers**: Testing pricing models and hedging theories
- **Traders**: Analyzing option strategies and risk exposure
- **Students**: Learning derivatives pricing and risk management
- **Portfolio Managers**: Hedging portfolio risk

---

## Architecture

The application is built on a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Dashboard Layer (Plotly Dash)            │
│          Interactive UI with Real-time Visualizations        │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                   Application Logic Layer                   │
├─────────────────────┬───────────────────┬───────────────────┤
│  Pricing Engine     │  Hedging Simulator│   Validation      │
│  - Black-Scholes    │  - Delta Hedge    │   - Accuracy      │
│  - Binomial Tree    │  - Gamma Hedge    │   - Benchmarks    │
│  - Greeks           │  - Monte Carlo    │                   │
└─────────────────────┴───────────────────┴───────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────┐
│              Optimization Layer (Numba JIT)                 │
│        Compiled Functions for Performance-Critical Code      │
└─────────────────────────────────────────────────────────────┘
```

### File Structure
```
options-simulator/
├── pricing.py              # Core pricing engine (Black-Scholes & Binomial)
├── pricing_optimized.py    # JIT-compiled optimized pricing engine
├── hedging.py              # Hedging strategies and portfolio management
├── validation.py           # Pricing accuracy validation against benchmarks
├── dashboard.py            # Interactive Plotly Dash web application
├── scripts/
│   ├── run_dashboard.py           # Launch the dashboard server
│   ├── test_pricing.py            # Validate pricing accuracy
│   ├── test_hedging.py            # Test hedging effectiveness
│   └── benchmark_performance.py   # Performance benchmarking
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
└── README.md               # Quick start guide
```

---

## Core Components

### 1. Pricing Engine (`pricing.py`)

The baseline pricing engine implements two fundamental option pricing models:

#### Black-Scholes Model
- **Purpose**: Analytical pricing for European-style options
- **Advantages**: Exact solution, very fast computation
- **Limitations**: European options only (no early exercise)

#### Binomial Tree Model
- **Purpose**: Discrete-time pricing for American-style options
- **Advantages**: Supports early exercise, flexible
- **Parameters**: Default 100 time steps for accuracy

**Example Usage:**
```python
from pricing import OptionParams, OptionsPricingEngine

# Create pricing engine
engine = OptionsPricingEngine()

# Define option parameters
params = OptionParams(
    spot=100,           # Current stock price
    strike=100,         # Strike price
    volatility=0.25,    # 25% annual volatility
    rate=0.05,          # 5% risk-free rate
    maturity=1.0,       # 1 year to expiration
    option_type='call', # 'call' or 'put'
    style='european'    # 'european' or 'american'
)

# Calculate price
price = engine.price(params)
print(f"Option Price: ${price:.2f}")

# Calculate Greeks
greeks = engine.greeks(params)
print(f"Delta: {greeks['delta']:.4f}")
print(f"Gamma: {greeks['gamma']:.4f}")
print(f"Vega:  {greeks['vega']:.4f}")
print(f"Theta: {greeks['theta']:.4f}")
print(f"Rho:   {greeks['rho']:.4f}")
```

### 2. Optimized Pricing Engine (`pricing_optimized.py`)

The optimized engine uses Numba JIT compilation for high-performance computation:

**Key Features:**
- 40-60% faster than baseline for single pricing
- 80-90% faster for vectorized operations
- Supports parallel Monte Carlo simulation
- < 2 seconds for 10,000 price paths

**Example - Vectorized Pricing:**
```python
from pricing_optimized import OptimizedPricingEngine, OptionParams
import numpy as np

engine = OptimizedPricingEngine()

params = OptionParams(
    spot=100, strike=100, volatility=0.25,
    rate=0.05, maturity=1.0, option_type='call'
)

# Price options for multiple spot prices
spot_array = np.linspace(80, 120, 1000)
prices = engine.price_multiple(spot_array, params)
# Computes 1,000 prices efficiently
```

**Example - Monte Carlo Simulation:**
```python
# Simulate 10,000 price paths
paths = engine.simulate_paths(
    S0=100,         # Initial price
    sigma=0.25,     # Volatility
    r=0.05,         # Risk-free rate
    T=1.0,          # Time horizon
    n_paths=10000,  # Number of paths
    n_steps=252     # Daily time steps
)
# Returns: (10000, 253) array of price paths
# Completes in < 2 seconds
```

### 3. Hedging Simulator (`hedging.py`)

Implements sophisticated hedging strategies to reduce portfolio risk:

#### Portfolio Structure
```python
from hedging import Portfolio, Position
from pricing import OptionParams

# Create a portfolio
portfolio = Portfolio(positions=[])

# Add option position
call_option = OptionParams(
    spot=100, strike=100, volatility=0.25,
    rate=0.05, maturity=0.5, option_type='call'
)
portfolio.add_position(
    Position(instrument_type='option', quantity=10, params=call_option)
)

# Add stock position
portfolio.add_position(
    Position(instrument_type='stock', quantity=-50)  # Short stock
)
```

#### Hedging Strategies

**Delta Hedging:**
- Creates a delta-neutral position
- Uses underlying stock to offset delta exposure
- Protects against small price movements

**Gamma Hedging:**
- Creates both delta and gamma-neutral positions
- Uses additional options to offset gamma exposure
- Protects against large price movements and delta changes

**Example - Hedging Simulation:**
```python
from hedging import HedgingSimulator

simulator = HedgingSimulator()

# Test hedging effectiveness
results = simulator.simulate_hedging_effectiveness(
    portfolio=portfolio,
    hedge_strategy='delta',  # 'none', 'delta', or 'gamma'
    n_scenarios=1000
)

print(f"Portfolio Value Std Dev: ${results['portfolio_std']:.2f}")
print(f"Variance Reduction: {results['variance_reduction']:.1f}%")
print(f"Max Loss: ${results['max_loss']:.2f}")
```

### 4. Validation System (`validation.py`)

Ensures pricing accuracy against academic benchmarks:

**Test Cases:**
- At-the-money (ATM) options
- In-the-money (ITM) options
- Out-of-the-money (OTM) options
- Various maturities and volatilities

**Accuracy Target:** ≤ 0.5% error vs benchmark prices

```bash
# Run validation
python scripts/test_pricing.py
```

**Sample Output:**
```
======================================================================
OPTIONS PRICING ENGINE VALIDATION
======================================================================
Test Case                 Expected     Calculated   Error %   
----------------------------------------------------------------------
ATM European Call         $10.4506     $10.4502     0.0038%   ✓
OTM European Put          $6.0400      $6.0403      0.0050%   ✓
ITM European Call         $13.8308     $13.8305     0.0022%   ✓
----------------------------------------------------------------------

Validation Statistics:
  Tests Passed: 10/10 (100.0%)
  Average Error: 0.0315%
  Maximum Error: 0.1243%
  
✓ SUCCESS: All tests passed (error < 0.5% target)
```

---

## Pricing Models

### Black-Scholes Model

The Black-Scholes formula provides an analytical solution for European options:

**Call Option:**
```
C = S₀ · N(d₁) - K · e^(-rT) · N(d₂)
```

**Put Option:**
```
P = K · e^(-rT) · N(-d₂) - S₀ · N(-d₁)
```

Where:
- **d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T)**
- **d₂ = d₁ - σ√T**
- **S₀** = Current stock price
- **K** = Strike price
- **r** = Risk-free rate
- **σ** = Volatility
- **T** = Time to maturity
- **N(x)** = Cumulative normal distribution

**Assumptions:**
- European exercise only
- Constant volatility
- No dividends
- Efficient markets
- Log-normal price distribution

### Binomial Tree Model

A discrete-time model that builds a tree of possible future prices:

**Algorithm:**
1. Calculate up (u) and down (d) factors:
   - u = e^(σ√Δt)
   - d = 1/u
   - p = (e^(rΔt) - d) / (u - d)  [risk-neutral probability]

2. Build price tree forward from spot to maturity

3. Calculate option values backward from maturity:
   - Terminal values: max(S - K, 0) for calls
   - Interior nodes: max(discounted expected value, early exercise value)

**Advantages:**
- Handles American options (early exercise)
- Can incorporate dividends
- More intuitive than Black-Scholes

**Configuration:**
- Default: 100 time steps
- More steps = higher accuracy but slower computation

---

## Greeks Computation

Greeks measure option price sensitivity to various market factors:

### Delta (Δ)
**Definition:** Rate of change of option price with respect to underlying price
```
Δ = ∂V/∂S
```
- **Call Delta:** 0 to 1
- **Put Delta:** -1 to 0
- **Use:** Hedge ratio, directional risk

**Example:**
- Delta = 0.6 means a $1 increase in stock price → ~$0.60 increase in option price
- To hedge 100 call options (Delta = 0.6): Short 60 shares

### Gamma (Γ)
**Definition:** Rate of change of delta with respect to underlying price
```
Γ = ∂²V/∂S²
```
- **Range:** Always positive for long options
- **Use:** Delta hedging stability, curvature risk

**Example:**
- Gamma = 0.05 means if stock moves $1, delta changes by 0.05
- High gamma → delta changes rapidly → need frequent rehedging

### Vega (ν)
**Definition:** Rate of change of option price with respect to volatility
```
ν = ∂V/∂σ
```
- **Range:** Always positive for long options
- **Use:** Volatility risk exposure

**Example:**
- Vega = 0.4 means 1% volatility increase → $0.40 option price increase
- Long options → positive vega (benefit from vol increase)

### Theta (Θ)
**Definition:** Rate of change of option price with respect to time
```
Θ = ∂V/∂t
```
- **Range:** Typically negative for long options (time decay)
- **Use:** Time decay risk

**Example:**
- Theta = -0.05 means option loses $0.05 per day (all else equal)
- Accelerates as expiration approaches

### Rho (ρ)
**Definition:** Rate of change of option price with respect to interest rate
```
ρ = ∂V/∂r
```
- **Call Rho:** Positive (higher rates → higher call values)
- **Put Rho:** Negative (higher rates → lower put values)
- **Use:** Interest rate risk (usually minor)

### Portfolio Greeks

For a portfolio with multiple positions:
```python
simulator = HedgingSimulator()
portfolio_greeks = simulator.calculate_portfolio_greeks(portfolio)

print(f"Portfolio Delta: {portfolio_greeks['delta']:.2f}")
print(f"Portfolio Gamma: {portfolio_greeks['gamma']:.4f}")
print(f"Portfolio Vega:  {portfolio_greeks['vega']:.2f}")
```

---

## Hedging Strategies

### Delta Hedging

**Objective:** Create a delta-neutral position to eliminate directional risk

**Implementation:**
```python
simulator = HedgingSimulator()

# Original portfolio with long call options
original_portfolio = Portfolio(positions=[...])

# Apply delta hedge
hedged_portfolio = simulator.delta_hedge(original_portfolio)

# The hedged portfolio now has Delta ≈ 0
```

**Mechanics:**
1. Calculate portfolio delta
2. Add opposite stock position: shares = -portfolio_delta
3. Result: Delta-neutral portfolio

**Benefits:**
- Protects against small price movements
- Reduces directional risk
- Captures time value and volatility changes

**Limitations:**
- Requires continuous rebalancing
- Gamma risk remains (delta changes as price moves)
- Transaction costs

### Gamma Hedging

**Objective:** Create both delta and gamma-neutral positions

**Implementation:**
```python
# Define hedge option (typically different strike)
hedge_option = OptionParams(
    spot=100, strike=95, volatility=0.25,
    rate=0.05, maturity=0.5, option_type='put'
)

# Apply gamma hedge
hedged_portfolio = simulator.gamma_hedge(
    portfolio=original_portfolio,
    hedge_option_params=hedge_option
)

# Now both Delta ≈ 0 and Gamma ≈ 0
```

**Mechanics:**
1. Add options to neutralize gamma
2. Then delta hedge the combined portfolio
3. Result: Both delta and gamma neutral

**Benefits:**
- More stable than delta-only hedge
- Less rebalancing needed
- Better for large moves

**Considerations:**
- Requires option positions (higher costs)
- Vega exposure may change
- More complex to implement

### Monte Carlo Stress Testing

Test hedging effectiveness across thousands of scenarios:

```python
results = simulator.simulate_hedging_effectiveness(
    portfolio=portfolio,
    hedge_strategy='delta',
    n_scenarios=1000
)

# Analyze results
print(f"Unhedged Std Dev: ${results['unhedged_std']:.2f}")
print(f"Hedged Std Dev:   ${results['hedged_std']:.2f}")
print(f"Variance Reduction: {results['variance_reduction']:.1f}%")
```

**Scenarios Include:**
- Random spot price changes (-20% to +20%)
- Volatility shocks (-50% to +50%)
- Time decay (1 day forward)

**Success Metric:** ≥ 15% variance reduction

---

## Interactive Dashboard

The Plotly Dash dashboard provides real-time visualization and analysis:

### Launching the Dashboard

```bash
python scripts/run_dashboard.py
```

Then navigate to: **http://127.0.0.1:8050**

### Dashboard Features

#### 1. Option Parameters Panel
**Inputs:**
- Spot Price: Current underlying price
- Strike Price: Option exercise price
- Time to Maturity: Years until expiration
- Volatility: Annual volatility (sigma)
- Risk-Free Rate: Annual rate
- Option Type: Call or Put
- Exercise Style: European or American
- Pricing Model: Black-Scholes or Binomial Tree

#### 2. Pricing Results Display
**Outputs:**
- Option Price (both models for comparison)
- All Greeks (Delta, Gamma, Vega, Theta, Rho)
- Time value vs Intrinsic value breakdown

#### 3. Payoff Diagram
**Visualization:**
- Profit/Loss vs underlying price at expiration
- Breakeven points
- Maximum profit/loss
- Current spot price indicator

#### 4. Greeks Visualization
**Charts:**
- Delta curve across spot prices
- Gamma curve showing sensitivity
- Vega profile
- Time decay (Theta) over time

#### 5. 3D Delta Surface
**Interactive 3D Plot:**
- Delta variation with spot price and time
- Rotating 3D visualization
- Color gradient for magnitude

#### 6. Hedging Simulation
**Analysis:**
- Compare no hedge vs delta hedge vs gamma hedge
- PnL distribution histograms
- Variance reduction metrics
- Expected shortfall (worst-case scenarios)

### Performance Characteristics
- **Update Latency:** < 1 second for all calculations
- **Responsiveness:** Instant parameter updates
- **Visualization:** Smooth, interactive charts

---

## Performance Optimization

### Optimization Techniques

#### 1. Numba JIT Compilation
**Impact:** 10-100x speedup for numerical functions

```python
from numba import jit

@jit(nopython=True, cache=True)
def black_scholes_price(S, K, sigma, r, T, is_call):
    # Compiled to machine code
    # Runs at near-C speed
    ...
```

**Benefits:**
- Near-native code performance
- Automatic parallelization
- Cached compilation (fast subsequent runs)

#### 2. Vectorization
**Impact:** 80-90% faster for array operations

```python
# Instead of looping
for i in range(len(spot_array)):
    price = calculate_price(spot_array[i])
    
# Vectorize
prices = black_scholes_vectorized(spot_array, K, sigma, r, T)
```

**Benefits:**
- SIMD instructions utilized
- Eliminates Python loop overhead
- Batch processing efficiency

#### 3. Fast Approximations
**Normal Distribution:**
```python
@jit(nopython=True, cache=True)
def norm_cdf(x):
    # Fast tanh-based approximation
    return 0.5 * (1.0 + np.tanh(np.sqrt(2/np.pi) * (x + 0.044715 * x**3)))
```

**Benefits:**
- Avoids scipy overhead
- Maintains < 0.1% accuracy
- Significant speedup for frequent calls

#### 4. Parallel Monte Carlo
```python
@jit(nopython=True, parallel=True, cache=True)
def monte_carlo_paths(S0, sigma, r, T, n_paths, n_steps):
    for i in prange(n_paths):  # Parallel loop
        # Independent path generation
        ...
```

**Benefits:**
- Multi-core utilization
- Linear scaling with CPU cores
- No thread management overhead

### Performance Benchmarks

Run benchmarks:
```bash
python scripts/benchmark_performance.py
```

**Expected Results:**

| Operation | Baseline | Optimized | Speedup |
|-----------|----------|-----------|---------|
| Single Pricing | 100ms | 40ms | 60% |
| Greeks Calculation | 500ms | 250ms | 50% |
| Vectorized (1000 prices) | 2000ms | 200ms | 90% |
| Monte Carlo (10K paths) | 3500ms | 1800ms | 48% |

**Hardware:** Results shown for typical modern CPU (4-8 cores)

---

## Getting Started

### Installation

#### Prerequisites
- Python 3.8 or higher
- pip package manager

#### Install Dependencies
```bash
pip install -r requirements.txt
```

**Required Packages:**
- numpy >= 1.24.0
- scipy >= 1.10.0
- plotly >= 5.14.0
- dash >= 2.9.0
- pandas >= 2.0.0
- numba >= 0.57.0

### Quick Start Examples

#### Example 1: Price a Single Option
```python
from pricing import OptionParams, OptionsPricingEngine

engine = OptionsPricingEngine()

call = OptionParams(
    spot=100, strike=105, volatility=0.20,
    rate=0.03, maturity=0.5, option_type='call'
)

price = engine.price(call)
greeks = engine.greeks(call)

print(f"Call Price: ${price:.2f}")
print(f"Delta: {greeks['delta']:.4f}")
```

#### Example 2: Compare American vs European
```python
# European put
euro_put = OptionParams(
    spot=100, strike=100, volatility=0.25,
    rate=0.05, maturity=1.0, 
    option_type='put', style='european'
)

# American put (same parameters)
amer_put = OptionParams(
    spot=100, strike=100, volatility=0.25,
    rate=0.05, maturity=1.0, 
    option_type='put', style='american'
)

euro_price = engine.price(euro_put)
amer_price = engine.price(amer_put)

print(f"European Put: ${euro_price:.2f}")
print(f"American Put: ${amer_price:.2f}")
print(f"Early Exercise Premium: ${amer_price - euro_price:.2f}")
```

#### Example 3: Build and Hedge a Portfolio
```python
from hedging import Portfolio, Position, HedgingSimulator

# Create portfolio with long calls
portfolio = Portfolio(positions=[
    Position(
        instrument_type='option',
        quantity=100,
        params=OptionParams(
            spot=100, strike=100, volatility=0.25,
            rate=0.05, maturity=0.25, option_type='call'
        )
    )
])

# Simulate hedging
simulator = HedgingSimulator()

results = simulator.compare_strategies(
    portfolio=portfolio,
    n_scenarios=1000
)

print(f"Unhedged Variance: ${results['no_hedge']['pnl_std']:.2f}")
print(f"Delta Hedged Variance: ${results['delta_hedge']['pnl_std']:.2f}")
print(f"Variance Reduction: {results['delta_hedge']['variance_reduction']:.1f}%")
```

### Docker Deployment

#### Build Image
```bash
docker build -t options-simulator .
```

#### Run Container
```bash
docker run -p 8050:8050 options-simulator
```

Access dashboard at: http://localhost:8050

### Running Tests

#### Validate Pricing Accuracy
```bash
python scripts/test_pricing.py
```

#### Test Hedging Simulation
```bash
python scripts/test_hedging.py
```

#### Performance Benchmarks
```bash
python scripts/benchmark_performance.py
```

---

## API Reference

### OptionParams Class

```python
@dataclass
class OptionParams:
    spot: float          # Current underlying price
    strike: float        # Strike/exercise price
    volatility: float    # Annualized volatility (σ)
    rate: float          # Risk-free rate (annual)
    maturity: float      # Time to maturity (years)
    option_type: Literal['call', 'put']
    style: Literal['european', 'american'] = 'european'
```

### OptionsPricingEngine

```python
class OptionsPricingEngine:
    def __init__(self, binomial_steps: int = 100):
        """Initialize pricing engine"""
        
    def price(self, params: OptionParams) -> float:
        """Calculate option price"""
        
    def greeks(self, params: OptionParams) -> Dict[str, float]:
        """Calculate all Greeks
        Returns: {'delta', 'gamma', 'vega', 'theta', 'rho'}
        """
```

### OptimizedPricingEngine

```python
class OptimizedPricingEngine:
    def __init__(self, binomial_steps: int = 100):
        """Initialize optimized engine with JIT compilation"""
        
    def price(self, params: OptionParams) -> float:
        """Price option (optimized)"""
        
    def greeks(self, params: OptionParams) -> Dict[str, float]:
        """Calculate Greeks (optimized)"""
        
    def price_multiple(self, spot_array: np.ndarray, 
                      params: OptionParams) -> np.ndarray:
        """Vectorized pricing for multiple spot prices"""
        
    def simulate_paths(self, S0: float, sigma: float, r: float,
                      T: float, n_paths: int, n_steps: int) -> np.ndarray:
        """Monte Carlo price path simulation"""
```

### HedgingSimulator

```python
class HedgingSimulator:
    def __init__(self):
        """Initialize hedging simulator"""
        
    def delta_hedge(self, portfolio: Portfolio) -> Portfolio:
        """Create delta-neutral hedge"""
        
    def gamma_hedge(self, portfolio: Portfolio, 
                   hedge_option_params: OptionParams) -> Portfolio:
        """Create delta and gamma-neutral hedge"""
        
    def calculate_portfolio_greeks(self, portfolio: Portfolio) -> Dict:
        """Calculate aggregated portfolio Greeks"""
        
    def simulate_hedging_effectiveness(
        self, portfolio: Portfolio,
        hedge_strategy: Literal['none', 'delta', 'gamma'],
        n_scenarios: int = 1000
    ) -> Dict:
        """Simulate hedging across market scenarios"""
        
    def compare_strategies(self, portfolio: Portfolio,
                          n_scenarios: int = 1000,
                          hedge_option_params: OptionParams = None) -> Dict:
        """Compare all hedging strategies"""
```

---

## Use Cases

### Use Case 1: Option Pricing for Trading
**Scenario:** Determine fair value of an option before trading

```python
from pricing import OptionParams, OptionsPricingEngine

engine = OptionsPricingEngine()

# Market data
market_call = OptionParams(
    spot=150.25,      # Current AAPL price
    strike=155,       # Strike price
    volatility=0.30,  # Implied volatility
    rate=0.045,       # Current risk-free rate
    maturity=45/365,  # 45 days to expiration
    option_type='call'
)

fair_value = engine.price(market_call)
greeks = engine.greeks(market_call)

print(f"Fair Value: ${fair_value:.2f}")
print(f"Delta: {greeks['delta']:.3f}")

# Decision: If market price < fair value → potential buy
```

### Use Case 2: Portfolio Risk Management
**Scenario:** Manage delta exposure of an options portfolio

```python
from hedging import Portfolio, Position, HedgingSimulator

# Build portfolio
portfolio = Portfolio(positions=[
    Position(instrument_type='option', quantity=50, 
             params=call_option_1),
    Position(instrument_type='option', quantity=-30, 
             params=put_option_1),
    Position(instrument_type='stock', quantity=100)
])

simulator = HedgingSimulator()

# Check current exposure
greeks = simulator.calculate_portfolio_greeks(portfolio)
print(f"Portfolio Delta: {greeks['delta']:.2f}")
print(f"Portfolio Gamma: {greeks['gamma']:.4f}")

# If |delta| > threshold, hedge it
if abs(greeks['delta']) > 50:
    hedged = simulator.delta_hedge(portfolio)
    print("Portfolio hedged")
```

### Use Case 3: Backtesting Hedging Strategies
**Scenario:** Evaluate effectiveness of different hedging approaches

```python
simulator = HedgingSimulator()

# Test portfolio under stressed conditions
results = simulator.compare_strategies(
    portfolio=portfolio,
    n_scenarios=5000,  # More scenarios for robust testing
    hedge_option_params=hedge_option
)

# Analyze results
for strategy in ['no_hedge', 'delta_hedge', 'gamma_hedge']:
    stats = results[strategy]
    print(f"\n{strategy.upper()}:")
    print(f"  Mean PnL: ${stats['pnl_mean']:.2f}")
    print(f"  Std Dev: ${stats['pnl_std']:.2f}")
    print(f"  Max Loss: ${stats['max_loss']:.2f}")
    print(f"  Sharpe Ratio: {stats['pnl_mean']/stats['pnl_std']:.2f}")
```

### Use Case 4: Education & Learning
**Scenario:** Interactive learning about option Greeks

```bash
# Launch the dashboard
python scripts/run_dashboard.py
```

Then in browser:
1. Adjust spot price slider → observe Delta changes
2. Change time to maturity → see Theta effect
3. Modify volatility → watch Vega impact
4. Switch between call/put → compare Greeks
5. View 3D Delta surface → understand behavior

### Use Case 5: Performance-Critical Applications
**Scenario:** Price thousands of options for real-time risk systems

```python
from pricing_optimized import OptimizedPricingEngine
import numpy as np

engine = OptimizedPricingEngine()

# Generate spot price grid
spots = np.linspace(80, 120, 10000)

# Base option parameters
params = OptionParams(
    spot=100, strike=100, volatility=0.25,
    rate=0.05, maturity=1.0, option_type='call'
)

# Vectorized pricing (very fast)
import time
start = time.time()
prices = engine.price_multiple(spots, params)
elapsed = time.time() - start

print(f"Priced {len(spots)} options in {elapsed:.3f}s")
print(f"Rate: {len(spots)/elapsed:.0f} prices/second")
```

### Use Case 6: Stress Testing
**Scenario:** Test portfolio under extreme market conditions

```python
from hedging import MarketScenario

# Generate extreme scenarios
extreme_scenarios = MarketScenario.generate_scenarios(
    base_spot=100,
    base_vol=0.25,
    n_scenarios=1000,
    spot_shock_range=(-0.3, 0.3),    # ±30% moves
    vol_shock_range=(-0.7, 1.0),      # Volatility spikes
    time_step=5/252                    # 5 trading days
)

# Test portfolio performance
pnls = []
for scenario in extreme_scenarios:
    value = simulator.calculate_portfolio_value(
        portfolio, 
        scenario['spot'], 
        scenario['volatility'],
        scenario['time_elapsed']
    )
    pnls.append(value)

# Risk metrics
var_95 = np.percentile(pnls, 5)  # Value at Risk
cvar_95 = np.mean([p for p in pnls if p < var_95])  # CVaR

print(f"95% VaR: ${var_95:.2f}")
print(f"95% CVaR: ${cvar_95:.2f}")
```

---

## Conclusion

The Options Pricing & Hedging Simulator provides a comprehensive toolkit for options analysis, from basic pricing to sophisticated hedging strategies. Its combination of accuracy, performance, and usability makes it suitable for both educational and professional applications.

### Key Takeaways

1. **Accurate**: Validated against academic benchmarks (≤ 0.5% error)
2. **Fast**: Optimized for real-time applications (< 1s updates)
3. **Comprehensive**: Covers pricing, Greeks, and hedging
4. **Interactive**: Professional dashboard for visualization
5. **Flexible**: Both baseline and optimized engines available
6. **Educational**: Clear code structure for learning

### Next Steps

- Explore the interactive dashboard
- Run validation and benchmark scripts
- Experiment with different option strategies
- Integrate into your own applications
- Contribute enhancements via GitHub

### Resources

- **Repository**: github.com/johaankjis/Options-Pricing---Greeks-Hedging-Simulator
- **Documentation**: README.md (quick start)
- **API Reference**: This guide (comprehensive)

---

*For questions, issues, or contributions, please visit the GitHub repository.*
