import httpx
from mcp_server.config import BACKEND_URL

async def create_note(title: str, content: str):
    """Create a new note in FastAPI backend"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/notes",
            json={"title": title, "content": content}
        )
        response.raise_for_status()
        return response.json()