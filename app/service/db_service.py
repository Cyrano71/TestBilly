import asyncio
from app.database.builder import SqliteBuilder
from app.database.models.models import Organizers
from sqlalchemy import select

db = None

async def build():
    db_builder = SqliteBuilder()
    await db_builder.build_database("data")
    global db
    db = await db_builder.get_database()

async def get_organizers():
    return await db.select(select(Organizers))

async def get_organizers_by_id(id: int):
    return await db.select(select(Organizers).where(Organizers.id == id))

"""
async def update_smart_contract(id: int, item: SmartContractData):
    data = item.dict(exclude_unset=True)
    placeholders = ''
    for key in data.keys():
        placeholders += key + '=?,'
    sql = '''UPDATE smartContract SET {}
            WHERE id=?
            '''.format(placeholders[:-1])
    result = await db.exec_query_with_data(sql, list(data.values()) + [id])
    #return SmartContractData.convert(result)
"""