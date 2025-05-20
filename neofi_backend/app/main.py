from fastapi import FastAPI
from app.api.routes import auth, events

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])

@app.get("/")
def read_root():
    return {"message": "NeoFi Backend API is running"}
