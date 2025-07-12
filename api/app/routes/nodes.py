from fastapi import APIRouter, HTTPException

def get_router(store):
    router = APIRouter()

    @router.get("/")
    async def list_nodes():
        return store.list_nodes()

    @router.get("/{node_name}")
    async def get_node(node_name: str):
        node = store.get_node(node_name)
        if not node:
            raise HTTPException(status_code=404, detail="Node not found")
        return node

    @router.post("/")
    async def create_node(body: dict):
        return store.create_node(body)

    @router.delete("/{node_name}")
    async def delete_node(node_name: str):
        return store.delete_node(node_name)

    @router.post("/{node_name}/reserve")
    async def reserve_node(node_name: str, body: dict):
        user = body["user"]
        ttl = body["ttl_seconds"]
        return store.reserve_node(node_name, user, ttl)

    @router.post("/{node_name}/release")
    async def release_node(node_name: str):
        return store.release_node(node_name)

    return router

