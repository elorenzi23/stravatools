import pandas as pd
import plotly.graph_objects as go


def plot_speed_vs_time(
    df: pd.DataFrame, activity_name: str = "Ride"
) -> go.Figure:
    """
    Create speed vs time plot
    """
    fig = go.Figure()

    # Add speed trace
    fig.add_trace(
        go.Scatter(
            x=df['time_minutes'],
            y=df['speed_kmh'],
            mode='lines',
            name='Speed',
            line=dict(color='#1f77b4', width=2),
            hovertemplate='<b>Time:</b> %{x:.1f} min<br>'
            + '<b>Speed:</b> %{y:.1f} km/h<br>'
            + '<extra></extra>',
        )
    )

    # Add average speed line
    if not df['speed_kmh'].empty:
        avg_speed = df['speed_kmh'].mean()
        fig.add_hline(
            y=avg_speed,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Avg: {avg_speed:.1f} km/h",
            annotation_position="top right",
        )

    fig.update_layout(
        title=f'{activity_name} - Speed Profile',
        xaxis_title='Time (minutes)',
        yaxis_title='Speed (km/h)',
        template='plotly_white',
        hovermode='x unified',
        height=400,
    )

    return fig
