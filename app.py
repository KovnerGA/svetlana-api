from fastapi import FastAPI, Request
from pydantic import BaseModel
from google_drive_utils import update_journal
import datetime
import json

app = FastAPI()


class JournalEntry(BaseModel):
    user_id: str
    session_data: dict
    mory_entry: str = ""


@app.post("/journal/update")
async def update_journal_entry(entry: JournalEntry):
    print("📘 Получен запрос на обновление журнала:")
    print(f"user_id: {entry.user_id}")
    print(f"session_data: {entry.session_data}")
    print(f"mory_entry: {entry.mory_entry}")

    update_journal(entry.user_id, entry.session_data, entry.mory_entry)

    return {"status": "success", "message": f"Журнал обновлён для {entry.user_id}"}


@app.post("/memory-log")
async def memory_log(request: Request):
    data = await request.json()
    print("🧠 Запись в память:")
    print(data)

    try:
        with open("memory_log.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "ok", "message": "Память записана"}
