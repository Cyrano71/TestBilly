import os
from app.database.sqlite import Database
from app.database.models.models import Organizers
from app.database.models.models import SmartContracts
        
class SqliteBuilder():
    
    def __init__(self):
        self.__db = Database()
        
    async def build_database(self, path:str):
        await self.__db.open()
        organizers = Organizers.read(os.path.join(path, "organizers-data.csv"))
        smart_contracts = SmartContracts.read(os.path.join(path, "smart-contracts-data.json"))
        for organizer in organizers:
            organizer.ticketCollections = []
            for smart_contract in smart_contracts:
                if smart_contract.eventId == organizer.id:
                    organizer.ticketCollections.append(smart_contract)
        await self.__db.insert(organizers)
           
    def get_database(self):
        return self.__db
        