import streamlit as st
import requests

from app.strava.strava_client import StravaClient
from app.strava.authenticator import Authenticator
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any
import json


def fetch_strava_data():
    auth = Authenticator()
    headers = auth.get_auth_header()

    response = requests.get(
        "https://www.strava.com/api/v3/athlete", headers=headers
    )
    athlete_data = response.json()

    access_token = auth.token_data["access_token"]
    client = StravaClient(access_token=access_token)

    page = 1
    per_page = 30
    ride = None
        
    while True:
        print(f"Checking page {page}...")
        activities = client.get_activities(page=page, per_page=per_page)
       
        if not activities:
            print("No more activities or API error occurred")
            break
            
        # Check each activity for type "Ride"
        for activity in activities:
            print(f"Activity: {activity['name']} - Type: {activity['type']}")
                
            if activity['type'] == 'Ride':
               print(f"\nFound first ride!")
               ride = activity
               break
        if ride:
            break
            
        # If no rides found on this page, check next page
        if len(activities) < per_page:
            # We've reached the end of activities
            print("No ride activities found in your account")
            break
            
        page += 1

    if ride:
        activity_id = ride["id"]

        gpx_data = client.get_activity_streams(
            activity_id=activity_id, access_token=access_token
        )
    else:
        gpx_data = {}

    return athlete_data, ride, gpx_data


def process_streams_for_plotting(streams_json: Dict[str, Any]) -> pd.DataFrame:
    """
    Process Strava streams JSON into a DataFrame ready for plotting
    """
    if not streams_json:
        return pd.DataFrame()
    
    data = {}
    
    # Extract time stream
    if 'time' in streams_json and 'data' in streams_json['time']:
        data['time_seconds'] = streams_json['time']['data']
        data['time_minutes'] = [t / 60 for t in streams_json['time']['data']]
        data['time_hours'] = [t / 3600 for t in streams_json['time']['data']]
    
    # Extract and convert speed stream
    if 'velocity_smooth' in streams_json and 'data' in streams_json['velocity_smooth']:
        velocity_data = streams_json['velocity_smooth']['data']
        data['speed_ms'] = velocity_data
        data['speed_kmh'] = [v * 3.6 if v is not None else 0 for v in velocity_data]
        data['speed_mph'] = [v * 2.237 if v is not None else 0 for v in velocity_data]
    
    # Extract other useful streams
    if 'distance' in streams_json and 'data' in streams_json['distance']:
        distance_data = streams_json['distance']['data']
        data['distance_km'] = [d / 1000 if d is not None else 0 for d in distance_data]
    
    if 'altitude' in streams_json and 'data' in streams_json['altitude']:
        data['altitude'] = streams_json['altitude']['data']
    
    if 'heartrate' in streams_json and 'data' in streams_json['heartrate']:
        data['heartrate'] = streams_json['heartrate']['data']
    
    if 'cadence' in streams_json and 'data' in streams_json['cadence']:
        data['cadence'] = streams_json['cadence']['data']
    
    if 'watts' in streams_json and 'data' in streams_json['watts']:
        data['watts'] = streams_json['watts']['data']
    
    return pd.DataFrame(data)

def plot_speed_vs_time(df: pd.DataFrame, activity_name: str = "Ride") -> go.Figure:
    """
    Create speed vs time plot
    """
    fig = go.Figure()
    
    # Add speed trace
    fig.add_trace(go.Scatter(
        x=df['time_minutes'],
        y=df['speed_kmh'],
        mode='lines',
        name='Speed',
        line=dict(color='#1f77b4', width=2),
        hovertemplate='<b>Time:</b> %{x:.1f} min<br>' +
                      '<b>Speed:</b> %{y:.1f} km/h<br>' +
                      '<extra></extra>'
    ))
    
    # Add average speed line
    if not df['speed_kmh'].empty:
        avg_speed = df['speed_kmh'].mean()
        fig.add_hline(
            y=avg_speed, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Avg: {avg_speed:.1f} km/h",
            annotation_position="top right"
        )
    
    fig.update_layout(
        title=f'{activity_name} - Speed Profile',
        xaxis_title='Time (minutes)',
        yaxis_title='Speed (km/h)',
        template='plotly_white',
        hovermode='x unified',
        height=400
    )
    
    return fig



# Streamlit UI
st.set_page_config(page_title="Strava Data Viewer")

st.title("Strava Data Viewer")

if st.button("Fetch Strava Data"):
    athlete_data, activities, gpx_data = fetch_strava_data()

    st.subheader("Athlete Profile")
    st.json(athlete_data)

    st.subheader("Activities (First Page)")
    st.json(activities)

    st.subheader("speed plot of latest activity")
    
    df = process_streams_for_plotting(gpx_data)
    
    st.markdown("### Speed vs Time")
    if 'speed_kmh' in df.columns and 'time_minutes' in df.columns:
        speed_fig = plot_speed_vs_time(df, "ride")
        st.plotly_chart(speed_fig, use_container_width=True)
    else:
        st.warning("Speed or time data not available")



else:
    st.write("Click the button to fetch Strava data.")

