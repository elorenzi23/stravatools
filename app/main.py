from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.strava.authenticator import Authenticator
import threading
import requests

def run_startup_task():
    auth = Authenticator()
    headers = auth.get_auth_header()
    response = requests.get("https://www.strava.com/api/v3/athlete", headers=headers)
    print(response.json())

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
