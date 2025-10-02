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

## 🛡️ Hedging Strategies

> *Advanced techniques to reduce portfolio risk*

---

### ⚖️ Delta Hedging

> *Eliminate directional risk with delta-neutral positions*

#### 🎯 Objective
Create a **delta-neutral** position to eliminate directional risk

#### 💻 Implementation

```python
simulator = HedgingSimulator()

# 📊 Original portfolio with long call options
original_portfolio = Portfolio(positions=[...])

# 🛡️ Apply delta hedge
hedged_portfolio = simulator.delta_hedge(original_portfolio)

# ✅ The hedged portfolio now has Delta ≈ 0
```

#### 🔄 Mechanics

```
1️⃣ Calculate portfolio delta
2️⃣ Add opposite stock position: shares = -portfolio_delta
3️⃣ Result: Delta-neutral portfolio (Δ ≈ 0)
```

<table>
<tr>
<td width="50%">

#### ✅ Benefits
- 🎯 Protects against small price moves
- 📉 Reduces directional risk
- 💰 Captures time value changes
- 🌊 Benefits from volatility

</td>
<td width="50%">

#### ⚠️ Limitations
- 🔄 Requires continuous rebalancing
- 📊 Gamma risk remains
- 💸 Transaction costs
- ⏰ Time-intensive

</td>
</tr>
</table>

---

### 🎲 Gamma Hedging

> *Create both delta and gamma-neutral positions*

#### 🎯 Objective
Achieve **delta & gamma neutrality** for enhanced stability

#### 💻 Implementation

```python
# 📝 Define hedge option (typically different strike)
hedge_option = OptionParams(
    spot=100, strike=95, volatility=0.25,
    rate=0.05, maturity=0.5, option_type='put'
)

# 🛡️ Apply gamma hedge
hedged_portfolio = simulator.gamma_hedge(
    portfolio=original_portfolio,
    hedge_option_params=hedge_option
)

# ✅ Now both Delta ≈ 0 and Gamma ≈ 0
```

#### 🔄 Mechanics

```
1️⃣ Add options to neutralize gamma
2️⃣ Then delta hedge the combined portfolio
3️⃣ Result: Both Δ ≈ 0 and Γ ≈ 0
```

<table>
<tr>
<td width="50%">

#### ✅ Benefits
- 🎯 More stable than delta-only
- 🔄 Less rebalancing needed
- 📈 Better for large moves
- 🛡️ Enhanced protection

</td>
<td width="50%">

#### ⚠️ Considerations
- 💸 Higher costs (options needed)
- 🌊 Vega exposure may change
- 🔧 More complex to implement
- 📊 Requires option liquidity

</td>
</tr>
</table>

---

### 🎲 Monte Carlo Stress Testing

> *Test hedging effectiveness across thousands of market scenarios*

#### 💻 Implementation

```python
# 🧪 Run stress test simulation
results = simulator.simulate_hedging_effectiveness(
    portfolio=portfolio,
    hedge_strategy='delta',  # 'none', 'delta', or 'gamma'
    n_scenarios=1000         # 1000 market scenarios
)

# 📊 Analyze results
print(f"📊 Unhedged Std Dev: ${results['unhedged_std']:.2f}")
print(f"🛡️ Hedged Std Dev:   ${results['hedged_std']:.2f}")
print(f"📉 Variance Reduction: {results['variance_reduction']:.1f}%")
```

#### 🎲 Scenarios Include

<div align="center">

| Scenario | Range | Impact |
|----------|-------|--------|
| 📈 **Price Changes** | -20% to +20% | Directional moves |
| 🌊 **Volatility Shocks** | -50% to +50% | Vol spikes/crashes |
| ⏰ **Time Decay** | 1 day forward | Theta impact |

**🎯 Success Metric:** ≥ 15% variance reduction

</div>

---

## 🎨 Interactive Dashboard

> *Real-time visualization and analysis with Plotly Dash*

### 🚀 Launching the Dashboard

```bash
# 🚀 Start the dashboard server
python scripts/run_dashboard.py
```

Then navigate to: **🌐 http://127.0.0.1:8050**

---

### 🎛️ Dashboard Features

#### 1️⃣ Option Parameters Panel

**📝 Inputs:**

<div align="center">

