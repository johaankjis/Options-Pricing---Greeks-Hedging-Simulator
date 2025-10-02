"""
Interactive Plotly Dash Dashboard
Visualizes options pricing, Greeks, and hedging effectiveness
Target: < 1s latency for updates
"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from pricing import OptionParams, OptionsPricingEngine
from hedging import Portfolio, Position, HedgingSimulator, MarketScenario


# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Options Pricing & Hedging Simulator"

# Initialize engines
pricing_engine = OptionsPricingEngine()
hedging_simulator = HedgingSimulator()


# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Options Pricing & Hedging Simulator", 
                style={'margin': '0', 'color': '#e5e5e5', 'fontSize': '28px', 'fontWeight': '600'}),
        html.P("Real-time options pricing, Greeks analysis, and hedging simulation",
               style={'margin': '8px 0 0 0', 'color': '#a3a3a3', 'fontSize': '14px'})
    ], style={
        'padding': '24px 32px',
        'backgroundColor': '#0a0a0a',
        'borderBottom': '1px solid #262626'
    }),
    
    # Main content
    html.Div([
        # Left panel - Input controls
        html.Div([
            html.Div([
                html.H3("Option Parameters", style={'color': '#e5e5e5', 'fontSize': '16px', 'marginBottom': '20px'}),
                
                # Spot Price
                html.Label("Spot Price ($)", style={'color': '#a3a3a3', 'fontSize': '13px', 'marginBottom': '6px'}),
                dcc.Input(id='spot-input', type='number', value=100, 
                         style={'width': '100%', 'padding': '8px', 'marginBottom': '16px',
                                'backgroundColor': '#171717', 'border': '1px solid #262626',
                                'color': '#e5e5e5', 'borderRadius': '6px'}),
                
                # Strike Price
                html.Label("Strike Price ($)", style={'color': '#a3a3a3', 'fontSize': '13px', 'marginBottom': '6px'}),
                dcc.Input(id='strike-input', type='number', value=100,
                         style={'width': '100%', 'padding': '8px', 'marginBottom': '16px',
                                'backgroundColor': '#171717', 'border': '1px solid #262626',
                                'color': '#e5e5e5', 'borderRadius': '6px'}),
                
                # Volatility
                html.Label("Volatility (%)", style={'color': '#a3a3a3', 'fontSize': '13px', 'marginBottom': '6px'}),
                dcc.Input(id='volatility-input', type='number', value=25,
                         style={'width': '100%', 'padding': '8px', 'marginBottom': '16px',
                                'backgroundColor': '#171717', 'border': '1px solid #262626',
                                'color': '#e5e5e5', 'borderRadius': '6px'}),
                
                # Interest Rate
                html.Label("Interest Rate (%)", style={'color': '#a3a3a3', 'fontSize': '13px', 'marginBottom': '6px'}),
                dcc.Input(id='rate-input', type='number', value=5,
                         style={'width': '100%', 'padding': '8px', 'marginBottom': '16px',
                                'backgroundColor': '#171717', 'border': '1px solid #262626',
                                'color': '#e5e5e5', 'borderRadius': '6px'}),
                
                # Maturity
                html.Label("Time to Maturity (years)", style={'color': '#a3a3a3', 'fontSize': '13px', 'marginBottom': '6px'}),
                dcc.Input(id='maturity-input', type='number', value=1.0,
                         style={'width': '100%', 'padding': '8px', 'marginBottom': '16px',
                                'backgroundColor': '#171717', 'border': '1px solid #262626',
                                'color': '#e5e5e5', 'borderRadius': '6px'}),
                
                # Option Type
                html.Label("Option Type", style={'color': '#a3a3a3', 'fontSize': '13px', 'marginBottom': '6px'}),
                dcc.Dropdown(
                    id='option-type-dropdown',
                    options=[
                        {'label': 'Call', 'value': 'call'},
                        {'label': 'Put', 'value': 'put'}
                    ],
                    value='call',
                    style={'marginBottom': '16px', 'backgroundColor': '#171717',
                           'border': '1px solid #262626', 'color': '#e5e5e5'}
                ),
                
                # Option Style
                html.Label("Option Style", style={'color': '#a3a3a3', 'fontSize': '13px', 'marginBottom': '6px'}),
                dcc.Dropdown(
                    id='option-style-dropdown',
                    options=[
                        {'label': 'European', 'value': 'european'},
                        {'label': 'American', 'value': 'american'}
                    ],
                    value='european',
                    style={'marginBottom': '24px', 'backgroundColor': '#171717',
                           'border': '1px solid #262626', 'color': '#e5e5e5'}
                ),
                
                # Calculate button
                html.Button('Calculate', id='calculate-button',
                           style={'width': '100%', 'padding': '12px', 'backgroundColor': '#3b82f6',
                                  'color': 'white', 'border': 'none', 'borderRadius': '6px',
                                  'cursor': 'pointer', 'fontSize': '14px', 'fontWeight': '500'})
            ], style={'padding': '24px', 'backgroundColor': '#0a0a0a', 'borderRadius': '8px',
                     'border': '1px solid #262626'})
        ], style={'width': '320px', 'marginRight': '24px'}),
        
        # Right panel - Results and visualizations
        html.Div([
            # Price and Greeks cards
            html.Div([
                # Option Price card
                html.Div([
                    html.Div("Option Price", style={'color': '#a3a3a3', 'fontSize': '13px', 'marginBottom': '8px'}),
                    html.Div(id='option-price-display', children="$0.00",
                            style={'color': '#3b82f6', 'fontSize': '32px', 'fontWeight': '600'})
                ], style={'flex': '1', 'padding': '20px', 'backgroundColor': '#0a0a0a',
                         'borderRadius': '8px', 'border': '1px solid #262626', 'marginRight': '16px'}),
                
                # Delta card
                html.Div([
                    html.Div("Delta", style={'color': '#a3a3a3', 'fontSize': '13px', 'marginBottom': '8px'}),
                    html.Div(id='delta-display', children="0.0000",
                            style={'color': '#10b981', 'fontSize': '32px', 'fontWeight': '600'})
                ], style={'flex': '1', 'padding': '20px', 'backgroundColor': '#0a0a0a',
                         'borderRadius': '8px', 'border': '1px solid #262626', 'marginRight': '16px'}),
                
                # Gamma card
                html.Div([
                    html.Div("Gamma", style={'color': '#a3a3a3', 'fontSize': '13px', 'marginBottom': '8px'}),
                    html.Div(id='gamma-display', children="0.0000",
                            style={'color': '#f59e0b', 'fontSize': '32px', 'fontWeight': '600'})
                ], style={'flex': '1', 'padding': '20px', 'backgroundColor': '#0a0a0a',
                         'borderRadius': '8px', 'border': '1px solid #262626'})
            ], style={'display': 'flex', 'marginBottom': '24px'}),
            
            # Additional Greeks
            html.Div([
                html.Div([
                    html.Span("Vega: ", style={'color': '#a3a3a3', 'fontSize': '13px'}),
                    html.Span(id='vega-display', children="0.0000", style={'color': '#e5e5e5', 'fontSize': '13px', 'fontWeight': '500'})
                ], style={'flex': '1', 'padding': '16px', 'backgroundColor': '#0a0a0a',
                         'borderRadius': '8px', 'border': '1px solid #262626', 'marginRight': '16px'}),
                
                html.Div([
                    html.Span("Theta: ", style={'color': '#a3a3a3', 'fontSize': '13px'}),
                    html.Span(id='theta-display', children="0.0000", style={'color': '#e5e5e5', 'fontSize': '13px', 'fontWeight': '500'})
                ], style={'flex': '1', 'padding': '16px', 'backgroundColor': '#0a0a0a',
                         'borderRadius': '8px', 'border': '1px solid #262626', 'marginRight': '16px'}),
                
                html.Div([
                    html.Span("Rho: ", style={'color': '#a3a3a3', 'fontSize': '13px'}),
                    html.Span(id='rho-display', children="0.0000", style={'color': '#e5e5e5', 'fontSize': '13px', 'fontWeight': '500'})
                ], style={'flex': '1', 'padding': '16px', 'backgroundColor': '#0a0a0a',
                         'borderRadius': '8px', 'border': '1px solid #262626'})
            ], style={'display': 'flex', 'marginBottom': '24px'}),
            
            # Charts
            html.Div([
                # Payoff diagram
                html.Div([
                    html.H3("Payoff Diagram", style={'color': '#e5e5e5', 'fontSize': '16px', 'marginBottom': '16px'}),
                    dcc.Graph(id='payoff-chart', config={'displayModeBar': False})
                ], style={'flex': '1', 'padding': '24px', 'backgroundColor': '#0a0a0a',
                         'borderRadius': '8px', 'border': '1px solid #262626', 'marginRight': '16px'}),
                
                # Greeks surface
                html.Div([
                    html.H3("Delta Surface", style={'color': '#e5e5e5', 'fontSize': '16px', 'marginBottom': '16px'}),
                    dcc.Graph(id='greeks-chart', config={'displayModeBar': False})
                ], style={'flex': '1', 'padding': '24px', 'backgroundColor': '#0a0a0a',
                         'borderRadius': '8px', 'border': '1px solid #262626'})
            ], style={'display': 'flex', 'marginBottom': '24px'}),
            
            # Hedging simulation
            html.Div([
                html.H3("Hedging Simulation", style={'color': '#e5e5e5', 'fontSize': '16px', 'marginBottom': '16px'}),
                html.Button('Run Hedging Simulation', id='hedge-button',
                           style={'padding': '10px 20px', 'backgroundColor': '#10b981',
                                  'color': 'white', 'border': 'none', 'borderRadius': '6px',
                                  'cursor': 'pointer', 'fontSize': '14px', 'fontWeight': '500',
                                  'marginBottom': '16px'}),
                dcc.Graph(id='hedging-chart', config={'displayModeBar': False}),
                html.Div(id='hedging-stats', style={'marginTop': '16px', 'color': '#a3a3a3', 'fontSize': '13px'})
            ], style={'padding': '24px', 'backgroundColor': '#0a0a0a',
                     'borderRadius': '8px', 'border': '1px solid #262626'})
        ], style={'flex': '1'})
    ], style={'display': 'flex', 'padding': '24px', 'backgroundColor': '#000000', 'minHeight': 'calc(100vh - 100px)'})
], style={'backgroundColor': '#000000', 'minHeight': '100vh', 'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'})


# Callbacks
@app.callback(
    [Output('option-price-display', 'children'),
     Output('delta-display', 'children'),
     Output('gamma-display', 'children'),
     Output('vega-display', 'children'),
     Output('theta-display', 'children'),
     Output('rho-display', 'children'),
     Output('payoff-chart', 'figure'),
     Output('greeks-chart', 'figure')],
    [Input('calculate-button', 'n_clicks')],
    [State('spot-input', 'value'),
     State('strike-input', 'value'),
     State('volatility-input', 'value'),
     State('rate-input', 'value'),
     State('maturity-input', 'value'),
     State('option-type-dropdown', 'value'),
     State('option-style-dropdown', 'value')]
)
def update_pricing(n_clicks, spot, strike, volatility, rate, maturity, option_type, option_style):
    """Update pricing and Greeks displays"""
    if not all([spot, strike, volatility, rate, maturity]):
        return ["$0.00"] * 6 + [go.Figure(), go.Figure()]
    
    # Create option parameters
    params = OptionParams(
        spot=spot,
        strike=strike,
        volatility=volatility / 100,
        rate=rate / 100,
        maturity=maturity,
        option_type=option_type,
        style=option_style
    )
    
    # Calculate price and Greeks
    price = pricing_engine.price(params)
    greeks = pricing_engine.greeks(params)
    
    # Create payoff diagram
    spot_range = np.linspace(spot * 0.7, spot * 1.3, 100)
    payoffs = []
    
    for s in spot_range:
        if option_type == 'call':
            payoff = max(s - strike, 0) - price
        else:
            payoff = max(strike - s, 0) - price
        payoffs.append(payoff)
    
    payoff_fig = go.Figure()
    payoff_fig.add_trace(go.Scatter(
        x=spot_range, y=payoffs,
        mode='lines',
        line=dict(color='#3b82f6', width=2),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)'
    ))
    payoff_fig.add_hline(y=0, line_dash="dash", line_color="#404040")
    payoff_fig.add_vline(x=strike, line_dash="dash", line_color="#f59e0b", annotation_text="Strike")
    payoff_fig.update_layout(
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#0a0a0a',
        font=dict(color='#a3a3a3'),
        xaxis=dict(title='Spot Price', gridcolor='#171717'),
        yaxis=dict(title='Profit/Loss', gridcolor='#171717'),
        margin=dict(l=40, r=20, t=20, b=40),
        height=300
    )
    
    # Create Delta surface
    spot_range_surface = np.linspace(spot * 0.8, spot * 1.2, 30)
    time_range = np.linspace(0.1, maturity, 30)
    delta_surface = np.zeros((len(time_range), len(spot_range_surface)))
    
    for i, t in enumerate(time_range):
        for j, s in enumerate(spot_range_surface):
            temp_params = OptionParams(
                spot=s, strike=strike, volatility=volatility/100,
                rate=rate/100, maturity=t, option_type=option_type, style='european'
            )
            temp_greeks = pricing_engine.greeks(temp_params)
            delta_surface[i, j] = temp_greeks['delta']
    
    greeks_fig = go.Figure(data=[go.Surface(
        x=spot_range_surface,
        y=time_range,
        z=delta_surface,
        colorscale='Blues',
        showscale=True
    )])
    greeks_fig.update_layout(
        scene=dict(
            xaxis=dict(title='Spot Price', backgroundcolor='#0a0a0a', gridcolor='#262626'),
            yaxis=dict(title='Time to Maturity', backgroundcolor='#0a0a0a', gridcolor='#262626'),
            zaxis=dict(title='Delta', backgroundcolor='#0a0a0a', gridcolor='#262626'),
            bgcolor='#0a0a0a'
        ),
        paper_bgcolor='#0a0a0a',
        font=dict(color='#a3a3a3'),
        margin=dict(l=0, r=0, t=0, b=0),
        height=300
    )
    
    return (
        f"${price:.2f}",
        f"{greeks['delta']:.4f}",
        f"{greeks['gamma']:.4f}",
        f"{greeks['vega']:.4f}",
        f"{greeks['theta']:.4f}",
        f"{greeks['rho']:.4f}",
        payoff_fig,
        greeks_fig
    )


@app.callback(
    [Output('hedging-chart', 'figure'),
     Output('hedging-stats', 'children')],
    [Input('hedge-button', 'n_clicks')],
    [State('spot-input', 'value'),
     State('strike-input', 'value'),
     State('volatility-input', 'value'),
     State('rate-input', 'value'),
     State('maturity-input', 'value'),
     State('option-type-dropdown', 'value')]
)
def run_hedging_simulation(n_clicks, spot, strike, volatility, rate, maturity, option_type):
    """Run hedging simulation and display results"""
    if not n_clicks or not all([spot, strike, volatility, rate, maturity]):
        return go.Figure(), ""
    
    # Create portfolio
    params = OptionParams(
        spot=spot, strike=strike, volatility=volatility/100,
        rate=rate/100, maturity=maturity, option_type=option_type
    )
    portfolio = Portfolio(positions=[
        Position(instrument_type='option', quantity=10, params=params)
    ])
    
    # Run simulations
    no_hedge = hedging_simulator.simulate_hedging_effectiveness(portfolio, 'none', n_scenarios=500)
    delta_hedge = hedging_simulator.simulate_hedging_effectiveness(portfolio, 'delta', n_scenarios=500)
    
    # Create histogram
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=no_hedge['pnl_values'],
        name='No Hedge',
        opacity=0.7,
        marker_color='#ef4444',
        nbinsx=30
    ))
    fig.add_trace(go.Histogram(
        x=delta_hedge['pnl_values'],
        name='Delta Hedge',
        opacity=0.7,
        marker_color='#10b981',
        nbinsx=30
    ))
    
    fig.update_layout(
        barmode='overlay',
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#0a0a0a',
        font=dict(color='#a3a3a3'),
        xaxis=dict(title='PnL', gridcolor='#171717'),
        yaxis=dict(title='Frequency', gridcolor='#171717'),
        legend=dict(bgcolor='#0a0a0a', bordercolor='#262626'),
        margin=dict(l=40, r=20, t=20, b=40),
        height=400
    )
    
    # Calculate statistics
    variance_reduction = (1 - delta_hedge['pnl_var'] / no_hedge['pnl_var']) * 100
    
    stats_text = html.Div([
        html.Div([
            html.Span("No Hedge PnL Std: ", style={'color': '#a3a3a3'}),
            html.Span(f"${no_hedge['pnl_std']:.2f}", style={'color': '#ef4444', 'fontWeight': '500'})
        ], style={'marginBottom': '8px'}),
        html.Div([
            html.Span("Delta Hedge PnL Std: ", style={'color': '#a3a3a3'}),
            html.Span(f"${delta_hedge['pnl_std']:.2f}", style={'color': '#10b981', 'fontWeight': '500'})
        ], style={'marginBottom': '8px'}),
        html.Div([
            html.Span("Variance Reduction: ", style={'color': '#a3a3a3'}),
            html.Span(f"{variance_reduction:.1f}%", style={'color': '#3b82f6', 'fontWeight': '500', 'fontSize': '16px'})
        ])
    ])
    
    return fig, stats_text


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("Starting Options Pricing & Hedging Dashboard")
    print("=" * 70)
    print("\nDashboard running at: http://127.0.0.1:8050")
    print("Press Ctrl+C to stop\n")
    
    app.run_server(debug=True, host='0.0.0.0', port=8050)
