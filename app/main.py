import threading
from contextlib import asynccontextmanager

import requests
from fastapi import FastAPI

from app.strava.strava_client import StravaClient
from app.strava.authenticator import Authenticator


def run_startup_task():
    auth = Authenticator()
    headers = auth.get_auth_header()
    response = requests.get(
        "https://www.strava.com/api/v3/athlete", headers=headers
    )
    print(response.json())

    access_token = auth.token_data["access_token"]
    client = StravaClient(access_token=access_token)

    activities = client.get_activities(page=1, per_page=1)
    print(activities)
    activity_id = activities[0]["id"]

    gpx_data = client.get_activity_streams(
        activity_id=activity_id, access_token=access_token
    )

    print(gpx_data)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    thread = threading.Thread(target=run_startup_task, daemon=True)
    thread.start()

    yield  # This is where the app runs

    # Optional: shutdown logic here


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
