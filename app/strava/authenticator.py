import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()


class Authenticator:
    def __init__(self, token_file="strava_tokens.json"):
        self.client_id = os.getenv("STRAVA_CLIENT_ID")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")
        self.token_file = token_file
        self.token_url = "https://www.strava.com/api/v3/oauth/token"

        self.token_data = self._load_tokens()

        if self._token_expired():
            self._refresh_token()

    def _load_tokens(self):
        try:
            with open(self.token_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Token file not found, initializing from .env...")
            return {
                "access_token": "",
                "refresh_token": os.getenv("STRAVA_REFRESH_TOKEN"),
                "expires_at": 0,
            }

    def _token_expired(self):
        return time.time() > self.token_data.get("expires_at", 0)

    def _refresh_token(self):
        print("Refreshing Strava access token...")
        response = requests.post(
            self.token_url,
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': self.token_data["refresh_token"],
            },
        )
        response.raise_for_status()
        new_tokens = response.json()
        self.token_data.update(new_tokens)
        if "scope" in new_tokens:
            self.token_data["scope"] = new_tokens["scope"]
        self._save_tokens()

    def _save_tokens(self):
        with open(self.token_file, "w") as f:
            json.dump(self.token_data, f)

    def get_auth_header(self):
        if self._token_expired():
            self._refresh_token()
        print(self.token_data)
        return {"Authorization": f"Bearer {self.token_data['access_token']}"}
