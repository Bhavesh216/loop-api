# Loop AI Ingest API

## How to run locally

1. Install dependencies:
pip install -r requirements.txt

2. Run the server:
uvicorn main:app --reload

3. Visit:
- Home: http://127.0.0.1:8000/
- Swagger Docs: http://localhost:8000/docs
- URL: https://first-loop-api.onrender.com/

# Loop AI Assignment – Data Ingestion API

This is a FastAPI-based microservice for data ingestion with priority queuing, batch processing, and status tracking.

## 🔧 Endpoints

### 1. `POST /ingest`

- Accepts a list of integer `ids` and a `priority` level (`HIGH`, `MEDIUM`, `LOW`)
- Batches are created (max 3 ids per batch)
- Each batch is enqueued and processed in the background
- Only **1 batch is processed every 5 seconds**
- High priority jobs are processed before low priority ones
- Returns a unique `ingestion_id`

**Sample Request:**

```json
POST /ingest
{
  "ids": [1, 2, 3, 4, 5],
  "priority": "MEDIUM"
}
