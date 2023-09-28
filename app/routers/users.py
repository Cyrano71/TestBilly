from fastapi import APIRouter
from app.service import db_service

router = APIRouter()

@router.get("/get_smart_contract/{event_id}")
async def get_smart_contract(event_id: int):
    result = await db_service.get_smart_contract_by_event_id(event_id)
    return {"result": result}

@router.get("/get_organizer/{id}")
async def get_organizer(id: int):
    result = await db_service.get_organizers_by_id(id)
    return {"result": result}