from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from app.schemas import NoteCreate, NoteUpdate, Note
from app.crud import NoteCRUD

app = FastAPI(title="Note Manager API")

# Allow all origins for local/dev use. In production narrow this down.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# instantiate CRUD with path to JSON file
crud = NoteCRUD("notes.json")


@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note_in: NoteCreate):
    """
    Create a new note. Returns the created note (including generated id).
    """
    return crud.create_note(note_in)


@app.get("/notes", response_model=List[Note])
def list_notes():
    """
    List all notes.
    """
    return crud.list_notes()


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: str):
    """
    Get a single note by id.
    """
    note = crud.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: str, note_in: NoteUpdate):
    """
    Update an existing note (partial update allowed).
    """
    note = crud.update_note(note_id, note_in)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str):
    """
    Delete a note by id.
    """
    ok = crud.delete_note(note_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    return None
