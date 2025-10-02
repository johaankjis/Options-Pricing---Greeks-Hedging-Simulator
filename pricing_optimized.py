"""
Optimized Options Pricing Engine
Uses NumPy vectorization and Numba JIT compilation
Target: 40% faster than baseline, 10,000 paths in < 2s
"""

import numpy as np
from scipy.stats import norm
from numba import jit, prange
from typing import Literal, Dict
from dataclasses import dataclass


@dataclass
class OptionParams:
    """Parameters for option pricing"""
    spot: float
    strike: float
    volatility: float
    rate: float
    maturity: float
    option_type: Literal['call', 'put']
    style: Literal['european', 'american'] = 'european'


@jit(nopython=True, cache=True)
def norm_cdf(x):
    """Fast approximation of cumulative normal distribution"""
    return 0.5 * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * x**3)))


@jit(nopython=True, cache=True)
def norm_pdf(x):
    """Fast approximation of normal probability density function"""
    return np.exp(-0.5 * x**2) / np.sqrt(2.0 * np.pi)


@jit(nopython=True, cache=True)
def black_scholes_price(S, K, sigma, r, T, is_call):
    """
    Optimized Black-Scholes pricing with Numba JIT
    
    Args:
        S: Spot price
        K: Strike price
        sigma: Volatility
        r: Risk-free rate
        T: Time to maturity
        is_call: True for call, False for put
        
    Returns:
        Option price
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if is_call:
        price = S * norm_cdf(d1) - K * np.exp(-r * T) * norm_cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)
    
    return price


@jit(nopython=True, cache=True)
def black_scholes_greeks(S, K, sigma, r, T, is_call):
    """
    Optimized Greeks calculation with Numba JIT
    
    Returns:
        Tuple of (delta, gamma, vega, theta, rho)
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    pdf_d1 = norm_pdf(d1)
    cdf_d1 = norm_cdf(d1)
    cdf_d2 = norm_cdf(d2)
    
    # Delta
    if is_call:
        delta = cdf_d1
    else:
        delta = cdf_d1 - 1.0
    
    # Gamma (same for calls and puts)
    gamma = pdf_d1 / (S * sigma * np.sqrt(T))
    
    # Vega (per 1% change)
    vega = S * pdf_d1 * np.sqrt(T) / 100.0
    
    # Theta (per day)
    if is_call:
        theta = (-(S * pdf_d1 * sigma) / (2.0 * np.sqrt(T)) 
                - r * K * np.exp(-r * T) * cdf_d2) / 365.0
    else:
        theta = (-(S * pdf_d1 * sigma) / (2.0 * np.sqrt(T)) 
                + r * K * np.exp(-r * T) * norm_cdf(-d2)) / 365.0
    
    # Rho (per 1% change)
    if is_call:
        rho = K * T * np.exp(-r * T) * cdf_d2 / 100.0
    else:
        rho = -K * T * np.exp(-r * T) * norm_cdf(-d2) / 100.0
    
    return delta, gamma, vega, theta, rho


