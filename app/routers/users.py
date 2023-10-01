from fastapi import APIRouter
from app.service import db_service
from app.schemas.smart_contract_schema import SmartContractPutRequest

router = APIRouter()

@router.get("/get_smart_contract/{event_id}")
async def get_smart_contract(event_id: int):
    result = await db_service.get_smart_contract_by_event_id(event_id)
    return {"result": result}    
    
@router.put("/update_smart_contract/{id}")
async def update_item(id: int, item: SmartContractPutRequest):
    result = await db_service.update_smart_contract(id, item)
    return result

@router.get("/get_organizer/{id}")
async def get_organizer(id: int):
    result = await db_service.get_organizers_by_id(id)
    return {"result": result}