from fastapi import APIRouter
from app.service import db_service
from app.schemas.schemas import *
from fastapi import Depends
from typing import Generator

router = APIRouter()

async def get_db()-> Generator:
    yield db_service.db_builder.get_database()

@router.get("/get_all_organizers/")
async def get_organizer(db = Depends(get_db)):
    result = await db_service.get_organizers(db)
    return {"result": result}

@router.get("/get_organizer/{id}")
async def get_organizer(id: int, db = Depends(get_db)):
    result = await db_service.get_organizer_by_id(db, id)
    return {"result": result}

@router.put("/update_organizer/{id}")
async def update_organizer(id: int, item: OrganizersPutRequest, db = Depends(get_db)):
    result = await db_service.update_organizer(db, id, item)
    return result

@router.get("/get_smart_contract/{id}")
async def get_smart_contract(id: int, db = Depends(get_db)):
    result = await db_service.get_smart_contract_by_id(db, id)
    return {"result": result}
    
@router.put("/update_smart_contract/{id}")
async def update_smart_contract(id: int, item: SmartContractPutRequest, db = Depends(get_db)):
    result = await db_service.update_smart_contract(db, id, item)
    return result