@jit(nopython=True, cache=True)
def binomial_tree_price(S, K, sigma, r, T, N, is_call, is_american):
    """
    Optimized binomial tree pricing with Numba JIT
    
    Args:
        S: Spot price
        K: Strike price
        sigma: Volatility
        r: Risk-free rate
        T: Time to maturity
        N: Number of steps
        is_call: True for call, False for put
        is_american: True for American, False for European
        
    Returns:
        Option price
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    p = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)
    
    # Initialize asset prices at maturity
    asset_prices = np.zeros(N + 1)
    for i in range(N + 1):
        asset_prices[i] = S * (u ** (N - i)) * (d ** i)
    
    # Initialize option values at maturity
    option_values = np.zeros(N + 1)
    for i in range(N + 1):
        if is_call:
            option_values[i] = max(asset_prices[i] - K, 0.0)
        else:
            option_values[i] = max(K - asset_prices[i], 0.0)
    
    # Backward induction
    for step in range(N - 1, -1, -1):
        for i in range(step + 1):
            option_values[i] = discount * (p * option_values[i] + (1.0 - p) * option_values[i + 1])
            
            if is_american:
                asset_price = S * (u ** (step - i)) * (d ** i)
                if is_call:
                    intrinsic = max(asset_price - K, 0.0)
                else:
                    intrinsic = max(K - asset_price, 0.0)
                option_values[i] = max(option_values[i], intrinsic)
    
    return option_values[0]


@jit(nopython=True, parallel=True, cache=True)
def monte_carlo_paths(S0, sigma, r, T, n_paths, n_steps):
    """
    Vectorized Monte Carlo path generation with parallel execution
    
    Args:
        S0: Initial spot price
        sigma: Volatility
        r: Risk-free rate
        T: Time horizon
        n_paths: Number of simulation paths
        n_steps: Number of time steps
        
    Returns:
        Array of shape (n_paths, n_steps+1) with price paths
    """
    dt = T / n_steps
    paths = np.zeros((n_paths, n_steps + 1))
    paths[:, 0] = S0
    
    # Parallel loop over paths
    for i in prange(n_paths):
        for j in range(n_steps):
            z = np.random.randn()
            paths[i, j + 1] = paths[i, j] * np.exp(
                (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
            )
    
    return paths


@jit(nopython=True, parallel=True, cache=True)
def vectorized_option_pricing(spot_array, K, sigma, r, T, is_call):
    """
    Vectorized option pricing for multiple spot prices
    
    Args:
        spot_array: Array of spot prices
        K: Strike price
        sigma: Volatility
        r: Risk-free rate
        T: Time to maturity
        is_call: True for call, False for put
        
    Returns:
        Array of option prices
    """
    n = len(spot_array)
    prices = np.zeros(n)
    
    for i in prange(n):
        prices[i] = black_scholes_price(spot_array[i], K, sigma, r, T, is_call)
    
    return prices


class OptimizedPricingEngine:
    """
    High-performance pricing engine using Numba JIT compilation
    """
    
    def __init__(self, binomial_steps: int = 100):
        self.binomial_steps = binomial_steps
    
    def price(self, params: OptionParams) -> float:
        """Price an option using optimized methods"""
        is_call = params.option_type == 'call'
        
        if params.style == 'european':
            return black_scholes_price(
                params.spot, params.strike, params.volatility,
                params.rate, params.maturity, is_call
            )
        else:
            return binomial_tree_price(
                params.spot, params.strike, params.volatility,
                params.rate, params.maturity, self.binomial_steps,
                is_call, True
            )
    
    def greeks(self, params: OptionParams) -> Dict[str, float]:
        """Calculate Greeks using optimized methods"""
        if params.style == 'european':
            is_call = params.option_type == 'call'
            delta, gamma, vega, theta, rho = black_scholes_greeks(
                params.spot, params.strike, params.volatility,
                params.rate, params.maturity, is_call
            )
            
            return {
                'delta': delta,
                'gamma': gamma,
                'vega': vega,
                'theta': theta,
                'rho': rho
            }
        else:
            # Numerical Greeks for American options
            return self._numerical_greeks(params)
    
    def _numerical_greeks(self, params: OptionParams) -> Dict[str, float]:
        """Numerical Greeks calculation"""
        base_price = self.price(params)
        
        # Delta
        h = 0.01 * params.spot
        is_call = params.option_type == 'call'
        price_up = binomial_tree_price(
            params.spot + h, params.strike, params.volatility,
            params.rate, params.maturity, self.binomial_steps, is_call, True
        )
        price_down = binomial_tree_price(
            params.spot - h, params.strike, params.volatility,
            params.rate, params.maturity, self.binomial_steps, is_call, True
        )
        delta = (price_up - price_down) / (2 * h)
        
        # Gamma
        gamma = (price_up - 2 * base_price + price_down) / (h ** 2)
        
        # Vega
        h_vol = 0.01
        price_vol_up = binomial_tree_price(
            params.spot, params.strike, params.volatility + h_vol,
            params.rate, params.maturity, self.binomial_steps, is_call, True
        )
        vega = (price_vol_up - base_price) / 1.0
        
        # Theta
        h_time = 1 / 365
        if params.maturity > h_time:
            price_time = binomial_tree_price(
                params.spot, params.strike, params.volatility,
                params.rate, params.maturity - h_time, self.binomial_steps, is_call, True
            )
            theta = price_time - base_price
        else:
            theta = 0.0
        
        # Rho
        h_rate = 0.01
        price_rate_up = binomial_tree_price(
            params.spot, params.strike, params.volatility,
            params.rate + h_rate, params.maturity, self.binomial_steps, is_call, True
        )
        rho = (price_rate_up - base_price) / 1.0
        
        return {
            'delta': delta,
            'gamma': gamma,
            'vega': vega,
            'theta': theta,
            'rho': rho
        }
    
    def price_multiple(self, spot_array: np.ndarray, params: OptionParams) -> np.ndarray:
        """
        Price options for multiple spot prices (vectorized)
        
        Args:
            spot_array: Array of spot prices
            params: Option parameters (spot will be overridden)
            
        Returns:
            Array of option prices
        """
        is_call = params.option_type == 'call'
        return vectorized_option_pricing(
            spot_array, params.strike, params.volatility,
            params.rate, params.maturity, is_call
        )
    
    def simulate_paths(
        self, 
        S0: float, 
        sigma: float, 
        r: float, 
        T: float, 
        n_paths: int = 10000, 
        n_steps: int = 252
    ) -> np.ndarray:
        """
        Generate Monte Carlo price paths (optimized)
        
        Args:
            S0: Initial spot price
            sigma: Volatility
            r: Risk-free rate
            T: Time horizon
            n_paths: Number of paths
            n_steps: Number of time steps
            
        Returns:
            Array of shape (n_paths, n_steps+1)
        """
        return monte_carlo_paths(S0, sigma, r, T, n_paths, n_steps)
