import httpx
from mcp_server.config import BACKEND_URL

async def get_notes():
    """Fetch all notes from FastAPI backend"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/notes")
        response.raise_for_status()
        return response.json()