| Parameter | Description | Example |
|-----------|-------------|---------|
| 💵 **Spot Price** | Current underlying price | $100 |
| 🎯 **Strike Price** | Option exercise price | $105 |
| ⏰ **Time to Maturity** | Years until expiration | 1.0 year |
| 📊 **Volatility** | Annual volatility (σ) | 25% |
| 💰 **Risk-Free Rate** | Annual rate | 5% |
| 📈 **Option Type** | Call or Put | Call |
| 🌍 **Exercise Style** | European or American | European |
| 🔧 **Pricing Model** | Black-Scholes or Binomial | B-S |

</div>

---

#### 2️⃣ Pricing Results Display

**📊 Outputs:**

<table>
<tr>
<td width="33%">

**💵 Price**
- Both model prices
- Comparison view
- % difference

</td>
<td width="33%">

**📊 Greeks**
- Δ, Γ, ν, Θ, ρ
- All sensitivities
- Real-time updates

</td>
<td width="33%">

**💎 Value Breakdown**
- Time value
- Intrinsic value
- Premium components

</td>
</tr>
</table>

---

#### 3️⃣ Payoff Diagram

**📈 Visualization:**

- 📉 Profit/Loss vs underlying price at expiration
- 🎯 Breakeven points highlighted
- 📊 Maximum profit/loss markers
- 📍 Current spot price indicator
- 🎨 Interactive hover details

---

#### 4️⃣ Greeks Visualization

**📊 Charts:**

<table>
<tr>
<td width="50%">

**Delta Curve**
- 📈 Δ across spot prices
- 🎯 Spot price sensitivity
- Color-coded regions

</td>
<td width="50%">

**Gamma Curve**
- 📊 Γ showing convexity
- 🎲 Delta sensitivity
- Peak visualization

</td>
</tr>
<tr>
<td width="50%">

**Vega Profile**
- 🌊 Volatility sensitivity
- 📊 Vol impact visualization
- Peak at ATM

</td>
<td width="50%">

**Theta Decay**
- ⏰ Time decay over time
- 📉 Acceleration near expiry
- Daily loss visualization

</td>
</tr>
</table>

---

#### 5️⃣ 3D Delta Surface

**🗺️ Interactive 3D Plot:**

- 📊 Delta variation with spot & time
- 🔄 Rotating 3D visualization
- 🎨 Color gradient for magnitude
- 🖱️ Interactive controls (zoom, pan, rotate)
- 💡 Intuitive understanding of Δ behavior

---

#### 6️⃣ Hedging Simulation

**📊 Analysis:**

<div align="center">

| Comparison | Visualization | Metrics |
|------------|---------------|---------|
| **No Hedge** | 📊 PnL distribution | Std dev, VaR |
| **Delta Hedge** | 📊 Improved distribution | Variance reduction |
| **Gamma Hedge** | 📊 Best distribution | Maximum protection |

</div>

**📈 Features:**
- PnL distribution histograms
- Variance reduction metrics (%)
- Expected shortfall (worst-case)
- Side-by-side comparison

---

### ⚡ Performance Characteristics

<div align="center">

| Metric | Target | Status |
|--------|--------|--------|
| ⚡ **Update Latency** | < 1 second | ✅ |
| 🎯 **Responsiveness** | Instant | ✅ |
| 🎨 **Visualization** | Smooth & Interactive | ✅ |
| 💻 **CPU Usage** | Low | ✅ |
| 📊 **Chart Rendering** | Real-time | ✅ |

</div>

---

## ⚡ Performance Optimization

> *Achieving 40-90% faster computation through advanced techniques*

---

### 🛠️ Optimization Techniques

#### 1️⃣ Numba JIT Compilation

**💥 Impact:** 10-100x speedup for numerical functions

```python
from numba import jit

@jit(nopython=True, cache=True)
def black_scholes_price(S, K, sigma, r, T, is_call):
    # 🚀 Compiled to machine code
    # ⚡ Runs at near-C speed
    ...
```

<table>
<tr>
<td width="33%">

**🚀 Performance**
- Near-native code speed
- Machine code compilation
- Dramatic speedups

</td>
<td width="33%">

**🔀 Parallelization**
- Automatic threading
- Multi-core utilization
- No GIL overhead

</td>
<td width="33%">

**💾 Caching**
- Cached compilation
- Fast subsequent runs
- Persistent cache

