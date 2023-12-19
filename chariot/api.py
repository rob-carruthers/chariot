"""FastAPI endpoints for Chariot"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .interface import ChariotJourneyPipeline

app = FastAPI()
app.state.pipeline = ChariotJourneyPipeline()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
    # Add other origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/ping")
def ping():
    """
    Return a ping if the api is able to respond.
    """
    return {"response": "ping"}

@app.get("/")
async def chariot_request(query):
    """
    Process a natural language TFL journey request.
    """
    result = app.state.pipeline.request_from_natural_language(query)
    return {"duration": result.duration,
            "legs": result.legs,
            "departure_stop": result.departure_stop,
            "arrival_stop": result.arrival_stop
    }
