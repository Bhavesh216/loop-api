# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# A class to define what kind of data we expect in /ingest
class IngestData(BaseModel):
    id: int
    message: str

# This will temporarily store the data we receive
stored_data: List[IngestData] = []

@app.get("/")
def root():
    return {"message": "Service is up and running!"}

@app.post("/ingest")
def ingest(data: IngestData):
    stored_data.append(data)
    return {"message": "Data received successfully", "data": data}
