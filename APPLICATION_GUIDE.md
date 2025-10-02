<div align="center">

# 📚 Options Pricing & Hedging Simulator
## *Comprehensive Application Guide*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/docs-comprehensive-brightgreen.svg)](.)
[![API](https://img.shields.io/badge/API-reference-orange.svg)](#api-reference)

*Your complete guide to professional-grade options pricing and hedging*

---

</div>

## 📑 Table of Contents

<table>
<tr>
<td width="50%">

### 🎯 Fundamentals
1. [📖 Overview](#overview)
2. [🏗️ Architecture](#architecture)
3. [🧩 Core Components](#core-components)
4. [📐 Pricing Models](#pricing-models)
5. [📊 Greeks Computation](#greeks-computation)

</td>
<td width="50%">

### 🚀 Advanced Topics
6. [🛡️ Hedging Strategies](#hedging-strategies)
7. [🎨 Interactive Dashboard](#interactive-dashboard)
8. [⚡ Performance Optimization](#performance-optimization)
9. [💻 Getting Started](#getting-started)
10. [📚 API Reference](#api-reference)
11. [🎯 Use Cases](#use-cases)

</td>
</tr>
</table>

---

## 📖 Overview

> *A professional-grade application designed for quantitative researchers, traders, and finance students.*

The **Options Pricing & Hedging Simulator** provides accurate options pricing, real-time Greeks computation, and sophisticated hedging strategy simulation capabilities.

### 🎯 Key Capabilities

<div align="center">

| Feature | Specification | Status |
|---------|--------------|--------|
| 🎯 **Accurate Pricing** | ≤ 0.5% error vs benchmarks | ✅ |
| ⚡ **Real-Time Analysis** | < 1s dashboard updates | ✅ |
| 🚀 **High Performance** | 10K Monte Carlo paths in < 2s | ✅ |
| 📊 **Comprehensive Greeks** | Δ, Γ, ν, Θ, ρ | ✅ |
| 🛡️ **Advanced Hedging** | Delta & Gamma-neutral | ✅ |
| 🎲 **Monte Carlo** | 1,000+ market scenarios | ✅ |

</div>

### 👥 Target Users

<table>
<tr>
<td width="50%">

#### 🔬 Quantitative Researchers
- Testing pricing models
- Validating hedging theories
- Academic research

</td>
<td width="50%">

#### 📈 Traders
- Analyzing option strategies
- Assessing risk exposure
- Real-time decision making

</td>
</tr>
<tr>
<td width="50%">

#### 🎓 Students
- Learning derivatives pricing
- Understanding risk management
- Hands-on practice

</td>
<td width="50%">

#### 💼 Portfolio Managers
- Hedging portfolio risk
- Stress testing positions
- Risk analytics

</td>
</tr>
</table>

---

## 🏗️ Architecture

> *Built on a modular architecture with clear separation of concerns*

```
╔═══════════════════════════════════════════════════════════╗
║            🎨 Dashboard Layer (Plotly Dash)              ║
║        Interactive UI with Real-time Visualizations       ║
╚═══════════════════════════╦═══════════════════════════════╝
                            ║
╔═══════════════════════════╩═══════════════════════════════╗
║              📊 Application Logic Layer                   ║
╠═══════════════╦═══════════════════╦═══════════════════════╣
║ 💰 Pricing    ║  🛡️ Hedging       ║  ✅ Validation        ║
║ • Black-Sch.. ║  • Delta Hedge   ║  • Accuracy           ║
║ • Binomial    ║  • Gamma Hedge   ║  • Benchmarks         ║
║ • Greeks      ║  • Monte Carlo   ║                       ║
╚═══════════════╩═══════════════════╩═══════════════════════╝
                            ║
╔═══════════════════════════╩═══════════════════════════════╗
║           ⚡ Optimization Layer (Numba JIT)              ║
║      Compiled Functions for Performance-Critical Code     ║
╚═══════════════════════════════════════════════════════════╝
```

### 📂 File Structure

```
options-simulator/
│
├── 💰 Pricing Engines
│   ├── pricing.py                  # Core pricing engine (Black-Scholes & Binomial)
│   └── pricing_optimized.py        # JIT-compiled optimized engine
│
├── 🛡️ Risk Management
│   ├── hedging.py                  # Hedging strategies & portfolio management
│   └── validation.py               # Accuracy validation against benchmarks
│
├── 🎨 User Interface
│   └── dashboard.py                # Interactive Plotly Dash web application
│
├── 🧪 Testing & Scripts
│   └── scripts/
│       ├── run_dashboard.py        # 🚀 Launch dashboard server
│       ├── test_pricing.py         # ✅ Validate pricing accuracy
│       ├── test_hedging.py         # 🛡️ Test hedging effectiveness
│       └── benchmark_performance.py # 📊 Performance benchmarking
│
├── 🐳 Deployment
│   └── Dockerfile                  # Container configuration
│
└── 📚 Documentation
    ├── README.md                   # Quick start guide
    ├── APPLICATION_GUIDE.md        # This comprehensive guide
    └── requirements.txt            # Python dependencies
```

---

## 🧩 Core Components

### 1️⃣ Pricing Engine (`pricing.py`)

> *The baseline pricing engine implementing two fundamental option pricing models*

<table>
<tr>
<td width="50%">

#### 📐 Black-Scholes Model
- **Purpose**: European options
- **✅ Advantages**: Exact solution, fast
- **⚠️ Limitations**: No early exercise

</td>
<td width="50%">

#### 🌳 Binomial Tree Model
- **Purpose**: American options
- **✅ Advantages**: Early exercise support
- **⚙️ Parameters**: 100 time steps (default)

</td>
</tr>
</table>

#### 💻 Example Usage

```python
from pricing import OptionParams, OptionsPricingEngine

# 🔧 Create pricing engine
engine = OptionsPricingEngine()

# 📝 Define option parameters
params = OptionParams(
    spot=100,           # 💵 Current stock price
    strike=100,         # 🎯 Strike price
    volatility=0.25,    # 📊 25% annual volatility
    rate=0.05,          # 💰 5% risk-free rate
    maturity=1.0,       # ⏰ 1 year to expiration
    option_type='call', # 📈 'call' or 'put'
    style='european'    # 🌍 'european' or 'american'
)

# 💵 Calculate price
price = engine.price(params)
print(f"💰 Option Price: ${price:.2f}")

# 📊 Calculate Greeks
greeks = engine.greeks(params)
print(f"📊 Delta: {greeks['delta']:.4f}")
print(f"📊 Gamma: {greeks['gamma']:.4f}")
print(f"📊 Vega:  {greeks['vega']:.4f}")
print(f"📊 Theta: {greeks['theta']:.4f}")
print(f"📊 Rho:   {greeks['rho']:.4f}")
```

### 2️⃣ Optimized Pricing Engine (`pricing_optimized.py`)

> *High-performance engine using Numba JIT compilation* ⚡

#### 🚀 Key Features

<div align="center">

| Feature | Performance | Improvement |
|---------|-------------|-------------|
| Single Pricing | Fast | **40-60%** faster |
| Vectorized Operations | Ultra Fast | **80-90%** faster |
| Monte Carlo | Lightning | **10K paths < 2s** |
| Parallel Processing | Multi-core | Near-linear scaling |

</div>

#### 💻 Example - Vectorized Pricing

```python
from pricing_optimized import OptimizedPricingEngine, OptionParams
import numpy as np

# 🔧 Initialize optimized engine
engine = OptimizedPricingEngine()

params = OptionParams(
    spot=100, strike=100, volatility=0.25,
    rate=0.05, maturity=1.0, option_type='call'
)

# 🔢 Price options for multiple spot prices
spot_array = np.linspace(80, 120, 1000)
prices = engine.price_multiple(spot_array, params)

# ⚡ Computes 1,000 prices efficiently!
print(f"✅ Computed {len(prices)} prices instantly!")
```

#### 💻 Example - Monte Carlo Simulation

```python
# 🎲 Simulate 10,000 price paths
paths = engine.simulate_paths(
    S0=100,         # 💵 Initial price
    sigma=0.25,     # 📊 Volatility (25%)
    r=0.05,         # 💰 Risk-free rate (5%)
    T=1.0,          # ⏰ Time horizon (1 year)
    n_paths=10000,  # 🔢 Number of paths
    n_steps=252     # 📅 Daily time steps
)

# 📊 Returns: (10000, 253) array of price paths
# ⚡ Completes in < 2 seconds
print(f"✅ Generated {paths.shape[0]:,} price paths!")
```

### 3️⃣ Hedging Simulator (`hedging.py`)

> *Sophisticated hedging strategies to reduce portfolio risk* 🛡️

#### 📦 Portfolio Structure

```python
from hedging import Portfolio, Position
from pricing import OptionParams

# 📊 Create a portfolio
portfolio = Portfolio(positions=[])

# ➕ Add option position
call_option = OptionParams(
    spot=100, strike=100, volatility=0.25,
    rate=0.05, maturity=0.5, option_type='call'
)
portfolio.add_position(
    Position(instrument_type='option', quantity=10, params=call_option)
)

# ➕ Add stock position
portfolio.add_position(
    Position(instrument_type='stock', quantity=-50)  # 📉 Short stock
)
```

#### 🛡️ Hedging Strategies

<table>
<tr>
<td width="50%">

##### ⚖️ Delta Hedging
- ✅ Delta-neutral position
- 📊 Uses underlying stock
- 🎯 Protects against small moves

</td>
<td width="50%">

##### 🎲 Gamma Hedging
- ✅ Delta & Gamma neutral
- 📊 Uses additional options
- 🎯 Protects against large moves

</td>
</tr>
</table>

#### 💻 Example - Hedging Simulation

```python
from hedging import HedgingSimulator

# 🔧 Initialize simulator
simulator = HedgingSimulator()

# 🧪 Test hedging effectiveness
results = simulator.simulate_hedging_effectiveness(
    portfolio=portfolio,
    hedge_strategy='delta',  # 🎯 'none', 'delta', or 'gamma'
    n_scenarios=1000         # 🎲 1000 market scenarios
)

# 📊 Display results
print(f"📊 Portfolio Std Dev: ${results['portfolio_std']:.2f}")
print(f"📉 Variance Reduction: {results['variance_reduction']:.1f}%")
print(f"⚠️ Max Loss: ${results['max_loss']:.2f}")
```

### 4️⃣ Validation System (`validation.py`)

> *Ensures pricing accuracy against academic benchmarks* ✅

#### 🎯 Test Cases

<div align="center">

| Category | Description | Coverage |
|----------|-------------|----------|
| **ATM** | At-the-money options | ✅ |
| **ITM** | In-the-money options | ✅ |
| **OTM** | Out-of-the-money options | ✅ |
| **Various** | Multiple maturities & volatilities | ✅ |

**🎯 Accuracy Target:** ≤ 0.5% error vs benchmark prices

</div>

#### 🧪 Running Validation

```bash
# 🚀 Run validation suite
python scripts/test_pricing.py
```

#### 📊 Sample Output

```
╔══════════════════════════════════════════════════════════════════╗
║          OPTIONS PRICING ENGINE VALIDATION                       ║
╚══════════════════════════════════════════════════════════════════╝

Test Case                 Expected     Calculated   Error %   Status
──────────────────────────────────────────────────────────────────────
ATM European Call         $10.4506     $10.4502     0.0038%   ✅
OTM European Put          $6.0400      $6.0403      0.0050%   ✅
ITM European Call         $13.8308     $13.8305     0.0022%   ✅
──────────────────────────────────────────────────────────────────────

📊 Validation Statistics:
  ✅ Tests Passed: 10/10 (100.0%)
  📊 Average Error: 0.0315%
  📊 Maximum Error: 0.1243%
  
🎉 SUCCESS: All tests passed (error < 0.5% target)
```

---

## 📐 Pricing Models

### 📊 Black-Scholes Model

> *Analytical solution for European options - Fast & Exact*

#### 📐 Formulas

<table>
<tr>
<td width="50%">

**📈 Call Option:**
```
C = S₀ · N(d₁) - K · e^(-rT) · N(d₂)
```

</td>
<td width="50%">

**📉 Put Option:**
```
P = K · e^(-rT) · N(-d₂) - S₀ · N(-d₁)
```

</td>
</tr>
</table>

#### 🔢 Where:

<div align="center">

| Variable | Description | Formula |
|----------|-------------|---------|
| **d₁** | First parameter | `[ln(S₀/K) + (r + σ²/2)T] / (σ√T)` |
| **d₂** | Second parameter | `d₁ - σ√T` |
| **S₀** | Current stock price | Market value |
| **K** | Strike price | Exercise price |
| **r** | Risk-free rate | Annual rate |
| **σ** | Volatility | Annual volatility |
| **T** | Time to maturity | Years |
| **N(x)** | Normal CDF | Cumulative distribution |

</div>

#### ⚠️ Assumptions

- ✅ European exercise only
- ✅ Constant volatility
- ✅ No dividends
- ✅ Efficient markets
- ✅ Log-normal price distribution

---

### 🌳 Binomial Tree Model

> *Discrete-time model for American options - Flexible & Intuitive*

#### 🔄 Algorithm

```
1️⃣ Calculate factors:
   • u = e^(σ√Δt)                    [up factor]
   • d = 1/u                         [down factor]
   • p = (e^(rΔt) - d)/(u - d)       [risk-neutral probability]

2️⃣ Build price tree:
   • Forward from spot to maturity
   • Tree structure: [spot] → [up/down] → [up²/ud/down²] → ...

3️⃣ Calculate option values:
   • Terminal values: max(S - K, 0) for calls
   • Backward induction: max(expected value, early exercise)
```

#### ✅ Advantages

<table>
<tr>
<td width="33%">

**🎯 Flexibility**
- American options
- Early exercise
- Dividends support

</td>
<td width="33%">

**📊 Intuitive**
- Visual tree structure
- Clear probability paths
- Easy to understand

</td>
<td width="33%">

**⚙️ Configurable**
- Adjustable steps
- Accuracy vs speed
- Default: 100 steps

</td>
</tr>
</table>

#### ⚙️ Configuration

| Parameter | Default | Impact |
|-----------|---------|--------|
| **Time Steps** | 100 | More steps = ↑ accuracy, ↓ speed |
| **Optimal** | 50-200 | Balance accuracy & performance |

---

## 📊 Greeks Computation

> *Measuring option price sensitivity to market factors*

<div align="center">

### 🎯 The Five Greeks

| Greek | Symbol | Measures | Formula | Range |
|-------|--------|----------|---------|-------|
| **Delta** | Δ | Price sensitivity | ∂V/∂S | Call: [0,1], Put: [-1,0] |
| **Gamma** | Γ | Delta sensitivity | ∂²V/∂S² | Always positive |
| **Vega** | ν | Volatility sensitivity | ∂V/∂σ | Always positive |
| **Theta** | Θ | Time decay | ∂V/∂t | Usually negative |
| **Rho** | ρ | Rate sensitivity | ∂V/∂r | Call: +, Put: - |

</div>

---

### 📈 Delta (Δ) - Directional Risk

```
Δ = ∂V/∂S
```

<table>
<tr>
<td width="50%">

**📊 Characteristics**
- **Call Delta:** 0 to 1
- **Put Delta:** -1 to 0
- **Use:** Hedge ratio, directional risk

</td>
<td width="50%">

**💡 Example**
- Delta = 0.6 → $1 ↑ stock = ~$0.60 ↑ option
- To hedge 100 calls (Δ=0.6): Short 60 shares
- ATM options: Δ ≈ 0.5 (calls)

</td>
</tr>
</table>

---

### 📊 Gamma (Γ) - Convexity Risk

```
Γ = ∂²V/∂S²
```

<table>
<tr>
<td width="50%">

**📊 Characteristics**
- **Range:** Always positive (long)
- **Use:** Delta stability, curvature
- **Peak:** ATM options

</td>
<td width="50%">

**💡 Example**
- Gamma = 0.05 → $1 move = 0.05 delta change
- High gamma = rapid delta changes
- Need frequent rehedging

</td>
</tr>
</table>

---

### 🌊 Vega (ν) - Volatility Risk

```
ν = ∂V/∂σ
```

<table>
<tr>
<td width="50%">

**📊 Characteristics**
- **Range:** Always positive (long)
- **Use:** Volatility exposure
- **Peak:** ATM, longer maturity

</td>
<td width="50%">

**💡 Example**
- Vega = 0.4 → 1% vol ↑ = $0.40 ↑ option
- Long options = positive vega
- Benefit from volatility increases

</td>
</tr>
</table>

---

### ⏰ Theta (Θ) - Time Decay

```
Θ = ∂V/∂t
```

<table>
<tr>
<td width="50%">

**📊 Characteristics**
- **Range:** Usually negative (long)
- **Use:** Time decay tracking
- **Acceleration:** Near expiration

</td>
<td width="50%">

**💡 Example**
- Theta = -0.05 → lose $0.05/day
- Accelerates near expiration
- Long options lose value over time

</td>
</tr>
</table>

---

### 💰 Rho (ρ) - Interest Rate Risk

```
ρ = ∂V/∂r
```

<table>
<tr>
<td width="50%">

**📊 Characteristics**
- **Call Rho:** Positive
- **Put Rho:** Negative
- **Use:** Rate risk (minor)

</td>
<td width="50%">

**💡 Example**
- Higher rates → higher call values
- Higher rates → lower put values
- Usually smallest Greek impact

</td>
</tr>
</table>

---

### 📦 Portfolio Greeks

```python
# 🔧 Calculate aggregated portfolio Greeks
simulator = HedgingSimulator()
portfolio_greeks = simulator.calculate_portfolio_greeks(portfolio)

# 📊 Display results
print(f"📈 Portfolio Delta: {portfolio_greeks['delta']:.2f}")
print(f"📊 Portfolio Gamma: {portfolio_greeks['gamma']:.4f}")
print(f"🌊 Portfolio Vega:  {portfolio_greeks['vega']:.2f}")
print(f"⏰ Portfolio Theta: {portfolio_greeks['theta']:.2f}")
print(f"💰 Portfolio Rho:   {portfolio_greeks['rho']:.2f}")
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
