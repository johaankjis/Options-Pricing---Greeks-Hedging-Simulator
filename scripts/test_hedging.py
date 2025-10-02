"""
Test script to validate hedging simulator
Demonstrates delta and gamma hedging effectiveness
"""

import sys
sys.path.append('..')

from pricing import OptionParams
from hedging import Portfolio, Position, HedgingSimulator


def create_sample_portfolio():
    """Create a sample portfolio with long call options"""
    # Long 10 ATM call options
    call_params = OptionParams(
        spot=100,
        strike=100,
        volatility=0.25,
        rate=0.05,
        maturity=0.5,  # 6 months
        option_type='call',
        style='european'
    )
    
    portfolio = Portfolio(positions=[
        Position(instrument_type='option', quantity=10, params=call_params)
    ])
    
    return portfolio, call_params


def main():
    print("\n" + "=" * 70)
    print("HEDGING SIMULATOR TEST")
    print("=" * 70)
    
    # Create sample portfolio
    portfolio, base_params = create_sample_portfolio()
    
    print("\nPortfolio: Long 10 ATM Call Options")
    print(f"  Spot: ${base_params.spot}")
    print(f"  Strike: ${base_params.strike}")
    print(f"  Volatility: {base_params.volatility*100}%")
    print(f"  Maturity: {base_params.maturity} years")
    
    # Initialize simulator
    simulator = HedgingSimulator()
    
    # Calculate initial Greeks
    initial_greeks = simulator.calculate_portfolio_greeks(portfolio)
    print(f"\nInitial Portfolio Greeks:")
    print(f"  Delta: {initial_greeks['delta']:.4f}")
    print(f"  Gamma: {initial_greeks['gamma']:.4f}")
    print(f"  Vega:  {initial_greeks['vega']:.4f}")
    
    # Create hedge option for gamma hedging (OTM put)
    hedge_option = OptionParams(
        spot=100,
        strike=95,
        volatility=0.25,
        rate=0.05,
        maturity=0.5,
        option_type='put',
        style='european'
    )
    
    # Compare strategies
    print("\n")
    results = simulator.compare_strategies(
        portfolio=portfolio,
        n_scenarios=1000,
        hedge_option_params=hedge_option
    )
    
    # Additional analysis
    print("\nPnL Distribution (Delta Hedge):")
    percentiles = results['delta_hedge']['pnl_percentiles']
    print(f"  5th percentile:  ${percentiles['5th']:.2f}")
    print(f"  25th percentile: ${percentiles['25th']:.2f}")
    print(f"  Median:          ${percentiles['50th']:.2f}")
    print(f"  75th percentile: ${percentiles['75th']:.2f}")
    print(f"  95th percentile: ${percentiles['95th']:.2f}")
    
    print("\n" + "=" * 70)
    if results['target_met']:
        print("SUCCESS: Hedging achieves target variance reduction (≥15%)")
    else:
        print("FAILED: Hedging does not meet target variance reduction")
    print("=" * 70)


if __name__ == '__main__':
    main()
