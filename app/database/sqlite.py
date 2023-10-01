import sqlite3
from app.database.models.smart_contract import SmartContractData
import os
import aiosqlite

class Database:
    
    def __init__(self, name="billy.db"):    
        self.conn = None
        self.cursor = None
        self.name = name
    
    async def open(self):     
        try:
            self.conn = await aiosqlite.connect(self.name);
            self.cursor = await self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!")
    
    async def close(self):     
        if self.conn:
            await self.conn.commit()
            await self.cursor.close()
            await self.conn.close()  

    async def __aenter__(self):
        return self

    async def __aexit__(self,exc_type,exc_value,traceback):
        await self.close()

    async def create_table(self, tableName, query):
        await self.cursor.execute('DROP TABLE IF EXISTS {0}'.format(tableName))
        await self.cursor.execute("CREATE TABLE {0}({1})".format(tableName, query))

    async def insert(self, tableName, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(tableName, columns, placeholders)
                        
        await self.cursor.execute(sql, list(data.values()))
        await self.conn.commit()
        
        return self.cursor.lastrowid

    async def exec_query(self, query):
        await self.cursor.execute(query)
        return await self.cursor.fetchall()
    
    async def exec_query_with_data(self, query, data):
        await self.cursor.execute(query, data)
        return await self.cursor.fetchall()

