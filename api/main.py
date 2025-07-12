from fastapi import FastAPI
from app.routes import nodes
from app.store.dynamodb import DynamoDBNodeStore
# from app.store.memory import InMemoryNodeStore
import os

app = FastAPI(
    title="ReBM API",
    version="0.0.1"
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
