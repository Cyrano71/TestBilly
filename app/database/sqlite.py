from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from app.database.models.models import *
from sqlalchemy import select

class Database:
    
    def __init__(self):
        self.engine = None
        self.async_session = None
    
    async def open(self):
        try:
            self.engine = create_async_engine('sqlite+aiosqlite://')
            self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            print(f"Error connecting to database {e}!")
    
    async def close(self):
        if self.engine:
            await engine.dispose()

    async def __aenter__(self):
        return self

    async def __aexit__(self,exc_type,exc_value,traceback):
        await self.close()

    async def insert(self, data):
        async with self.async_session() as session:
            async with session.begin():
                session.add_all(data)
    
    queries: dict = {
        TypeTable.SmartContracts : lambda x : select(SmartContracts).where(SmartContracts.id == x),
        TypeTable.Organizers : lambda x : select(Organizers).where(Organizers.id == x)
        }
    
    simple_queries: dict = {
        TypeTable.SmartContracts : lambda : select(SmartContracts),
        TypeTable.Organizers : lambda : select(Organizers)
        }
    
    async def select(self, table: TypeTable, where_id: int = None):
        async with self.async_session() as session:
            query = None
            if where_id:
                query = self.queries[table](where_id)
            else:
                query = self.simple_queries[table]()
               
            result = await session.execute(query)
            data = []
            for result in result.scalars():             
                if table == TypeTable.SmartContracts:
                    await result.awaitable_attrs.metadataList
                else:
                    await result.awaitable_attrs.lineUp
                    for ticket in await result.awaitable_attrs.ticketCollections:
                        await ticket.awaitable_attrs.metadataList
                data.append(result)
            return data
    
    async def update(self, table: TypeTable, where_id: int, update: dict):
        async with self.async_session() as session:
            query = self.queries[table](where_id)
            result = await session.execute(query)
            item = result.scalars().one()
            for key, value in update.items():
                setattr(item, key, value)
            await session.commit()
    
    async def update_relationship(self, table: TypeTable, where_id: int, update: list):
        async with self.async_session() as session:
            query = self.queries[table](where_id)
            
            result = await session.execute(query)
            item = result.scalars().one()
            
            if table == TypeTable.SmartContracts:
                await item.awaitable_attrs.metadataList     
                metadatas = [Metadatas(smart_contract_id=item.id, data=metadata) for metadata in update]
                item.metadataList = []
                await session.flush()
                item.metadataList = metadatas
                await session.commit()
            else:
                await item.awaitable_attrs.lineUp     
                linesUp = [LinesUp(organizer_id=item.id, data=lineUp) for lineUp in update]
                item.lineUp = []
                await session.flush()
                item.lineUp = linesUp
                await session.commit()

