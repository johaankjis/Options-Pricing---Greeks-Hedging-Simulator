"""
Test script to validate the pricing engine
Run this to ensure accuracy meets the ≤ 0.5% target
"""

import sys
sys.path.append('..')

from validation import PricingValidator

if __name__ == '__main__':
    print("\n🚀 Running Options Pricing Engine Validation\n")
    
    validator = PricingValidator()
    
    # Validate pricing accuracy
    results = validator.validate_pricing()
    
    # Validate Greeks
    validator.validate_greeks()
    
    # Summary
    print("\n" + "=" * 70)
    if results['target_met']:
        print("✓ SUCCESS: Pricing engine meets accuracy target (≤ 0.5% error)")
    else:
        print("✗ FAILED: Pricing engine does not meet accuracy target")
        print(f"  Maximum error: {results['max_error']:.4f}% (target: ≤ 0.5%)")
    print("=" * 70)
