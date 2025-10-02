"""
Options Pricing Engine
Implements Black-Scholes and Binomial Tree models for European and American options
Target accuracy: ≤ 0.5% error vs benchmark data
"""

import numpy as np
from scipy.stats import norm
from typing import Literal, Dict
from dataclasses import dataclass


@dataclass
class OptionParams:
    """Parameters for option pricing"""
    spot: float  # Current stock price
    strike: float  # Strike price
    volatility: float  # Annualized volatility (sigma)
    rate: float  # Risk-free interest rate
    maturity: float  # Time to maturity in years
    option_type: Literal['call', 'put']
    style: Literal['european', 'american'] = 'european'


class BlackScholesModel:
    """
    Black-Scholes model for European option pricing
    Provides analytical solution for calls and puts
    """
    
    @staticmethod
    def price(params: OptionParams) -> float:
        """
        Calculate option price using Black-Scholes formula
        
        Args:
            params: OptionParams with pricing parameters
            
        Returns:
            Option price
        """
        S = params.spot
        K = params.strike
        sigma = params.volatility
        r = params.rate
        T = params.maturity
        
        # Calculate d1 and d2
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if params.option_type == 'call':
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:  # put
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
        return price
    
    @staticmethod
    def calculate_greeks(params: OptionParams) -> Dict[str, float]:
        """
        Calculate option Greeks (Delta, Gamma, Vega, Theta, Rho)
        
        Args:
            params: OptionParams with pricing parameters
            
        Returns:
            Dictionary with Greek values
        """
        S = params.spot
        K = params.strike
        sigma = params.volatility
        r = params.rate
        T = params.maturity
        
        # Calculate d1 and d2
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        # Common terms
        pdf_d1 = norm.pdf(d1)
        cdf_d1 = norm.cdf(d1)
        cdf_d2 = norm.cdf(d2)
        
        # Delta
        if params.option_type == 'call':
            delta = cdf_d1
        else:
            delta = cdf_d1 - 1
        
        # Gamma (same for calls and puts)
        gamma = pdf_d1 / (S * sigma * np.sqrt(T))
        
        # Vega (same for calls and puts, divided by 100 for 1% change)
        vega = S * pdf_d1 * np.sqrt(T) / 100
        
        # Theta (per day, divided by 365)
        if params.option_type == 'call':
            theta = (-(S * pdf_d1 * sigma) / (2 * np.sqrt(T)) 
                    - r * K * np.exp(-r * T) * cdf_d2) / 365
        else:
            theta = (-(S * pdf_d1 * sigma) / (2 * np.sqrt(T)) 
                    + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
        
        # Rho (divided by 100 for 1% change)
        if params.option_type == 'call':
            rho = K * T * np.exp(-r * T) * cdf_d2 / 100
        else:
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
        
        return {
            'delta': delta,
            'gamma': gamma,
            'vega': vega,
            'theta': theta,
            'rho': rho
        }


class BinomialTreeModel:
    """
    Binomial Tree model for American and European option pricing
    Supports early exercise for American options
    """
    
    def __init__(self, steps: int = 100):
        """
        Initialize binomial tree model
        
        Args:
            steps: Number of time steps in the tree (more steps = higher accuracy)
        """
        self.steps = steps
    
    def price(self, params: OptionParams) -> float:
        """
        Calculate option price using binomial tree
        
        Args:
            params: OptionParams with pricing parameters
            
        Returns:
            Option price
        """
        S = params.spot
        K = params.strike
        sigma = params.volatility
        r = params.rate
        T = params.maturity
        N = self.steps
        
        # Calculate parameters
        dt = T / N
        u = np.exp(sigma * np.sqrt(dt))  # Up factor
        d = 1 / u  # Down factor
        p = (np.exp(r * dt) - d) / (u - d)  # Risk-neutral probability
        discount = np.exp(-r * dt)
        
        # Initialize asset prices at maturity
        asset_prices = np.zeros(N + 1)
        for i in range(N + 1):
            asset_prices[i] = S * (u ** (N - i)) * (d ** i)
        
        # Initialize option values at maturity
        if params.option_type == 'call':
            option_values = np.maximum(asset_prices - K, 0)
        else:
            option_values = np.maximum(K - asset_prices, 0)
        
        # Backward induction through the tree
        for step in range(N - 1, -1, -1):
            for i in range(step + 1):
                # Calculate option value from next period
                option_values[i] = discount * (p * option_values[i] + (1 - p) * option_values[i + 1])
                
                # For American options, check early exercise
                if params.style == 'american':
                    asset_price = S * (u ** (step - i)) * (d ** i)
                    if params.option_type == 'call':
                        intrinsic = max(asset_price - K, 0)
                    else:
                        intrinsic = max(K - asset_price, 0)
                    option_values[i] = max(option_values[i], intrinsic)
        
        return option_values[0]


class OptionsPricingEngine:
    """
    Main pricing engine that routes to appropriate model
    """
    
    def __init__(self):
        self.bs_model = BlackScholesModel()
        self.binomial_model = BinomialTreeModel(steps=100)
    
    def price(self, params: OptionParams) -> float:
        """
        Price an option using the appropriate model
        
        Args:
            params: OptionParams with pricing parameters
            
        Returns:
            Option price
        """
        if params.style == 'european':
            # Use Black-Scholes for European options (faster and exact)
            return self.bs_model.price(params)
        else:
            # Use binomial tree for American options
            return self.binomial_model.price(params)
    
    def greeks(self, params: OptionParams) -> Dict[str, float]:
        """
        Calculate Greeks for an option
        
        Args:
            params: OptionParams with pricing parameters
            
        Returns:
            Dictionary with Greek values
        """
        if params.style == 'european':
            return self.bs_model.calculate_greeks(params)
        else:
            # For American options, use numerical approximation
            return self._numerical_greeks(params)
    
    def _numerical_greeks(self, params: OptionParams) -> Dict[str, float]:
        """
        Calculate Greeks numerically for American options
        """
        base_price = self.binomial_model.price(params)
        
        # Delta: dV/dS
        h = 0.01 * params.spot
        params_up = OptionParams(**{**params.__dict__, 'spot': params.spot + h})
        params_down = OptionParams(**{**params.__dict__, 'spot': params.spot - h})
        delta = (self.binomial_model.price(params_up) - self.binomial_model.price(params_down)) / (2 * h)
        
        # Gamma: d²V/dS²
        price_up = self.binomial_model.price(params_up)
        price_down = self.binomial_model.price(params_down)
        gamma = (price_up - 2 * base_price + price_down) / (h ** 2)
        
        # Vega: dV/dσ (per 1% change)
        h_vol = 0.01
        params_vol_up = OptionParams(**{**params.__dict__, 'volatility': params.volatility + h_vol})
        vega = (self.binomial_model.price(params_vol_up) - base_price) / 1
        
        # Theta: dV/dt (per day)
        h_time = 1 / 365
        if params.maturity > h_time:
            params_time = OptionParams(**{**params.__dict__, 'maturity': params.maturity - h_time})
            theta = self.binomial_model.price(params_time) - base_price
        else:
            theta = 0
        
        # Rho: dV/dr (per 1% change)
        h_rate = 0.01
        params_rate_up = OptionParams(**{**params.__dict__, 'rate': params.rate + h_rate})
        rho = (self.binomial_model.price(params_rate_up) - base_price) / 1
        
        return {
            'delta': delta,
            'gamma': gamma,
            'vega': vega,
            'theta': theta,
            'rho': rho
        }


# Convenience function for quick pricing
def price_option(
    spot: float,
    strike: float,
    volatility: float,
    rate: float,
    maturity: float,
    option_type: Literal['call', 'put'],
    style: Literal['european', 'american'] = 'european'
) -> float:
    """
    Quick function to price an option
    
    Example:
        >>> price = price_option(100, 105, 0.2, 0.05, 1.0, 'call')
    """
    params = OptionParams(spot, strike, volatility, rate, maturity, option_type, style)
    engine = OptionsPricingEngine()
    return engine.price(params)
