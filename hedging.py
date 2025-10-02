"""
Hedging Simulator
Implements Delta-neutral and Gamma-neutral hedging strategies
Runs Monte Carlo simulations across 1,000+ market scenarios
"""

import numpy as np
from typing import Dict, List, Literal, Tuple
from dataclasses import dataclass
from pricing import OptionParams, OptionsPricingEngine


@dataclass
class Position:
    """Represents a position in an option or underlying"""
    instrument_type: Literal['option', 'stock']
    quantity: float
    params: OptionParams = None  # Only for options


@dataclass
class Portfolio:
    """Portfolio of options and stock positions"""
    positions: List[Position]
    
    def add_position(self, position: Position):
        """Add a position to the portfolio"""
        self.positions.append(position)
    
    def clear_hedges(self):
        """Remove all hedging positions (keep only original positions)"""
        self.positions = [p for p in self.positions if not hasattr(p, 'is_hedge')]


class MarketScenario:
    """
    Generates randomized market scenarios for stress testing
    """
    
    @staticmethod
    def generate_scenarios(
        base_spot: float,
        base_vol: float,
        n_scenarios: int = 1000,
        spot_shock_range: Tuple[float, float] = (-0.2, 0.2),
        vol_shock_range: Tuple[float, float] = (-0.5, 0.5),
        time_step: float = 1/252  # 1 day
    ) -> List[Dict]:
        """
        Generate random market scenarios
        
        Args:
            base_spot: Current spot price
            base_vol: Current volatility
            n_scenarios: Number of scenarios to generate
            spot_shock_range: Range for spot price shocks (as fraction)
            vol_shock_range: Range for volatility shocks (as fraction)
            time_step: Time step for scenarios (default: 1 trading day)
            
        Returns:
            List of scenario dictionaries with spot, vol, and time changes
        """
        scenarios = []
        
        for _ in range(n_scenarios):
            # Random spot price shock
            spot_shock = np.random.uniform(*spot_shock_range)
            new_spot = base_spot * (1 + spot_shock)
            
            # Random volatility shock
            vol_shock = np.random.uniform(*vol_shock_range)
            new_vol = base_vol * (1 + vol_shock)
            new_vol = max(0.01, new_vol)  # Ensure vol stays positive
            
            scenarios.append({
                'spot': new_spot,
                'volatility': new_vol,
                'time_elapsed': time_step,
                'spot_shock': spot_shock,
                'vol_shock': vol_shock
            })
        
        return scenarios


