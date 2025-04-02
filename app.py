from fastapi import FastAPI
from pydantic import BaseModel
from google_drive_utils import update_journal

app = FastAPI()

class JournalEntry(BaseModel):
    user_id: str
    session_data: dict

@app.post("/journal/update")
async def update_journal_entry(entry: JournalEntry):
    print("📥 Получен запрос:")
    print(f"user_id: {entry.user_id}")
    print(f"session_data: {entry.session_data}")

    update_journal(entry.user_id, entry.session_data)

    return {"status": "success", "message": f"Журнал обновлён для {entry.user_id}"}
 