</td>
</tr>
</table>

---

#### 2️⃣ Vectorization

**💥 Impact:** 80-90% faster for array operations

```python
# ❌ Slow: Loop-based approach
for i in range(len(spot_array)):
    price = calculate_price(spot_array[i])
    
# ✅ Fast: Vectorized approach
prices = black_scholes_vectorized(spot_array, K, sigma, r, T)
```

<table>
<tr>
<td width="33%">

**💨 SIMD**
- Vector instructions
- Parallel processing
- Hardware acceleration

</td>
<td width="33%">

**🚫 No Loops**
- Eliminates Python loops
- Reduced overhead
- Batch efficiency

</td>
<td width="33%">

**📊 Batch**
- Process arrays
- Multiple at once
- Optimized memory access

</td>
</tr>
</table>

---

#### 3️⃣ Fast Approximations

**📐 Normal Distribution:**

```python
@jit(nopython=True, cache=True)
def norm_cdf(x):
    # ⚡ Fast tanh-based approximation
    return 0.5 * (1.0 + np.tanh(np.sqrt(2/np.pi) * (x + 0.044715 * x**3)))
```

<table>
<tr>
<td width="33%">

**⚡ Speed**
- Avoids scipy overhead
- Pure computation
- Inline optimization

</td>
<td width="33%">

**🎯 Accuracy**
- < 0.1% error
- Production quality
- Validated results

</td>
<td width="33%">

**🔄 Frequency**
- Called millions of times
- Cumulative speedup
- Major impact

</td>
</tr>
</table>

---

#### 4️⃣ Parallel Monte Carlo

```python
@jit(nopython=True, parallel=True, cache=True)
def monte_carlo_paths(S0, sigma, r, T, n_paths, n_steps):
    for i in prange(n_paths):  # 🔀 Parallel loop
        # Independent path generation
        ...
```

<table>
<tr>
<td width="33%">

**🔀 Multi-Core**
- All cores utilized
- Parallel execution
- Maximum throughput

</td>
<td width="33%">

**📈 Scaling**
- Linear with cores
- Predictable performance
- Efficient distribution

</td>
<td width="33%">

**🎯 Simple**
- No thread management
- Automatic distribution
- Easy to implement

</td>
</tr>
</table>

---

### 📊 Performance Benchmarks

**🧪 Run benchmarks:**

```bash
python scripts/benchmark_performance.py
```

#### 📈 Expected Results

<div align="center">

| Operation | Baseline | Optimized | Speedup | Status |
|-----------|----------|-----------|---------|--------|
| 🎯 **Single Pricing** | 100ms | 40ms | **60%** ↑ | ✅ |
| 📊 **Greeks Calculation** | 500ms | 250ms | **50%** ↑ | ✅ |
| 🔢 **Vectorized (1K prices)** | 2000ms | 200ms | **90%** ↑ | ✅ |
| 🎲 **Monte Carlo (10K paths)** | 3500ms | 1800ms | **48%** ↑ | ✅ |

</div>

**💻 Hardware:** Results shown for typical modern CPU (4-8 cores)

---

## 💻 Getting Started

> *Get up and running in minutes*

---

### 📦 Installation

#### ✅ Prerequisites

<div align="center">

| Requirement | Version | Status |
|-------------|---------|--------|
| 🐍 **Python** | 3.8 or higher | Required |
| 📦 **pip** | Latest | Required |
| 💻 **OS** | Windows/Mac/Linux | Any |

</div>

#### 🚀 Install Dependencies

```bash
# 📥 Install all required packages
pip install -r requirements.txt
```

**📚 Required Packages:**

<div align="center">

| Package | Version | Purpose |
|---------|---------|---------|
| **numpy** | >= 1.24.0 | Numerical computing |
| **scipy** | >= 1.10.0 | Scientific functions |
| **plotly** | >= 5.14.0 | Interactive charts |
| **dash** | >= 2.9.0 | Web dashboard |
| **pandas** | >= 2.0.0 | Data manipulation |
| **numba** | >= 0.57.0 | JIT compilation |

</div>

---

### 🎯 Quick Start Examples

#### Example 1️⃣: Price a Single Option

