from fastapi import APIRouter, HTTPException

def get_router(store):
    router = APIRouter()

    @router.get("/")
    async def list_nodes():
        return store.list_nodes()

    @router.get("/{node}")
    async def get_node(node: str):
        node_data = store.get_node(node)
        if not node_data:
            raise HTTPException(status_code=404, detail="Node not found")
        return node_data

    @router.post("/")
    async def create_node(body: dict):
        # Ensure the node field is set correctly
        if 'node_name' in body:
            body['node'] = body.pop('node_name')
        if 'name' in body:
            body['node'] = body.pop('name')
        return store.create_node(body)

    @router.delete("/{node}")
    async def delete_node(node: str):
        try:
            return store.delete_node(node)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/{node}/reserve")
    async def reserve_node(node: str, body: dict):
        user = body.get("user")
        expires_at = body.get("expires_at")
        duration_hours = body.get("duration_hours")

        if not user:
            raise HTTPException(status_code=400, detail="User is required")
        if not expires_at:
            if duration_hours:
                from datetime import datetime, timedelta, timezone
                expires_at = (datetime.now(timezone.utc) + timedelta(hours=duration_hours)).isoformat()
            else:
                raise HTTPException(status_code=400, detail="expires_at timestamp or duration_hours is required")
        try:
            return store.reserve_node(node, user, expires_at)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/{node}/release")
    async def release_node(node: str):
        try:
            return store.release_node(node)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/cleanup/expired")
    async def cleanup_expired_nodes():
        """Manually trigger cleanup of expired nodes"""
        return store.cleanup_expired_nodes()

    return router

