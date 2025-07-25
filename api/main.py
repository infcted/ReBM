"""
ReBM API Server
Copyright (c) 2024 Oscar Baeza
Licensed under the MIT License
"""

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.routes import nodes
from app.store.dynamodb import DynamoDBNodeStore
# from app.store.memory import InMemoryNodeStore
import os
import asyncio
import logging
from datetime import datetime, timezone

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ReBM API",
    version="0.0.1"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Choose your backend via ENV or config
backend = os.getenv("NODE_STORE_BACKEND", "dynamodb")
table = os.getenv("NODE_STORE_TABLE_NAME", "ReBM-dev")

if backend == "dynamodb":
    store = DynamoDBNodeStore(table_name=table)
# else:
#     store = InMemoryNodeStore()

# Include your node routes, injecting store
app.include_router(nodes.get_router(store), prefix="/nodes")

# Add a simple health check
@app.get("/health")
async def health():
    return {"status": "ok"}

# Background task to clean up expired nodes
async def cleanup_expired_nodes_task():
    """Background task to periodically clean up expired nodes"""
    while True:
        try:
            result = store.cleanup_expired_nodes()
            if result["message"] != "Cleaned up 0 expired nodes":
                logger.info(f"Background cleanup: {result['message']}")
        except Exception as e:
            logger.error(f"Error in background cleanup: {e}")
        
        # Wait for 5 minutes before next cleanup
        await asyncio.sleep(300)

@app.on_event("startup")
async def startup_event():
    """Start background tasks when the application starts"""
    asyncio.create_task(cleanup_expired_nodes_task())
    logger.info("Background cleanup task started")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up when the application shuts down"""
    logger.info("Application shutting down")
