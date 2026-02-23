import httpx
from mcp_server.config import BACKEND_URL

async def update_note(note_id: str, title: str, content: str):
    """Update a note by ID in FastAPI backend"""
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{BACKEND_URL}/notes/{note_id}",
            json={"title": title, "content": content}
        )
        response.raise_for_status()
        return response.json()