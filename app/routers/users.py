from fastapi import APIRouter, HTTPException, status
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
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No organizer with this id: `{id}` found",
        )
    return {"result": result}

@router.put("/update_organizer/{id}")
async def update_organizer(id: int, item: OrganizersDataRequest):
    result = await db_service.update_organizer(id, item)
    return {"Status": "Success", "id": id}

@router.post("/create_organizer/")
async def insert_organizers(item: OrganizersDataRequest):
    id = await db_service.insert_organizers(item)
    if not id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to insert data",
        )
    return {"Status": "Success", "id": id}

@router.get("/get_smart_contract/{id}")
async def get_smart_contract(id: int):
    result = await db_service.get_smart_contract_by_id(id)
    return {"result": result}
    
@router.put("/update_smart_contract/{id}")
async def update_smart_contract(id: int, item: SmartContractDataRequest):
    result = await db_service.update_smart_contract(id, item)
    return {"Status": "Success", "id": id}