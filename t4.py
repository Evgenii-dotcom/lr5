from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Notes API", version="1.0.0")

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

notes_db = []
current_id = 1

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
    return notes_db

@app.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int):
    for note in notes_db:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Заметка не найдена")

@app.post("/notes", response_model=NoteResponse)
async def create_note(note: NoteCreate):
    global current_id
    
    new_note = {
        "id": current_id,
        "title": note.title,
        "content": note.content,
        "tags": note.tags,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    notes_db.append(new_note)
    current_id += 1
    
    return new_note

@app.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, note: NoteCreate):
    for existing_note in notes_db:
        if existing_note["id"] == note_id:
            existing_note.update({
                "title": note.title,
                "content": note.content,
                "tags": note.tags,
                "updated_at": datetime.now().isoformat()
            })
            return existing_note
    
    raise HTTPException(status_code=404, detail="Заметка не найдена")

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    global notes_db
    
    for i, note in enumerate(notes_db):
        if note["id"] == note_id:
            deleted_note = notes_db.pop(i)
            return {
                "message": "Заметка удалена",
                "deleted_note": deleted_note
            }
    
    raise HTTPException(status_code=404, detail="Заметка не найдена")

@app.get("/notes/search/{tag}")
async def search_notes_by_tag(tag: str):
    filtered_notes = [note for note in notes_db if tag in note["tags"]]
    return {
        "tag": tag,
        "count": len(filtered_notes),
        "notes": filtered_notes
    }

@app.get("/stats")
async def get_stats():
    total_notes = len(notes_db)
    total_tags = len(set(tag for note in notes_db for tag in note["tags"]))
    
    return {
        "total_notes": total_notes,
        "total_tags": total_tags,
        "notes_created_today": len([
            note for note in notes_db 
            if datetime.fromisoformat(note["created_at"]).date() == datetime.now().date()
        ])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)