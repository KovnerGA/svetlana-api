from fastapi import FastAPI
from pydantic import BaseModel
from google_drive_utils import update_journal

app = FastAPI()

class JournalEntry(BaseModel):
    user_id: str
    session_data: dict
    mory_entry: str = ""  # Добавлено новое поле

@app.post("/journal/update")
async def update_journal_entry(entry: JournalEntry):
    print("📥 Получен запрос:")
    print(f"user_id: {entry.user_id}")
    print(f"session_data: {entry.session_data}")
    print(f"mory_entry: {entry.mory_entry}")

    update_journal(entry.user_id, entry.session_data, entry.mory_entry)

    return {"status": "success", "message": f"Журнал обновлён для {entry.user_id}"}