```python
from pricing import OptionParams, OptionsPricingEngine

# 🔧 Create pricing engine
engine = OptionsPricingEngine()

# 📝 Define call option
call = OptionParams(
    spot=100,           # 💵 Current price
    strike=105,         # 🎯 Strike price
    volatility=0.20,    # 📊 20% volatility
    rate=0.03,          # 💰 3% risk-free rate
    maturity=0.5,       # ⏰ 6 months
    option_type='call'  # 📈 Call option
)

# 💰 Calculate price and Greeks
price = engine.price(call)
greeks = engine.greeks(call)

print(f"💵 Call Price: ${price:.2f}")
print(f"📊 Delta: {greeks['delta']:.4f}")
```

---

#### Example 2️⃣: Compare American vs European

```python
# 🌍 European put
euro_put = OptionParams(
    spot=100, strike=100, volatility=0.25,
    rate=0.05, maturity=1.0, 
    option_type='put', style='european'
)

# 🇺🇸 American put (same parameters)
amer_put = OptionParams(
    spot=100, strike=100, volatility=0.25,
    rate=0.05, maturity=1.0, 
    option_type='put', style='american'
)

# 💵 Price both options
euro_price = engine.price(euro_put)
amer_price = engine.price(amer_put)

print(f"🌍 European Put: ${euro_price:.2f}")
print(f"🇺🇸 American Put: ${amer_price:.2f}")
print(f"💎 Early Exercise Premium: ${amer_price - euro_price:.2f}")
```

---

#### Example 3️⃣: Build and Hedge a Portfolio

```python
from hedging import Portfolio, Position, HedgingSimulator

# 📊 Create portfolio with long calls
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

# 🛡️ Simulate hedging strategies
simulator = HedgingSimulator()

results = simulator.compare_strategies(
    portfolio=portfolio,
    n_scenarios=1000
)

# 📊 Display results
print(f"📊 Unhedged Variance: ${results['no_hedge']['pnl_std']:.2f}")
print(f"🛡️ Delta Hedged Variance: ${results['delta_hedge']['pnl_std']:.2f}")
print(f"📉 Variance Reduction: {results['delta_hedge']['variance_reduction']:.1f}%")
```

---

### 🐳 Docker Deployment

#### 🏗️ Build Image

```bash
# 🔨 Build Docker image
docker build -t options-simulator .
```

#### 🚀 Run Container

```bash
# 🚀 Start container
docker run -p 8050:8050 options-simulator
```

**🌐 Access dashboard at:** http://localhost:8050

---

### 🧪 Running Tests

<table>
<tr>
<td width="50%">

#### ✅ Validate Pricing

```bash
# 🎯 Test pricing accuracy
python scripts/test_pricing.py
```

</td>
<td width="50%">

#### 🛡️ Test Hedging

```bash
# 🛡️ Test hedging strategies
python scripts/test_hedging.py
```

</td>
</tr>
<tr>
<td width="50%">

#### 📊 Benchmarks

```bash
# ⚡ Performance benchmarks
python scripts/benchmark_performance.py
```

</td>
<td width="50%">

#### 🎨 Launch Dashboard

```bash
# 🚀 Start dashboard
python scripts/run_dashboard.py
```

</td>
</tr>
</table>

---

## 📚 API Reference

> *Complete API documentation for developers*

---

### 📦 OptionParams Class

```python
@dataclass
class OptionParams:
    spot: float          # 💵 Current underlying price
    strike: float        # 🎯 Strike/exercise price
    volatility: float    # 📊 Annualized volatility (σ)
    rate: float          # 💰 Risk-free rate (annual)
    maturity: float      # ⏰ Time to maturity (years)
    option_type: Literal['call', 'put']
    style: Literal['european', 'american'] = 'european'
```

<div align="center">

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `spot` | float | Current underlying price | 100.0 |
| `strike` | float | Strike/exercise price | 105.0 |
| `volatility` | float | Annual volatility (σ) | 0.25 |
| `rate` | float | Risk-free rate (annual) | 0.05 |
| `maturity` | float | Time to maturity (years) | 1.0 |
| `option_type` | str | 'call' or 'put' | 'call' |
| `style` | str | 'european' or 'american' | 'european' |

</div>

---

### 💰 OptionsPricingEngine

