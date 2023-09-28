import pytest
import os

from app.database.sqlite import Database
from app.database.models.smart_contract import read_json_data

def test_insert():
    data = read_json_data(os.path.join("data", "smart-contracts-data.json"))
    with Database() as db:
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
           
        result = db.exec_query("select * from {0}".format(table_name))
        assert len(result) == 8