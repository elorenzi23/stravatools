
import requests
import streamlit as st

from app.data.processors import process_streams_for_plotting
from app.strava.authenticator import Authenticator
from app.strava.strava_client import StravaClient
from app.visualization.plots import plot_speed_vs_time


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
                print("\nFound first ride!")
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
