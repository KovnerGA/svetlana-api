from fastapi import FastAPI, Request
from google_drive_utils import update_journal

app = FastAPI()

@app.post("/journal/update")
async def update_journal_entry(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    session_data = data.get("session_data")
    if not user_id or not session_data:
        return {"error": "Missing user_id or session_data"}
    
    update_journal(user_id, session_data)
    return {"status": "success", "message": f"Журнал обновлён для {user_id}"}