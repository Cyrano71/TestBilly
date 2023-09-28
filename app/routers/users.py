from fastapi import APIRouter
from app.service import db_service

router = APIRouter()

@router.get("/get_events/{event_id}")
async def read_events_from_db(event_id: int):
    result = await db_service.get_item_by_event_id(event_id)
    return {"result": result}