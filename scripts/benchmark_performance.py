"""
Benchmark script to measure performance improvements
Compares baseline vs optimized implementations
Target: 40% faster, 10,000 paths in < 2s
"""

import sys
sys.path.append('..')

import time
import numpy as np
from pricing import OptionParams, OptionsPricingEngine
from pricing_optimized import OptimizedPricingEngine


def benchmark_single_pricing(n_iterations=1000):
    """Benchmark single option pricing"""
    print("\n" + "=" * 70)
    print("BENCHMARK: Single Option Pricing")
    print("=" * 70)
    
    params = OptionParams(
        spot=100, strike=100, volatility=0.25,
        rate=0.05, maturity=1.0, option_type='call', style='european'
    )
    
    # Baseline
    baseline_engine = OptionsPricingEngine()
    start = time.time()
    for _ in range(n_iterations):
        price = baseline_engine.price(params)
    baseline_time = time.time() - start
    
    # Optimized
    optimized_engine = OptimizedPricingEngine()
    start = time.time()
    for _ in range(n_iterations):
        price = optimized_engine.price(params)
    optimized_time = time.time() - start
    
    speedup = (baseline_time - optimized_time) / baseline_time * 100
    
    print(f"Iterations: {n_iterations}")
    print(f"Baseline time:   {baseline_time:.4f}s")
    print(f"Optimized time:  {optimized_time:.4f}s")
    print(f"Speedup:         {speedup:.1f}%")
    print("=" * 70)
    
    return speedup


def benchmark_greeks_calculation(n_iterations=1000):
    """Benchmark Greeks calculation"""
    print("\n" + "=" * 70)
    print("BENCHMARK: Greeks Calculation")
    print("=" * 70)
    
    params = OptionParams(
        spot=100, strike=100, volatility=0.25,
        rate=0.05, maturity=1.0, option_type='call', style='european'
    )
    
    # Baseline
    baseline_engine = OptionsPricingEngine()
    start = time.time()
    for _ in range(n_iterations):
        greeks = baseline_engine.greeks(params)
    baseline_time = time.time() - start
    
    # Optimized
    optimized_engine = OptimizedPricingEngine()
    start = time.time()
    for _ in range(n_iterations):
        greeks = optimized_engine.greeks(params)
    optimized_time = time.time() - start
    
    speedup = (baseline_time - optimized_time) / baseline_time * 100
    
    print(f"Iterations: {n_iterations}")
    print(f"Baseline time:   {baseline_time:.4f}s")
    print(f"Optimized time:  {optimized_time:.4f}s")
    print(f"Speedup:         {speedup:.1f}%")
    print("=" * 70)
    
    return speedup


def benchmark_vectorized_pricing(n_prices=10000):
    """Benchmark vectorized pricing for multiple spot prices"""
    print("\n" + "=" * 70)
    print("BENCHMARK: Vectorized Pricing")
    print("=" * 70)
    
    params = OptionParams(
        spot=100, strike=100, volatility=0.25,
        rate=0.05, maturity=1.0, option_type='call', style='european'
    )
    
    spot_array = np.linspace(80, 120, n_prices)
    
    # Baseline (loop)
    baseline_engine = OptionsPricingEngine()
    start = time.time()
    prices_baseline = []
    for spot in spot_array:
        params_temp = OptionParams(
            spot=spot, strike=params.strike, volatility=params.volatility,
            rate=params.rate, maturity=params.maturity, 
            option_type=params.option_type, style=params.style
        )
        prices_baseline.append(baseline_engine.price(params_temp))
    baseline_time = time.time() - start
    
    # Optimized (vectorized)
    optimized_engine = OptimizedPricingEngine()
    start = time.time()
    prices_optimized = optimized_engine.price_multiple(spot_array, params)
    optimized_time = time.time() - start
    
    speedup = (baseline_time - optimized_time) / baseline_time * 100
    
    print(f"Number of prices: {n_prices}")
    print(f"Baseline time:    {baseline_time:.4f}s")
    print(f"Optimized time:   {optimized_time:.4f}s")
    print(f"Speedup:          {speedup:.1f}%")
    print("=" * 70)
    
    return speedup


def benchmark_monte_carlo(n_paths=10000, n_steps=252):
    """Benchmark Monte Carlo simulation"""
    print("\n" + "=" * 70)
    print("BENCHMARK: Monte Carlo Simulation")
    print("=" * 70)
    print(f"Target: {n_paths} paths in < 2s")
    print("-" * 70)
    
    optimized_engine = OptimizedPricingEngine()
    
    # Warm-up JIT compilation
    _ = optimized_engine.simulate_paths(100, 0.25, 0.05, 1.0, 100, 10)
    
    # Actual benchmark
    start = time.time()
    paths = optimized_engine.simulate_paths(100, 0.25, 0.05, 1.0, n_paths, n_steps)
    elapsed = time.time() - start
    
    target_met = elapsed < 2.0
    
    print(f"Paths simulated:  {n_paths}")
    print(f"Steps per path:   {n_steps}")
    print(f"Time elapsed:     {elapsed:.4f}s")
    print(f"Paths per second: {n_paths/elapsed:.0f}")
    print(f"Target met:       {'YES' if target_met else 'NO'} (< 2s)")
    print("=" * 70)
    
    return elapsed, target_met


def main():
    print("\n" + "=" * 70)
    print("PERFORMANCE OPTIMIZATION BENCHMARK")
    print("=" * 70)
    print("\nTesting optimizations:")
    print("  - Numba JIT compilation")
    print("  - Vectorized operations")
    print("  - Parallel execution")
    print("  - Fast approximations")
    
    # Run benchmarks
    speedup_pricing = benchmark_single_pricing(n_iterations=1000)
    speedup_greeks = benchmark_greeks_calculation(n_iterations=1000)
    speedup_vectorized = benchmark_vectorized_pricing(n_prices=10000)
    mc_time, mc_target_met = benchmark_monte_carlo(n_paths=10000, n_steps=252)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    avg_speedup = (speedup_pricing + speedup_greeks + speedup_vectorized) / 3
    
    print(f"\nAverage Speedup: {avg_speedup:.1f}%")
    print(f"Target: 40% faster")
    print(f"Status: {'ACHIEVED' if avg_speedup >= 40 else 'NOT MET'}")
    
    print(f"\nMonte Carlo Performance:")
    print(f"  10,000 paths in {mc_time:.4f}s")
    print(f"  Target: < 2s")
    print(f"  Status: {'ACHIEVED' if mc_target_met else 'NOT MET'}")
    
    print("\n" + "=" * 70)
    
    overall_success = avg_speedup >= 40 and mc_target_met
    
    if overall_success:
        print("SUCCESS: All performance targets met!")
    else:
        print("PARTIAL: Some targets not met, but significant improvements achieved")
    
    print("=" * 70)


if __name__ == '__main__':
    main()
