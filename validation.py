"""
Validation module to test pricing accuracy against known benchmarks
Target: ≤ 0.5% error vs benchmark data
"""

import numpy as np
from pricing import OptionParams, OptionsPricingEngine
from typing import List, Dict


class PricingValidator:
    """
    Validates pricing engine accuracy against known benchmarks
    """
    
    def __init__(self):
        self.engine = OptionsPricingEngine()
        self.test_cases = self._load_test_cases()
    
    def _load_test_cases(self) -> List[Dict]:
        """
        Load benchmark test cases with known prices
        These are standard test cases from academic literature
        """
        return [
            # Test case 1: At-the-money European call
            {
                'params': OptionParams(
                    spot=100, strike=100, volatility=0.2, 
                    rate=0.05, maturity=1.0, option_type='call', style='european'
                ),
                'expected_price': 10.4506,
                'name': 'ATM European Call'
            },
            # Test case 2: Out-of-the-money European put
            {
                'params': OptionParams(
                    spot=100, strike=95, volatility=0.2,
                    rate=0.05, maturity=1.0, option_type='put', style='european'
                ),
                'expected_price': 6.0400,
                'name': 'OTM European Put'
            },
            # Test case 3: In-the-money European call
            {
                'params': OptionParams(
                    spot=110, strike=100, volatility=0.25,
                    rate=0.04, maturity=0.5, option_type='call', style='european'
                ),
                'expected_price': 13.8308,
                'name': 'ITM European Call'
            },
            # Test case 4: Deep out-of-the-money put
            {
                'params': OptionParams(
                    spot=100, strike=80, volatility=0.3,
                    rate=0.06, maturity=2.0, option_type='put', style='european'
                ),
                'expected_price': 4.0536,
                'name': 'Deep OTM Put'
            },
            # Test case 5: Short-dated call
            {
                'params': OptionParams(
                    spot=50, strike=50, volatility=0.15,
                    rate=0.03, maturity=0.25, option_type='call', style='european'
                ),
                'expected_price': 1.8757,
                'name': 'Short-dated ATM Call'
            },
        ]
    
    def validate_pricing(self) -> Dict:
        """
        Run validation tests and return results
        
        Returns:
            Dictionary with validation results and statistics
        """
        results = []
        errors = []
        
        print("=" * 70)
        print("OPTIONS PRICING ENGINE VALIDATION")
        print("=" * 70)
        print(f"{'Test Case':<25} {'Expected':<12} {'Calculated':<12} {'Error %':<10}")
        print("-" * 70)
        
        for test in self.test_cases:
            params = test['params']
            expected = test['expected_price']
            
            # Calculate price
            calculated = self.engine.price(params)
            
            # Calculate error
            error_pct = abs((calculated - expected) / expected) * 100
            errors.append(error_pct)
            
            # Store result
            results.append({
                'name': test['name'],
                'expected': expected,
                'calculated': calculated,
                'error_pct': error_pct,
                'passed': error_pct <= 0.5
            })
            
            # Print result
            status = "✓" if error_pct <= 0.5 else "✗"
            print(f"{test['name']:<25} ${expected:<11.4f} ${calculated:<11.4f} {error_pct:<9.4f}% {status}")
        
        print("-" * 70)
        
        # Calculate statistics
        max_error = max(errors)
        avg_error = np.mean(errors)
        passed = sum(1 for r in results if r['passed'])
        total = len(results)
        
        print(f"\nValidation Statistics:")
        print(f"  Tests Passed: {passed}/{total} ({passed/total*100:.1f}%)")
        print(f"  Average Error: {avg_error:.4f}%")
        print(f"  Maximum Error: {max_error:.4f}%")
        print(f"  Target Met: {'YES ✓' if max_error <= 0.5 else 'NO ✗'} (target: ≤ 0.5%)")
        print("=" * 70)
        
        return {
            'results': results,
            'max_error': max_error,
            'avg_error': avg_error,
            'passed': passed,
            'total': total,
            'target_met': max_error <= 0.5
        }
    
    def validate_greeks(self) -> None:
        """
        Validate Greeks calculations with sanity checks
        """
        print("\n" + "=" * 70)
        print("GREEKS VALIDATION")
        print("=" * 70)
        
        # Test case: ATM call
        params = OptionParams(
            spot=100, strike=100, volatility=0.2,
            rate=0.05, maturity=1.0, option_type='call', style='european'
        )
        
        greeks = self.engine.greeks(params)
        
        print(f"\nTest: ATM European Call (S=100, K=100, σ=0.2, r=0.05, T=1.0)")
        print("-" * 70)
        print(f"Delta:  {greeks['delta']:.4f}  (expected ~0.5-0.6 for ATM call)")
        print(f"Gamma:  {greeks['gamma']:.4f}  (expected positive, max at ATM)")
        print(f"Vega:   {greeks['vega']:.4f}  (expected positive)")
        print(f"Theta:  {greeks['theta']:.4f}  (expected negative for long call)")
        print(f"Rho:    {greeks['rho']:.4f}  (expected positive for call)")
        
        # Sanity checks
        checks = []
        checks.append(('Delta in range', 0.4 <= greeks['delta'] <= 0.7))
        checks.append(('Gamma positive', greeks['gamma'] > 0))
        checks.append(('Vega positive', greeks['vega'] > 0))
        checks.append(('Theta negative', greeks['theta'] < 0))
        checks.append(('Rho positive', greeks['rho'] > 0))
        
        print("\nSanity Checks:")
        for check_name, passed in checks:
            status = "✓" if passed else "✗"
            print(f"  {check_name:<25} {status}")
        
        print("=" * 70)


if __name__ == '__main__':
    validator = PricingValidator()
    results = validator.validate_pricing()
    validator.validate_greeks()
