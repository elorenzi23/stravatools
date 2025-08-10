from typing import Any, Dict

import pandas as pd


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
    if (
        'velocity_smooth' in streams_json
        and 'data' in streams_json['velocity_smooth']
    ):
        velocity_data = streams_json['velocity_smooth']['data']
        data['speed_ms'] = velocity_data
        data['speed_kmh'] = [
            v * 3.6 if v is not None else 0 for v in velocity_data
        ]
        data['speed_mph'] = [
            v * 2.237 if v is not None else 0 for v in velocity_data
        ]

    # Extract other useful streams
    if 'distance' in streams_json and 'data' in streams_json['distance']:
        distance_data = streams_json['distance']['data']
        data['distance_km'] = [
            d / 1000 if d is not None else 0 for d in distance_data
        ]

    if 'altitude' in streams_json and 'data' in streams_json['altitude']:
        data['altitude'] = streams_json['altitude']['data']

    if 'heartrate' in streams_json and 'data' in streams_json['heartrate']:
        data['heartrate'] = streams_json['heartrate']['data']

    if 'cadence' in streams_json and 'data' in streams_json['cadence']:
        data['cadence'] = streams_json['cadence']['data']

    if 'watts' in streams_json and 'data' in streams_json['watts']:
        data['watts'] = streams_json['watts']['data']

    return pd.DataFrame(data)
