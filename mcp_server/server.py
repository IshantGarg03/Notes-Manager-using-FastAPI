from mcp.server.fastmcp import FastMCP
import asyncio
import uvicorn
from mcp_server.config import BACKEND_URL

# Import backend tool functions
from mcp_server.tools.get_notes import get_notes as fetch_notes
from mcp_server.tools.create_note import create_note as add_note
from mcp_server.tools.get_note import get_note as fetch_note
from mcp_server.tools.update_note import update_note as modify_note
from mcp_server.tools.delete_note import delete_note as remove_note

# Create MCP server
mcp = FastMCP(name="notes-mcp-server")

# Register tools
@mcp.tool(name="get_notes", description="List all notes")
async def tool_get_notes():
    try:
        return await fetch_notes()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool(name="create_note", description="Create a new note")
async def tool_create_note(title: str, content: str):
    try:
        return await add_note(title, content)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool(name="get_note", description="Fetch a note by ID")
async def tool_get_note(note_id: str):
    try:
        return await fetch_note(note_id)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool(name="update_note", description="Update a note by ID")
async def tool_update_note(note_id: str, title: str, content: str):
    try:
        return await modify_note(note_id, title, content)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool(name="delete_note", description="Delete a note by ID")
async def tool_delete_note(note_id: str):
    try:
        return await remove_note(note_id)
    except Exception as e:
        return {"error": str(e)}

# ------------------------
# Standalone Runner with Uvicorn
# ------------------------

if __name__ == "__main__":
    # Get the ASGI application instance from FastMCP
    fastmcp_app = mcp.streamable_http_app()
    
    # Run the application using uvicorn with the desired host and port
    uvicorn.run(fastmcp_app, host="127.0.0.1", port=8001)
