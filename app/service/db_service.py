from app.database.builder import SqliteBuilder
from app.database.models.organizers import OrganizersData
from app.database.models.smart_contract import SmartContractData

db_builder = SqliteBuilder()
db_builder.buildOrganizers()
db_builder.buildSmartContract()
db = db_builder.getDatabase()

async def get_smart_contract_by_event_id(id: int):
    result = db.exec_query("SELECT * from smartContract WHERE eventId={1}".format(id))
    return SmartContractData.convert(result)

async def get_organizers_by_id(id: int):
    result = db.exec_query("SELECT * from organizers WHERE id={1}".format(id))
    return OrganizersData.convert(result)