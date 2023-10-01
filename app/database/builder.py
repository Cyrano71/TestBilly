import os
import json
from abc import ABC, abstractmethod
from app.database.sqlite import Database
from app.database.models.organizers import OrganizersData
from app.database.models.smart_contract import SmartContractData
        
class DatabaseBuilder(ABC):
    
    @abstractmethod
    async def build_database(self):
        pass
    
    @abstractmethod
    async def build_organizers(self, path: str):
        pass
    
    @abstractmethod
    async def build_smart_contract(self, path: str):
        pass
    
    @abstractmethod
    async def get_database(self):
        pass
    
class SqliteBuilder(DatabaseBuilder):
    
    def __init__(self):
        self.__db = Database()
        
    async def build_database(self):
        await self.__db.open()
           
    async def build_organizers(self, path: str):
        organizers = OrganizersData.read(path)
        table_name = "organizers"
        await self.__db.create_table(table_name, '''
                                      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                      eventTitle TEXT,
                                      eventStartDate INTEGER,
                                      eventEndDate INTEGER,
                                      nameLocation TEXT,
                                      addressLocation TEXT,
                                      totalTicketNumberInteger INTEGER,
                                      maximumTicketsPerUser INTEGER,
                                      saleStartDate TEXT,
                                      eventImageVideoUrl TEXT
                                ''')
                                
        lines_up = []
        for organizer in organizers:    
           d = organizer.__dict__
           if d['lineUp']:
               for l in d['lineUp'].split('-'):        
                   lines_up.append({'organizersId' : d['id'], 'name' : l})
           del d['lineUp']
           await self.__db.insert(table_name, d)
        
        table_name = "linesUp"
        await self.__db.create_table(table_name,'''
                                   organizersId INTEGER NOT NULL,
                                   name TEXT
                                ''')
                                
        for line_up in lines_up:     
           await self.__db.insert(table_name, line_up)   
    
    async def build_smart_contract(self, path: str):
        smart_contracts = SmartContractData.read(path)
        
        table_name = "smartContract"
        await self.__db.create_table(table_name, '''
                                              id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                              eventId INTEGER NOT NULL,
                                              collectionName TEXT,
                                              crowdsale TEXT,
                                              collection TEXT,
                                              multisig TEXT,
                                              startTime INTEGER NOT NULL,
                                              endTime INTEGER NOT NULL,
                                              isPresale INTEGER,
                                              pricePerToken REAL,
                                              maxMintPerUser REAL,
                                              saleSize REAL,
                                              saleCurrency TEXT
                                ''')
        
        metadatas = []
        for smart_contract in smart_contracts:  
            d = smart_contract.__dict__
            del d['id']
            metadataList = d['metadataList']
            del d['metadataList']
            d["saleCurrency"] = json.dumps(d["saleCurrency"])
            last_id = await self.__db.insert(table_name, d)
            if metadataList:
                for m in metadataList:
                    metadatas.append({"smartContractId" : last_id, "metadata" : m})
            
         
        table_name = "metadatas"
        await self.__db.create_table(table_name, '''
                                              smartContractId INTEGER NOT NULL,
                                              metadata TEXT NOT NULL
                                ''')
        for metadata in metadatas:     
           await self.__db.insert(table_name, metadata)   
           
    async def get_database(self):
        return self.__db
        