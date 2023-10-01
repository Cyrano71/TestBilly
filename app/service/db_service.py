import asyncio
from app.database.builder import SqliteBuilder
from app.database.models.models import *
from app.schemas.schemas import *
from sqlalchemy import select

db = None

async def build():
    db_builder = SqliteBuilder()
    await db_builder.build_database("data")
    global db
    db = await db_builder.get_database()

async def get_organizers():
    return await db.select(TypeTable.Organizers)

async def get_organizer_by_id(id: int):
    return await db.select(TypeTable.Organizers, where_id=id)

async def update_organizer(id: int, item: OrganizersPutRequest):
    table = TypeTable.Organizers
    if item.lineUp:
        await db.update_relationship(table, id, item.lineUp)
    data = item.dict(exclude_unset=True, exclude={"lineUp"})    
    if data:              
        await db.update(table, id, data)
        
async def get_smart_contract_by_id(id: int):
    return await db.select(TypeTable.SmartContracts, where_id=id)

async def update_smart_contract(id: int, item: SmartContractPutRequest):
    table = TypeTable.SmartContracts
    if item.metadataList:
        await db.update_relationship(table, id, item.metadataList)
    data = item.dict(exclude_unset=True, exclude={"metadataList"})    
    if data:              
        await db.update(table, id, data)