from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
# Pydantic Model for POST body
class IngestData(BaseModel):
    id: int
    message: str

# Temporary in-memory storage (resets every restart)
stored_data: List[IngestData] = []


# Root endpoint (health check)

@app.get("/")
def root():
    return {"message": "Service is up and running!"}


# POST /ingest - Add data to store

@app.post("/ingest")
def ingest(data: IngestData):
    stored_data.append(data)
    return {
        "message": "Data received successfully",
        "data": data,
        "total_items": len(stored_data)
    }

# GET /data - Returns all data (optional query filter)
# Example: /data?query=hello
@app.get("/data")
def get_all_data(query: Optional[str] = Query(default=None, description="Filter messages containing this text")):
    if query:
        filtered = [item for item in stored_data if query.lower() in item.message.lower()]
        return {"filtered_data": filtered}
    return {"all_data": stored_data}

# GET /data/{item_id} - Get specific item using path param
# Example: /data/2
@app.get("/data/{item_id}")
def get_item_by_id(item_id: int):
    for item in stored_data:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE /data/{item_id} - Delete specific item by id
@app.delete("/data/{item_id}")
def delete_item_by_id(item_id: int):
    global stored_data
    updated = [item for item in stored_data if item.id != item_id]
    if len(updated) == len(stored_data):
        raise HTTPException(status_code=404, detail="Item not found")
    stored_data = updated
    return {"message": f"Item with id {item_id} deleted."}

# DELETE /data - Clear all stored data
@app.delete("/data")
def clear_all_data():
    stored_data.clear()
    return {"message": "All data cleared"}
