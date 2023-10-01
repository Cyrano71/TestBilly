from fastapi import APIRouter
from app.service import db_service
from app.schemas.smart_contract_request import SmartContractPutRequest

router = APIRouter()

@router.get("/get_all_organizers/")
async def get_organizer():
    result = await db_service.get_organizers()
    return {"result": result}

@router.get("/get_organizer/{id}")
async def get_organizer(id: int):
    result = await db_service.get_organizers_by_id(id)
    return {"result": result}
    
@router.put("/update_smart_contract/{id}")
async def update_item(id: int, item: SmartContractPutRequest):
    pass
    #result = await db_service.update_smart_contract(id, item)
    #return result