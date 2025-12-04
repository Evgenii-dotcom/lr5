from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Note:
    def __init__(self, id, title, content, tags):
        self.id = id
        self.title = title
        self.content = content
        self.tags = tags or []
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def update(self, title, content, tags):
        self.title = title
        self.content = content
        self.tags = tags or []
        self.updated_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class NoteService:
    def __init__(self):
        self.notes = []
        self.current_id = 1

    def get_all(self):
        return [note.to_dict() for note in self.notes]

    def get(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note.to_dict()
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    def create(self, title, content, tags):
        note = Note(self.current_id, title, content, tags)
        self.notes.append(note)
        self.current_id += 1
        return note.to_dict()

    def update(self, note_id, title, content, tags):
        for note in self.notes:
            if note.id == note_id:
                note.update(title, content, tags)
                return note.to_dict()
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    def delete(self, note_id):
        for i, note in enumerate(self.notes):
            if note.id == note_id:
                deleted = self.notes.pop(i)
                return deleted.to_dict()
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    def search_by_tag(self, tag):
        return [note.to_dict() for note in self.notes if tag in note.tags]

    def stats(self):
        total_notes = len(self.notes)
        total_tags = len(set(tag for note in self.notes for tag in note.tags))
        today = datetime.now().date()

        notes_today = len([
            note for note in self.notes
            if datetime.fromisoformat(note.created_at).date() == today
        ])

        return {
            "total_notes": total_notes,
            "total_tags": total_tags,
            "notes_created_today": notes_today
        }


class NoteCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: List[str]
    created_at: str
    updated_at: str


service = NoteService()
app = FastAPI(title="Notes API", version="1.0.0")


@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в API заметок!",
        "endpoints": {
            "GET /notes": "Получить все заметки",
            "GET /notes/{id}": "Получить заметку по ID",
            "POST /notes": "Создать новую заметку",
            "PUT /notes/{id}": "Обновить заметку",
            "DELETE /notes/{id}": "Удалить заметку"
        }
    }


@app.get("/notes", response_model=List[NoteResponse])
async def get_notes():
    return service.get_all()


@app.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int):
    return service.get(note_id)


@app.post("/notes", response_model=NoteResponse)
async def create_note(note: NoteCreate):
    return service.create(note.title, note.content, note.tags)


@app.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, note: NoteCreate):
    return service.update(note_id, note.title, note.content, note.tags)


@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    deleted = service.delete(note_id)
    return {"message": "Заметка удалена", "deleted_note": deleted}


@app.get("/notes/search/{tag}")
async def search_notes_by_tag(tag: str):
    found = service.search_by_tag(tag)
    return {"tag": tag, "count": len(found), "notes": found}


@app.get("/stats")
async def get_stats():
    return service.stats()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