class HedgingSimulator:
    """
    Simulates hedging strategies and measures effectiveness
    """
    
    def __init__(self):
        self.engine = OptionsPricingEngine()
    
    def calculate_portfolio_value(
        self, 
        portfolio: Portfolio,
        spot: float,
        volatility: float = None,
        time_elapsed: float = 0
    ) -> float:
        """
        Calculate total portfolio value
        
        Args:
            portfolio: Portfolio to value
            spot: Current spot price
            volatility: Current volatility (if changed)
            time_elapsed: Time elapsed since position inception
            
        Returns:
            Total portfolio value
        """
        total_value = 0
        
        for position in portfolio.positions:
            if position.instrument_type == 'stock':
                # Stock position value
                total_value += position.quantity * spot
            else:
                # Option position value
                params = position.params
                
                # Update parameters for current market conditions
                updated_params = OptionParams(
                    spot=spot,
                    strike=params.strike,
                    volatility=volatility if volatility else params.volatility,
                    rate=params.rate,
                    maturity=max(0.001, params.maturity - time_elapsed),
                    option_type=params.option_type,
                    style=params.style
                )
                
                option_value = self.engine.price(updated_params)
                total_value += position.quantity * option_value
        
        return total_value
    
    def calculate_portfolio_greeks(self, portfolio: Portfolio) -> Dict[str, float]:
        """
        Calculate aggregate Greeks for entire portfolio
        
        Args:
            portfolio: Portfolio to analyze
            
        Returns:
            Dictionary with aggregate Greek values
        """
        total_greeks = {'delta': 0, 'gamma': 0, 'vega': 0, 'theta': 0, 'rho': 0}
        
        for position in portfolio.positions:
            if position.instrument_type == 'stock':
                # Stock has delta of 1, other Greeks are 0
                total_greeks['delta'] += position.quantity
            else:
                # Calculate option Greeks
                greeks = self.engine.greeks(position.params)
                for greek_name, greek_value in greeks.items():
                    total_greeks[greek_name] += position.quantity * greek_value
        
        return total_greeks
    
    def delta_hedge(self, portfolio: Portfolio) -> Portfolio:
        """
        Create delta-neutral hedge by adding stock position
        
        Args:
            portfolio: Original portfolio
            
        Returns:
            Hedged portfolio
        """
        # Calculate portfolio delta
        greeks = self.calculate_portfolio_greeks(portfolio)
        portfolio_delta = greeks['delta']
        
        # Create hedged portfolio (copy original positions)
        hedged = Portfolio(positions=portfolio.positions.copy())
        
        # Add stock position to neutralize delta
        # If portfolio delta is positive, short stock (negative quantity)
        hedge_quantity = -portfolio_delta
        
        if abs(hedge_quantity) > 0.001:  # Only hedge if delta is significant
            hedge_position = Position(
                instrument_type='stock',
                quantity=hedge_quantity
            )
            hedge_position.is_hedge = True  # Mark as hedge position
            hedged.add_position(hedge_position)
        
        return hedged
    
    def gamma_hedge(self, portfolio: Portfolio, hedge_option_params: OptionParams) -> Portfolio:
        """
        Create gamma-neutral hedge using another option
        
        Args:
            portfolio: Original portfolio
            hedge_option_params: Parameters for the option to use as hedge
            
        Returns:
            Hedged portfolio (gamma and delta neutral)
        """
        # Calculate portfolio Greeks
        portfolio_greeks = self.calculate_portfolio_greeks(portfolio)
        
        # Calculate Greeks of hedge option
        hedge_greeks = self.engine.greeks(hedge_option_params)
        
        # Determine quantity of hedge option needed to neutralize gamma
        # portfolio_gamma + quantity * hedge_gamma = 0
        hedge_quantity = -portfolio_greeks['gamma'] / hedge_greeks['gamma']
        
        # Create hedged portfolio
        hedged = Portfolio(positions=portfolio.positions.copy())
        
        # Add hedge option
        hedge_option = Position(
            instrument_type='option',
            quantity=hedge_quantity,
            params=hedge_option_params
        )
        hedge_option.is_hedge = True
        hedged.add_position(hedge_option)
        
        # Now delta hedge the combined portfolio
        hedged = self.delta_hedge(hedged)
        
        return hedged
    
    def simulate_hedging_effectiveness(
        self,
        portfolio: Portfolio,
        hedge_strategy: Literal['none', 'delta', 'gamma'],
        n_scenarios: int = 1000,
        hedge_option_params: OptionParams = None
    ) -> Dict:
        """
        Simulate hedging effectiveness across multiple scenarios
        
        Args:
            portfolio: Original portfolio to hedge
            hedge_strategy: 'none', 'delta', or 'gamma'
            n_scenarios: Number of scenarios to simulate
            hedge_option_params: Option params for gamma hedging
            
        Returns:
            Dictionary with simulation results and statistics
        """
        # Get base parameters from first option in portfolio
        base_params = None
        for pos in portfolio.positions:
            if pos.instrument_type == 'option':
                base_params = pos.params
                break
        
        if base_params is None:
            raise ValueError("Portfolio must contain at least one option")
        
        # Apply hedging strategy
        if hedge_strategy == 'delta':
            hedged_portfolio = self.delta_hedge(portfolio)
        elif hedge_strategy == 'gamma':
            if hedge_option_params is None:
                raise ValueError("hedge_option_params required for gamma hedging")
            hedged_portfolio = self.gamma_hedge(portfolio, hedge_option_params)
        else:
            hedged_portfolio = portfolio
        
        # Calculate initial values
        initial_value = self.calculate_portfolio_value(
            hedged_portfolio, 
            base_params.spot, 
            base_params.volatility
        )
        
        # Generate scenarios
        scenarios = MarketScenario.generate_scenarios(
            base_spot=base_params.spot,
            base_vol=base_params.volatility,
            n_scenarios=n_scenarios
        )
        
        # Simulate PnL across scenarios
        pnl_values = []
        
        for scenario in scenarios:
            new_value = self.calculate_portfolio_value(
                hedged_portfolio,
                spot=scenario['spot'],
                volatility=scenario['volatility'],
                time_elapsed=scenario['time_elapsed']
            )
            
            pnl = new_value - initial_value
            pnl_values.append(pnl)
        
        pnl_array = np.array(pnl_values)
        
        # Calculate statistics
        results = {
            'strategy': hedge_strategy,
            'n_scenarios': n_scenarios,
            'initial_value': initial_value,
            'pnl_mean': np.mean(pnl_array),
            'pnl_std': np.std(pnl_array),
            'pnl_var': np.var(pnl_array),
            'pnl_min': np.min(pnl_array),
            'pnl_max': np.max(pnl_array),
            'pnl_percentiles': {
                '5th': np.percentile(pnl_array, 5),
                '25th': np.percentile(pnl_array, 25),
                '50th': np.percentile(pnl_array, 50),
                '75th': np.percentile(pnl_array, 75),
                '95th': np.percentile(pnl_array, 95),
            },
            'pnl_values': pnl_values,
            'scenarios': scenarios,
            'portfolio_greeks': self.calculate_portfolio_greeks(hedged_portfolio)
        }
        
        return results
    
    def compare_strategies(
        self,
        portfolio: Portfolio,
        n_scenarios: int = 1000,
        hedge_option_params: OptionParams = None
    ) -> Dict:
        """
        Compare effectiveness of different hedging strategies
        
        Args:
            portfolio: Portfolio to hedge
            n_scenarios: Number of scenarios to simulate
            hedge_option_params: Option params for gamma hedging
            
        Returns:
            Comparison results with variance reduction metrics
        """
        print("=" * 70)
        print("HEDGING STRATEGY COMPARISON")
        print("=" * 70)
        
        # Simulate each strategy
        no_hedge = self.simulate_hedging_effectiveness(
            portfolio, 'none', n_scenarios
        )
        
        delta_hedge = self.simulate_hedging_effectiveness(
            portfolio, 'delta', n_scenarios
        )
        
        gamma_hedge = None
        if hedge_option_params:
            gamma_hedge = self.simulate_hedging_effectiveness(
                portfolio, 'gamma', n_scenarios, hedge_option_params
            )
        
        # Calculate variance reduction
        base_variance = no_hedge['pnl_var']
        delta_variance = delta_hedge['pnl_var']
        delta_reduction = (1 - delta_variance / base_variance) * 100
        
        print(f"\nSimulation: {n_scenarios} scenarios")
        print(f"Initial Portfolio Value: ${no_hedge['initial_value']:.2f}")
        print("-" * 70)
        print(f"{'Strategy':<20} {'PnL Std':<15} {'Variance':<15} {'Reduction':<15}")
        print("-" * 70)
        print(f"{'No Hedge':<20} ${no_hedge['pnl_std']:<14.2f} ${base_variance:<14.2f} {'—':<15}")
        print(f"{'Delta Hedge':<20} ${delta_hedge['pnl_std']:<14.2f} ${delta_variance:<14.2f} {delta_reduction:<14.1f}%")
        
        if gamma_hedge:
            gamma_variance = gamma_hedge['pnl_var']
            gamma_reduction = (1 - gamma_variance / base_variance) * 100
            print(f"{'Gamma Hedge':<20} ${gamma_hedge['pnl_std']:<14.2f} ${gamma_variance:<14.2f} {gamma_reduction:<14.1f}%")
        
        print("-" * 70)
        
        # Portfolio Greeks
        print("\nPortfolio Greeks:")
        print(f"  No Hedge:    Delta={no_hedge['portfolio_greeks']['delta']:.4f}, "
              f"Gamma={no_hedge['portfolio_greeks']['gamma']:.4f}")
        print(f"  Delta Hedge: Delta={delta_hedge['portfolio_greeks']['delta']:.4f}, "
              f"Gamma={delta_hedge['portfolio_greeks']['gamma']:.4f}")
        
        if gamma_hedge:
            print(f"  Gamma Hedge: Delta={gamma_hedge['portfolio_greeks']['delta']:.4f}, "
                  f"Gamma={gamma_hedge['portfolio_greeks']['gamma']:.4f}")
        
        print("=" * 70)
        
        # Check if target met (≥15% variance reduction)
        target_met = delta_reduction >= 15
        print(f"\nTarget Met: {'YES' if target_met else 'NO'} "
              f"(target: ≥15% variance reduction, achieved: {delta_reduction:.1f}%)")
        print("=" * 70)
        
        return {
            'no_hedge': no_hedge,
            'delta_hedge': delta_hedge,
            'gamma_hedge': gamma_hedge,
            'delta_variance_reduction': delta_reduction,
            'gamma_variance_reduction': gamma_reduction if gamma_hedge else None,
            'target_met': target_met
        }