```python
class OptionsPricingEngine:
    def __init__(self, binomial_steps: int = 100):
        """🔧 Initialize pricing engine
        
        Args:
            binomial_steps: Number of steps for binomial tree (default: 100)
        """
        
    def price(self, params: OptionParams) -> float:
        """💵 Calculate option price
        
        Args:
            params: Option parameters
            
        Returns:
            Option price (float)
        """
        
    def greeks(self, params: OptionParams) -> Dict[str, float]:
        """📊 Calculate all Greeks
        
        Args:
            params: Option parameters
            
        Returns:
            Dict: {'delta', 'gamma', 'vega', 'theta', 'rho'}
        """
```

---

### ⚡ OptimizedPricingEngine

```python
class OptimizedPricingEngine:
    def __init__(self, binomial_steps: int = 100):
        """🚀 Initialize optimized engine with JIT compilation
        
        Args:
            binomial_steps: Number of steps for binomial tree
        """
        
    def price(self, params: OptionParams) -> float:
        """💵 Price option (optimized)
        
        Returns: Option price
        """
        
    def greeks(self, params: OptionParams) -> Dict[str, float]:
        """📊 Calculate Greeks (optimized)
        
        Returns: All Greeks
        """
        
    def price_multiple(self, spot_array: np.ndarray, 
                      params: OptionParams) -> np.ndarray:
        """🔢 Vectorized pricing for multiple spot prices
        
        Args:
            spot_array: Array of spot prices
            params: Option parameters
            
        Returns:
            Array of option prices
        """
        
    def simulate_paths(self, S0: float, sigma: float, r: float,
                      T: float, n_paths: int, n_steps: int) -> np.ndarray:
        """🎲 Monte Carlo price path simulation
        
        Args:
            S0: Initial price
            sigma: Volatility
            r: Risk-free rate
            T: Time horizon
            n_paths: Number of paths
            n_steps: Steps per path
            
        Returns:
            Array of shape (n_paths, n_steps+1)
        """
```

---

### 🛡️ HedgingSimulator

```python
class HedgingSimulator:
    def __init__(self):
        """🔧 Initialize hedging simulator"""
        
    def delta_hedge(self, portfolio: Portfolio) -> Portfolio:
        """⚖️ Create delta-neutral hedge
        
        Args:
            portfolio: Original portfolio
            
        Returns:
            Hedged portfolio (Delta ≈ 0)
        """
        
    def gamma_hedge(self, portfolio: Portfolio, 
                   hedge_option_params: OptionParams) -> Portfolio:
        """🎲 Create delta and gamma-neutral hedge
        
        Args:
            portfolio: Original portfolio
            hedge_option_params: Hedge option parameters
            
        Returns:
            Hedged portfolio (Δ ≈ 0, Γ ≈ 0)
        """
        
    def calculate_portfolio_greeks(self, portfolio: Portfolio) -> Dict:
        """📊 Calculate aggregated portfolio Greeks
        
        Args:
            portfolio: Portfolio to analyze
            
        Returns:
            Dict: Portfolio Greeks
        """
        
    def simulate_hedging_effectiveness(
        self, portfolio: Portfolio,
        hedge_strategy: Literal['none', 'delta', 'gamma'],
        n_scenarios: int = 1000
    ) -> Dict:
        """🧪 Simulate hedging across market scenarios
        
        Args:
            portfolio: Portfolio to test
            hedge_strategy: Hedging approach
            n_scenarios: Number of scenarios
            
        Returns:
            Dict: Simulation results with metrics
        """
        
    def compare_strategies(self, portfolio: Portfolio,
                          n_scenarios: int = 1000,
                          hedge_option_params: OptionParams = None) -> Dict:
        """📊 Compare all hedging strategies
        
        Args:
            portfolio: Portfolio to analyze
            n_scenarios: Number of scenarios
            hedge_option_params: Optional hedge option
            
        Returns:
            Dict: Comparison results for all strategies
        """
```

---

## 🎯 Use Cases

> *Real-world applications and practical examples*

---

### 1️⃣ Option Pricing for Trading

**📊 Scenario:** Determine fair value of an option before trading

