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

    def get_activity_streams(self, activity_id: int, access_token: str):
        gpx_url = f"{self.BASE_URL}/activities/{activity_id}/streams"
        gpx_response = requests.get(gpx_url, headers=self.headers)
        if gpx_response.status_code == 200:
            return gpx_response.content
        else:
            print(f"Failed to download GPX: {gpx_response.status_code}")
