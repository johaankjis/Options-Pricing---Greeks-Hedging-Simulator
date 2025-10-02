"""
Launch the Plotly Dash dashboard
"""

import sys
sys.path.append('..')

from dashboard import app

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("OPTIONS PRICING & HEDGING DASHBOARD")
    print("=" * 70)
    print("\nFeatures:")
    print("  - Real-time options pricing (Black-Scholes & Binomial)")
    print("  - Greeks computation and visualization")
    print("  - Interactive payoff diagrams")
    print("  - Delta surface 3D visualization")
    print("  - Hedging simulation with PnL distribution")
    print("\n" + "=" * 70)
    print("\nStarting dashboard at: http://127.0.0.1:8050")
    print("Press Ctrl+C to stop")
    print("=" * 70 + "\n")
    
    app.run_server(debug=False, host='0.0.0.0', port=8050)
