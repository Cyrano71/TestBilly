from fastapi import APIRouter
from app.service import db_service
from app.schemas.schemas import *

router = APIRouter()

@router.get("/get_all_organizers/")
async def get_organizer():
    result = await db_service.get_organizers()
    return {"result": result}

@router.get("/get_organizer/{id}")
async def get_organizer(id: int):
    result = await db_service.get_organizer_by_id(id)
    return {"result": result}

@router.put("/update_organizer/{id}")
async def update_organizer(id: int, item: OrganizersPutRequest):
    result = await db_service.update_organizer(id, item)
    return {"SUCCESS": result}

@router.get("/get_smart_contract/{id}")
async def get_smart_contract(id: int):
    result = await db_service.get_smart_contract_by_id(id)
    return {"result": result}
    
@router.put("/update_smart_contract/{id}")
async def update_smart_contract(id: int, item: SmartContractPutRequest):
    result = await db_service.update_smart_contract(id, item)
    return {"SUCCESS": result}