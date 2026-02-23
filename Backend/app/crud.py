import json
from datetime import datetime
from uuid import uuid4
from typing import List, Optional
from app.schemas import NoteCreate, NoteUpdate, Note

class NoteCRUD:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _load_notes(self) -> List[dict]:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def _save_notes(self, notes: List[dict]):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(notes, f, indent=4)

    def create_note(self, note_in: NoteCreate) -> Note:
        notes = self._load_notes()
        new_note = {
            "id": str(uuid4()),
            "title": note_in.title,
            "content": note_in.content,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        notes.append(new_note)
        self._save_notes(notes)
        return new_note

    def list_notes(self) -> List[Note]:
        return self._load_notes()

    def get_note(self, note_id: str) -> Optional[Note]:
        notes = self._load_notes()
        for note in notes:
            if note["id"] == note_id:
                return note
        return None

    def update_note(self, note_id: str, note_in: NoteUpdate) -> Optional[Note]:
        notes = self._load_notes()
        for idx, note in enumerate(notes):
            if note["id"] == note_id:
                # Apply only provided fields
                if note_in.title is not None:
                    note["title"] = note_in.title
                if note_in.content is not None:
                    note["content"] = note_in.content
                note["updated_at"] = datetime.utcnow().isoformat()

                notes[idx] = note
                self._save_notes(notes)
                return note
        return None

    def delete_note(self, note_id: str) -> bool:
        notes = self._load_notes()
        for idx, note in enumerate(notes):
            if note["id"] == note_id:
                notes.pop(idx)
                self._save_notes(notes)
                return True
        return False
