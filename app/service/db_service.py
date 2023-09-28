from app.database.sqlite import Database
from app.database.models.smart_contract import read_json_data
import os

data = read_json_data(os.path.join("data", "smart-contracts-data.json"))
db = Database()
table_name = "SMART_CONTRACT"
db.create_table(table_name, '''
                              ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                              EVENT_ID INT NOT NULL,
                              COLLECTION_NAME TEXT,
                              START_TIME INTEGER NOT NULL,
                              END_TIME INTEGER NOT NULL,
                              PRICE_PER_TOKEN REAL NOT NULL,
                              MAX_MINT_PER_USER REAL NOT NULL,
                              SALE_SIZE REAL NOT NULL
                        ''')
for item in data:    
   db.insert(table_name, item.__dict__)
   
async def get_item_by_event_id(id: int):
    return db.exec_query("SELECT * from SMART_CONTRACT WHERE EVENT_ID={0}".format(id))