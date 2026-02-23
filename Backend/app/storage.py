import json
import os
import tempfile
import threading
from typing import List, Dict, Any

_lock = threading.Lock()  # simple in-process lock


class JSONStore:
    """
    Tiny atomic JSON file-backed store for a list of dicts.

    - ensures file exists
    - reads/writes atomically using tempfile + os.replace
    - uses a thread lock to reduce race conditions in single-process servers
    """

    def __init__(self, filename: str):
        self.filename = filename
        dirpath = os.path.dirname(self.filename)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        # initialize file if missing
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def read_all(self) -> List[Dict[str, Any]]:
        """Return list of objects from JSON file."""
        with _lock:
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    # If file contains something else, reset to empty list
                    return []
                except json.JSONDecodeError:
                    return []

    def write_all(self, notes: List[Dict[str, Any]]):
        """
        Atomically write the full list of notes to the JSON file.
        Uses tempfile + os.replace for atomicity.
        """
        dirpath = os.path.dirname(self.filename) or "."
        fd, tmp_path = tempfile.mkstemp(dir=dirpath)
        try:
            # fdopen accepts encoding
            with os.fdopen(fd, "w", encoding="utf-8") as tmp:
                json.dump(notes, tmp, ensure_ascii=False, indent=2)
            # atomic replace
            os.replace(tmp_path, self.filename)
        finally:
            # cleanup if something went wrong before replace
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
