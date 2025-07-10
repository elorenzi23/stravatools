import requests


class StravaClient:

    BASE_URL = "https://www.strava.com/api/v3"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def get_activities(self, per_page: int, page: int):
        url = f"{self.BASE_URL}/athlete/activities"
        response = requests.get(
            url,
            headers=self.headers,
            params={
                "per_page": per_page,
                "page": page,
            },
        )

        activities = response.json()

        if activities:
            return activities
        else:
            print("No activities found.")

    def get_activity_streams(
        self,
        activity_id: int,
        access_token: str = None,
        resolution: str = "high",
        stream_types: list = None,
    ):
        """
        Get activity streams from Strava API

        Args:
            activity_id (int): The ID of the activity
            access_token (str, optional): Override access token if needed
            resolution (str): "low", "medium", "high", or "all"
            stream_types (list, optional): List of stream types to request

        Returns:
            dict: Stream data organized by stream type, or None if error
        """

        # Default stream types if none specified
        if stream_types is None:
            stream_types = [
                "time",
                "velocity_smooth",
                "distance",
                "altitude",
                "heartrate",
                "cadence",
                "watts",
                "latlng",
            ]

        # Use provided access token or fall back to instance token
        if access_token:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
        else:
            headers = self.headers

        params = {
            "keys": ",".join(stream_types),
            "key_by_type": "true",
            "resolution": resolution,
        }

        streams_url = f"{self.BASE_URL}/activities/{activity_id}/streams"

        try:
            streams_response = requests.get(
                streams_url, headers=headers, params=params
            )

            if streams_response.status_code == 200:
                streams_data = streams_response.json()
                print(
                    f"Successfully retrieved {len(streams_data)} stream types for activity {activity_id}"
                )
                return streams_data
            elif streams_response.status_code == 401:
                print("Authentication failed: Invalid or expired access token")
                return None
            elif streams_response.status_code == 403:
                print(
                    "Access forbidden: You may not have permission to view this activity"
                )
                return None
            elif streams_response.status_code == 404:
                print(f"Activity {activity_id} not found")
                return None
            elif streams_response.status_code == 429:
                print(
                    "Rate limit exceeded. Please wait before making more requests"
                )
                return None
            else:
                print(
                    f"Failed to retrieve streams: {streams_response.status_code} - {streams_response.text}"
                )
                return None

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
