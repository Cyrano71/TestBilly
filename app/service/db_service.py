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

def transform2(smart_contracts: list):
    result = []
    for smart_contract in smart_contracts:
        result.append(SmartContractGetRequest(
        id = smart_contract.id,
        eventId = smart_contract.eventId,
        collectionName = smart_contract.collectionName,
        crowdsale = smart_contract.crowdsale,
        collection = smart_contract.collection,
        multisig = smart_contract.multisig,
        startTime = smart_contract.startTime,
        endTime = smart_contract.endTime,
        isPresale = smart_contract.isPresale,
        pricePerToken = smart_contract.pricePerToken,
        maxMintPerUser = smart_contract.maxMintPerUser,
        saleSize = smart_contract.saleSize,
        saleCurrency = smart_contract.saleCurrency,
        metadataList = [meta.data for meta in smart_contract.metadataList],
        ))
    return result
    
def transform1(organizers: list):
    result = []
    for organizer in organizers:
        org = OrganizersGetRequest(
            id = organizer.id,
            eventTitle = organizer.eventTitle,
            eventStartDate = organizer.eventStartDate,
            eventEndDate = organizer.eventEndDate,
            nameLocation = organizer.nameLocation,
            addressLocation = organizer.addressLocation,
            totalTicketNumberInteger = organizer.totalTicketNumberInteger,
            maximumTicketsPerUser = organizer.maximumTicketsPerUser,
            saleStartDate = organizer.saleStartDate,
            eventImageVideoUrl = organizer.eventImageVideoUrl,
            lineUp = '-'.join([line.data for line in organizer.lineUp]),
            )
        org.ticketCollections = transform2(organizer.ticketCollections)
        result.append(org)
    return result

transform : dict = {
    TypeTable.SmartContracts: lambda x: transform2(x),
    TypeTable.Organizers: lambda x: transform1(x)
    }

async def get(table: TypeTable, id: int = None):
    if id:
        result = await db.select(table, where_id=id)
    else:
        result = await db.select(table)
    return transform[table](result)
  
async def get_organizers():
    return await get(TypeTable.Organizers) 

async def get_organizer_by_id(id: int):
    return await get(TypeTable.Organizers, id)

async def get_smart_contract_by_id(id: int):
    return await get(TypeTable.SmartContracts, id)

async def update(table: TypeTable, item, id: int, property_name: str):
    prop = getattr(item, property_name)
    if prop:
        await db.update_relationship(table, id, prop)
    data = item.dict(exclude_unset=True, exclude={property_name})    
    if data:              
        await db.update(table, id, data)

async def update_organizer(id: int, item: OrganizersPutRequest):
    await update(TypeTable.Organizers, item, id, "lineUp")

async def update_smart_contract(id: int, item: SmartContractPutRequest):
    await update(TypeTable.SmartContracts, item, id, "metadataList")