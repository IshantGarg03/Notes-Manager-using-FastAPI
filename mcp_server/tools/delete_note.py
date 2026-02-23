import httpx
from mcp_server.config import BACKEND_URL

async def delete_note(note_id: str):
    """Delete a note by ID in FastAPI backend"""
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BACKEND_URL}/notes/{note_id}")
        response.raise_for_status()
        return {"status": "deleted", "note_id": note_id}