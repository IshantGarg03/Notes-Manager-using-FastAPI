import httpx
from mcp_server.config import BACKEND_URL

async def get_note(note_id: str):
    """Fetch a single note by ID from FastAPI backend"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/notes/{note_id}")
        response.raise_for_status()
        return response.json()