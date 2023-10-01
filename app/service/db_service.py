from app.database.builder import SqliteBuilder
from app.database.models.organizers import OrganizersData
from app.database.models.smart_contract import SmartContractData
import os
import asyncio

db = None

async def build():
    db_builder = SqliteBuilder()
    await db_builder.init_database()
    await db_builder.buildOrganizers(os.path.join("data", "organizers-data.csv"))
    await db_builder.buildSmartContract(os.path.join("data", "smart-contracts-data.json"))
    global db
    db = await db_builder.getDatabase()

async def get_smart_contract_by_event_id(event_id: int):
    sql = """
             select *, GROUP_CONCAT(metadata, ',') as metadataList from
             (
                select * from  
                (
                   select * from smartContract where eventId=?
                ) smartContract 
                left join metadatas on smartContract.id = metadatas.smartContractId
              ) smartContract 
              Group By smartContract.id
           """
    result = await db.exec_query_with_data(sql, [event_id])
    return SmartContractData.convert(result)

async def update_smart_contract(id: int, item: SmartContractData):
    data = item.dict(exclude_unset=True)
    placeholders = ''
    for key in data.keys():
        placeholders += key + '=?,'
    sql = '''UPDATE smartContract SET {}
            WHERE id=?
            '''.format(placeholders[:-1])
    result = await db.exec_query_with_data(sql, list(data.values()) + [id])
    return SmartContractData.convert(result)

async def get_organizers_by_id(id: int):
    sql = """
                select *, GROUP_CONCAT(name, '-') as lineUp from
                (
                    select * from 
                    (
                        select * from organizers where id=?
                    ) organizers
                    left join linesUp on organizers.id = linesUp.organizersId   
                ) organizers
                Group By organizers.id
                """
    result = await db.exec_query_with_data(sql, [id])
    return OrganizersData.convert(result)