```python
from pricing import OptionParams, OptionsPricingEngine

# 🔧 Initialize engine
engine = OptionsPricingEngine()

# 📝 Market data (e.g., AAPL call option)
market_call = OptionParams(
    spot=150.25,      # 💵 Current AAPL price
    strike=155,       # 🎯 Strike price
    volatility=0.30,  # 📊 30% implied volatility
    rate=0.045,       # 💰 4.5% risk-free rate
    maturity=45/365,  # ⏰ 45 days to expiration
    option_type='call'
)

# 💵 Calculate fair value
fair_value = engine.price(market_call)
greeks = engine.greeks(market_call)

print(f"💵 Fair Value: ${fair_value:.2f}")
print(f"📊 Delta: {greeks['delta']:.3f}")

# 💡 Decision: If market price < fair value → potential buy opportunity
```

**💡 Use case:** Compare theoretical value to market price for trading decisions

---

### 2️⃣ Portfolio Risk Management

**🛡️ Scenario:** Manage delta exposure of an options portfolio

```python
from hedging import Portfolio, Position, HedgingSimulator

# 📦 Build portfolio
portfolio = Portfolio(positions=[
    Position(instrument_type='option', quantity=50,  # 📈 50 long calls
             params=call_option_1),
    Position(instrument_type='option', quantity=-30, # 📉 30 short puts
             params=put_option_1),
    Position(instrument_type='stock', quantity=100)  # 💰 100 shares
])

# 🔧 Initialize simulator
simulator = HedgingSimulator()

# 📊 Check current exposure
greeks = simulator.calculate_portfolio_greeks(portfolio)
print(f"📊 Portfolio Delta: {greeks['delta']:.2f}")
print(f"📊 Portfolio Gamma: {greeks['gamma']:.4f}")

# 🛡️ If |delta| > threshold, hedge it
if abs(greeks['delta']) > 50:
    hedged = simulator.delta_hedge(portfolio)
    print("✅ Portfolio hedged successfully!")
```

**💡 Use case:** Monitor and manage portfolio Greeks for risk control

---

### 3️⃣ Backtesting Hedging Strategies

**📊 Scenario:** Evaluate effectiveness of different hedging approaches

```python
simulator = HedgingSimulator()

# 🧪 Test portfolio under stressed conditions
results = simulator.compare_strategies(
    portfolio=portfolio,
    n_scenarios=5000,  # 🎲 5000 scenarios for robust testing
    hedge_option_params=hedge_option
)

# 📊 Analyze results
for strategy in ['no_hedge', 'delta_hedge', 'gamma_hedge']:
    stats = results[strategy]
    print(f"\n{'='*50}")
    print(f"📊 {strategy.upper()}:")
    print(f"  💵 Mean PnL: ${stats['pnl_mean']:.2f}")
    print(f"  📊 Std Dev: ${stats['pnl_std']:.2f}")
    print(f"  ⚠️  Max Loss: ${stats['max_loss']:.2f}")
    print(f"  📈 Sharpe Ratio: {stats['pnl_mean']/stats['pnl_std']:.2f}")
```

**💡 Use case:** Compare hedging strategies to optimize risk-return profile

---

### 4️⃣ Education & Learning

**🎓 Scenario:** Interactive learning about option Greeks

```bash
# 🚀 Launch the dashboard
python scripts/run_dashboard.py
```

**📚 Learning path in browser:**

1. 📊 Adjust spot price slider → observe **Delta** changes
2. ⏰ Change time to maturity → see **Theta** effect  
3. 🌊 Modify volatility → watch **Vega** impact
4. 🔄 Switch between call/put → compare Greeks
5. 🗺️ View 3D Delta surface → understand behavior

**💡 Use case:** Hands-on learning for students and professionals

---

### 5️⃣ Performance-Critical Applications

**⚡ Scenario:** Price thousands of options for real-time risk systems

```python
from pricing_optimized import OptimizedPricingEngine
import numpy as np
import time

# 🚀 Initialize optimized engine
engine = OptimizedPricingEngine()

# 📊 Generate spot price grid (10,000 prices!)
spots = np.linspace(80, 120, 10000)

# 📝 Base option parameters
params = OptionParams(
    spot=100, strike=100, volatility=0.25,
    rate=0.05, maturity=1.0, option_type='call'
)

# ⚡ Vectorized pricing (blazingly fast!)
start = time.time()
prices = engine.price_multiple(spots, params)
elapsed = time.time() - start

print(f"✅ Priced {len(spots):,} options in {elapsed:.3f}s")
print(f"🚀 Rate: {len(spots)/elapsed:,.0f} prices/second")
```

**💡 Use case:** Real-time risk systems and high-frequency applications

