from app.database.sqlite import Database
from app.database.models.smart_contract import SmartContractData
from app.database.models.organizers import OrganizersData
import os

db = Database()

data = SmartContractData.read(os.path.join("data", "smart-contracts-data.json"))
smart_contract_table_name = "smartContract"
db.create_table(smart_contract_table_name, '''
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
   db.insert(smart_contract_table_name, item.__dict__)

data = OrganizersData.read(os.path.join("data", "organizers-data.csv"))  
organizers_table_name = "organizers"
db.create_table(organizers_table_name, '''
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
    db.insert(organizers_table_name, item.__dict__)
   
async def get_smart_contract_by_event_id(id: int):
    result = db.exec_query("SELECT * from {0} WHERE eventId={1}".format(smart_contract_table_name, id))
    return SmartContractData.convert(result)

async def get_organizers_by_id(id: int):
    result = db.exec_query("SELECT * from {0} WHERE id={1}".format(organizers_table_name, id))
    return OrganizersData.convert(result)