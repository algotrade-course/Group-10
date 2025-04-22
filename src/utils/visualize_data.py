import pandas as pd
import numpy as np
import plotly.graph_objects as go


def plotChart(data):
    fig = go.Figure()

    # --- Price Chart with EMA_50 ---
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['close'],
        mode='lines',
        name='Close Price',
        marker=dict(color='blue', size=6),
        hovertemplate='Timestamp: %{x}<br>Close Price: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['EMA_50'],
        mode='lines',
        name='EMA 50',
        marker=dict(color='orange', size=6),
        hovertemplate='Timestamp: %{x}<br>EMA 50: %{y}<extra></extra>'
    ))

    # --- MACD Indicator ---
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MACD'],
        mode='lines',
        name='MACD Line',
        marker=dict(color='blue', size=6),
        hovertemplate='Timestamp: %{x}<br>MACD: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['MACD_signal'],
        mode='lines',
        name='Signal Line',
        marker=dict(color='red', size=6),
        hovertemplate='Timestamp: %{x}<br>Signal Line: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Histogram'],
        name='Histogram',
        marker_color=np.where(data['Histogram'] >= 0, 'green', 'brown'),
        hovertemplate='Timestamp: %{x}<br>Histogram: %{y}<extra></extra>'
    ))

    # Update layout for better visualization
    fig.update_layout(
        title='Interactive Chart: Close Price, EMA 50, and MACD',
        xaxis=dict(
            title='Timestamp',
            tickmode='auto'
        ),
        yaxis_title='Value',
        legend_title='Indicators',
        template='plotly_white',
        hovermode='x unified',
        width=1200,
        height=800
    )

    # Show the interactive plot
    fig.show()