---

### 6️⃣ Stress Testing

**⚠️ Scenario:** Test portfolio under extreme market conditions

```python
from hedging import MarketScenario
import numpy as np

# 🎲 Generate extreme scenarios
extreme_scenarios = MarketScenario.generate_scenarios(
    base_spot=100,
    base_vol=0.25,
    n_scenarios=1000,
    spot_shock_range=(-0.3, 0.3),    # ±30% price moves
    vol_shock_range=(-0.7, 1.0),      # Volatility spikes
    time_step=5/252                    # 5 trading days
)

# 🧪 Test portfolio performance
pnls = []
for scenario in extreme_scenarios:
    value = simulator.calculate_portfolio_value(
        portfolio, 
        scenario['spot'], 
        scenario['volatility'],
        scenario['time_elapsed']
    )
    pnls.append(value)

# 📊 Calculate risk metrics
var_95 = np.percentile(pnls, 5)  # 📉 Value at Risk (95%)
cvar_95 = np.mean([p for p in pnls if p < var_95])  # 📉 Conditional VaR

print(f"⚠️  95% VaR: ${var_95:.2f}")
print(f"⚠️  95% CVaR: ${cvar_95:.2f}")
```

**💡 Use case:** Stress testing and tail risk analysis

---

## 🎉 Conclusion

> *A comprehensive toolkit for modern quantitative finance*

The **Options Pricing & Hedging Simulator** provides a complete solution for options analysis, from basic pricing to sophisticated hedging strategies. Its combination of accuracy, performance, and usability makes it suitable for both educational and professional applications.

---

### 🎯 Key Takeaways

<div align="center">

| Feature | Description | Status |
|---------|-------------|--------|
| 🎯 **Accurate** | Validated against academic benchmarks (≤ 0.5% error) | ✅ |
| ⚡ **Fast** | Optimized for real-time applications (< 1s updates) | ✅ |
| 📚 **Comprehensive** | Covers pricing, Greeks, and hedging | ✅ |
| 🎨 **Interactive** | Professional dashboard for visualization | ✅ |
| 🔧 **Flexible** | Both baseline and optimized engines available | ✅ |
| 🎓 **Educational** | Clear code structure for learning | ✅ |

</div>

---

### 🚀 Next Steps

<table>
<tr>
<td width="50%">

#### 🎨 Explore
- Launch the interactive dashboard
- Try different option parameters
- Visualize Greeks behavior
- Experiment with 3D surfaces

</td>
<td width="50%">

#### 🧪 Validate
- Run validation scripts
- Check pricing accuracy
- Benchmark performance
- Test hedging strategies

</td>
</tr>
<tr>
<td width="50%">

#### 🔬 Experiment
- Try different strategies
- Build custom portfolios
- Stress test positions
- Analyze risk metrics

</td>
<td width="50%">

#### 🤝 Contribute
- Integrate into your apps
- Add new features
- Share improvements
- Join the community

</td>
</tr>
</table>

---

### 📚 Resources

<div align="center">

| Resource | Link | Description |
|----------|------|-------------|
| 📦 **Repository** | [GitHub](https://github.com/johaankjis/Options-Pricing---Greeks-Hedging-Simulator) | Source code & issues |
| 📖 **Quick Start** | [README.md](README.md) | Installation & basics |
| 📚 **Full Guide** | This document | Comprehensive API reference |
| 🎓 **Examples** | [Use Cases](#use-cases) | Practical examples |

</div>

---

<div align="center">

### 🌟 Thank You for Using Our Simulator! 🌟

*Built with ❤️ for the quantitative finance community*

[![GitHub stars](https://img.shields.io/github/stars/johaankjis/Options-Pricing---Greeks-Hedging-Simulator?style=social)](https://github.com/johaankjis/Options-Pricing---Greeks-Hedging-Simulator)

**Questions? Issues? Contributions?**

[Report Bug](https://github.com/johaankjis/Options-Pricing---Greeks-Hedging-Simulator/issues) • [Request Feature](https://github.com/johaankjis/Options-Pricing---Greeks-Hedging-Simulator/issues) • [Discuss](https://github.com/johaankjis/Options-Pricing---Greeks-Hedging-Simulator/discussions)

---

*Happy trading and hedging! 📈🛡️💰*

</div>
