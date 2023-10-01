from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from app.database.models.models import *

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
                
    async def select(self, query):
        async with self.async_session() as session:
            result = await session.execute(query)
            data = []
            for result in result.scalars():
                await result.awaitable_attrs.lineUp
                for ticket in await result.awaitable_attrs.ticketCollections:
                    await ticket.awaitable_attrs.metadataList
                data.append(result)
            return data

    async def exec_query(self, query):
        await self.cursor.execute(query)
        return await self.cursor.fetchall()
    
    async def exec_query_with_data(self, query, data):
        await self.cursor.execute(query, data)
        return await self.cursor.fetchall()

