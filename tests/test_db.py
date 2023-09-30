import pytest
import os

from app.database.sqlite import Database
from app.database.models.smart_contract import SmartContractData
from app.database.models.organizers import OrganizersData

def test_smart_contract_data_insert():
    data = SmartContractData.read(os.path.join("data", "smart-contracts-data.json"))
    with Database() as db:
        table_name = "smartContract"
        db.create_table(table_name, '''
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
    
        for item in data:    
           db.insert(table_name, item.__dict__)
           
        result = db.exec_query("select * from {0}".format(table_name))
        result = SmartContractData.convert(result)
        assert len(result) == 8
        
def test_organizers_data_insert():
    data = OrganizersData.read(os.path.join("data", "organizers-data.csv"))
    with Database() as db:
        table_name = "organizers"
        db.create_table(table_name, '''
                                      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                      eventTitle TEXT,
                                      eventStartDate INTEGER,
                                      eventEndDate INTEGER,
                                      nameLocation TEXT,
                                      addressLocation TEXT,
                                      totalTicketNumberInteger INTEGER,
                                      maximumTicketsPerUser INTEGER,
                                      saleStartDate TEXT,
                                      lineUp BLOB,
                                      eventImageVideoUrl TEXT
                                ''')
    
        for item in data:    
           db.insert(table_name, item.__dict__)
           
        result = db.exec_query("select * from {0}".format(table_name))
        result = OrganizersData.convert(result)
        assert len(result) == 5

if __name__ == '__main__':
    os.chdir('../')
    test_organizers_data_insert()