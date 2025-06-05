from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import List, Dict
import uuid
import time
import threading
import asyncio
import heapq

app = FastAPI()

# -------------------------------
# Priority Enum
# -------------------------------
class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

# -------------------------------
# Request Model
# -------------------------------
class IngestRequest(BaseModel):
    ids: List[int]
    priority: Priority

# -------------------------------
# Global In-Memory Stores
# -------------------------------
ingestions: Dict[str, dict] = {}         # ingestion_id → metadata
batch_store: Dict[str, dict] = {}        # batch_id → batch info
processing_queue = []                    # Heap queue: (priority, time, tiebreaker, batch)

# Lock for thread-safe access
lock = threading.Lock()

# Priority level mapping
priority_map = {
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3
}

# -------------------------------
# Async Batch Processor
# -------------------------------
async def process_batches():
    while True:
        await asyncio.sleep(0.1)

        with lock:
            if not processing_queue:
                continue

            # Always pop (priority, time, tie_id, batch)
            _, _, _, batch = heapq.heappop(processing_queue)

        batch_id = batch["batch_id"]
        batch_store[batch_id]["status"] = "triggered"

        await asyncio.sleep(5)  # Simulate 5s rate-limited processing

        # Simulate API call and mark as completed
        batch_store[batch_id]["status"] = "completed"

# -------------------------------
# Start Background Worker Thread
# -------------------------------
def start_worker():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_batches())

threading.Thread(target=start_worker, daemon=True).start()

# -------------------------------
# POST /ingest
# -------------------------------
@app.post("/ingest")
def ingest(request: IngestRequest):
    ingestion_id = str(uuid.uuid4())
    created_time = time.time()

    # Split into batches of 3
    ids = request.ids
    batches = [ids[i:i + 3] for i in range(0, len(ids), 3)]
    batch_ids = []

    with lock:
        for batch_ids_list in batches:
            batch_id = str(uuid.uuid4())
            batch = {
                "batch_id": batch_id,
                "ids": batch_ids_list,
                "status": "yet_to_start",
                "ingestion_id": ingestion_id
            }

            batch_store[batch_id] = batch

            # ✅ FIX: Add tie-breaker UUID for safe comparison
            heapq.heappush(processing_queue, (
                priority_map[request.priority],
                created_time,
                str(uuid.uuid4()),  # tie-breaker
                batch
            ))

            batch_ids.append(batch_id)

        # Store ingestion metadata
        ingestions[ingestion_id] = {
            "priority": request.priority,
            "created_time": created_time,
            "batch_ids": batch_ids
        }

    return {"ingestion_id": ingestion_id}

# -------------------------------
# GET /status/{ingestion_id}
# -------------------------------
@app.get("/status/{ingestion_id}")
def get_status(ingestion_id: str):
    if ingestion_id not in ingestions:
        raise HTTPException(status_code=404, detail="Ingestion ID not found")

    data = ingestions[ingestion_id]
    batch_ids = data["batch_ids"]
    batch_statuses = [batch_store[bid]["status"] for bid in batch_ids]

    if all(status == "yet_to_start" for status in batch_statuses):
        overall_status = "yet_to_start"
    elif all(status == "completed" for status in batch_statuses):
        overall_status = "completed"
    else:
        overall_status = "triggered"

    return {
        "ingestion_id": ingestion_id,
        "status": overall_status,
        "batches": [
            {
                "batch_id": bid,
                "ids": batch_store[bid]["ids"],
                "status": batch_store[bid]["status"]
            }
            for bid in batch_ids
        ]
    }
