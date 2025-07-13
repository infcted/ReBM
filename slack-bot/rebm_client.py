import aiohttp
import logging
from config import Config

logger = logging.getLogger(__name__)

class ReBMClient:
    def __init__(self, api_url=None, timeout=None):
        self.api_url = api_url or Config.REBM_API_URL
        self.timeout = timeout or Config.REBM_API_TIMEOUT
        self.session = None

    async def _get_session(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session

    async def _make_request(self, method, endpoint, data=None):
        session = await self._get_session()
        url = f"{self.api_url}{endpoint}"
        try:
            async with session.request(method, url, json=data) as resp:
                resp.raise_for_status()
                return await resp.json()
        except Exception as e:
            logger.error(f"API request failed: {e}")
            return None

    async def get_nodes(self):
        resp = await self._make_request("GET", "/nodes/")
        return resp.get("nodes", []) if resp else []

    async def get_node(self, node_name):
        return await self._make_request("GET", f"/nodes/{node_name}")

    async def create_node(self, node_name, description=""):
        return await self._make_request("POST", "/nodes/", {"name": node_name, "description": description})

    async def delete_node(self, node_name):
        return await self._make_request("DELETE", f"/nodes/{node_name}")

    async def reserve_node(self, node_name, user, duration_hours=24):
        return await self._make_request("POST", f"/nodes/{node_name}/reserve", {"user": user, "duration_hours": duration_hours})

    async def release_node(self, node_name):
        return await self._make_request("POST", f"/nodes/{node_name}/release")

    async def cleanup_expired(self):
        return await self._make_request("POST", "/nodes/cleanup/expired")

    async def health_check(self):
        try:
            await self._make_request("GET", "/health")
            return True
        except Exception:
            return False

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close() 