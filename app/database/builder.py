from abc import ABC, abstractmethod
from app.database.sqlite import Database
from app.database.models.organizers import OrganizersData
from app.database.models.smart_contract import SmartContractData
import os

class DatabaseBuilder(ABC):
    @abstractmethod
    def buildOrganizers(self):
        pass
    
    @abstractmethod
    def buildSmartContract(self):
        pass
    
    @abstractmethod
    def getDatabase(self):
        pass
    
class SqliteBuilder(DatabaseBuilder):
    
    def __init__(self):
        self.__db = Database()
        
    def buildOrganizers(self):
        organizers = OrganizersData.read(os.path.join("data", "organizers-data.csv"))
        table_name = "organizers"
        self.__db.create_table(table_name, '''
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
           self.__db.insert(table_name, d)
        
        table_name = "linesUp"
        self.__db.create_table(table_name,'''
                                   organizersId INTEGER NOT NULL,
                                   name TEXT
                                ''')
                                
        for line_up in lines_up:     
           self.__db.insert(table_name, line_up)   
    
    def buildSmartContract(self):
        smart_contracts = SmartContractData.read(os.path.join("data", "smart-contracts-data.json"))
        smart_contract_table_name = "smartContract"
        self.__db.create_table(smart_contract_table_name, '''
                                              id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                              eventId INTEGER NOT NULL,
                                              collectionName TEXT,
                                              crowdsale TEXT,
                                              collection TEXT,
                                              multisig TEXT,
                                              startTime INTEGER NOT NULL,
                                              endTime INTEGER NOT NULL,
                                              isPresale INTEGER,
                                              metadataList BLOB,
                                              pricePerToken REAL,
                                              maxMintPerUser REAL,
                                              saleSize REAL,
                                              saleCurrency BLOB
                                ''')
        for smart_contract in smart_contracts:    
           self.__db.insert(smart_contract_table_name, smart_contract.__dict__)
           
    def getDatabase(self):
        return self.__db
        