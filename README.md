# Loop AI Ingest API

## How to run locally

1. Install dependencies:
pip install -r requirements.txt

2. Run the server:
uvicorn main:app --reload

3. Visit:
- Home:http://localhost:8000/
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

# Data Ingestion API System

## Overview

This project implements a simple asynchronous data ingestion API system using **FastAPI**.  
It allows clients to submit ingestion requests with a list of IDs and priority, processes these requests in batches asynchronously with rate limiting and priority handling, and exposes a status endpoint to track progress.

---

## Features

- **POST /ingest**: Accepts ingestion requests containing a list of IDs and a priority (HIGH, MEDIUM, LOW).  
- IDs are split into batches of 3 for processing.
- **Batch processing** is asynchronous, simulates external API calls with delay, and respects a rate limit of **1 batch per 5 seconds**.
- Requests with higher priority batches are processed first.
- **GET /status/{ingestion_id}**: Returns the overall ingestion status and details of each batch's status.  
- In-memory storage for ingestions and batches (suitable for demonstration and testing).

---

## Design Choices

- **FastAPI Framework**: Selected for its speed, async support, and ease of building RESTful APIs.  
- **Asyncio + Heap Queue**: Used `asyncio` for asynchronous batch processing and `heapq` as a priority queue, prioritizing by (priority level, creation time, tie-breaker).  
- **Batching**: Requests are split into batches of size 3 as per requirements.  
- **Rate Limiting**: Implemented via `asyncio.sleep(5)` between batches to simulate external API rate limit of one batch per 5 seconds.
- **In-Memory Persistence**: Stored ingestion and batch metadata in Python dictionaries for simplicity.  
- **Thread-safe Async Lock**: Used `asyncio.Lock` to guard shared data structures ensuring safe concurrent access in async environment.
- **Unique IDs**: Used UUID4 to generate unique ingestion and batch IDs.

---

## Getting Started

### Prerequisites

- Python 3.9+ installed
- `pip` package manager
![image](https://github.com/user-attachments/assets/dd363b3c-883e-4237-8f47-d46cb0357942)
![image](https://github.com/user-attachments/assets/6f1fa27e-1fc5-45a2-831f-91ac8cc5b482)

