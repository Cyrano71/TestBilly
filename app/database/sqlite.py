import sqlite3
from app.database.models.smart_contract import SmartContractData
import os

class Database:
    
    def __init__(self, name="billy.db"):    
        self.conn = None
        self.cursor = None
        self.name = name
        self.open(name)
    
    def open(self,name):     
        try:
            self.conn = sqlite3.connect(name);
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            print("Error connecting to database!")
    
    def close(self):     
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()  

    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        self.close()

    def create_table(self, tableName, query):
        self.cursor.execute('DROP TABLE IF EXISTS {0}'.format(tableName))
        self.cursor.execute("CREATE TABLE {0}({1})".format(tableName, query))

    def insert(self, tableName, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(tableName, columns, placeholders)
                        
        self.cursor.execute(sql, list(data.values()))
        self.conn.commit()
        
        return self.cursor.lastrowid

    def exec_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def exec_query_with_data(self, query, data):
        self.cursor.execute(query, data)
        return self.cursor.fetchall()

