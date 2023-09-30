import pytest
import os
from app.database.builder import SqliteBuilder
from app.database.models.organizers import OrganizersData
from app.database.models.smart_contract import SmartContractData
   
def test_smart_contract_data_insert():
    db_builder = SqliteBuilder()
    db_builder.buildSmartContract()
    with db_builder.getDatabase() as db:
        result = db.exec_query("select * from smartContract")
        result = SmartContractData.convert(result)
        assert len(result) == 8
        
def test_organizers_data_insert():
    db_builder = SqliteBuilder()
    db_builder.buildOrganizers()
    db = db_builder.getDatabase()
        
    sql = """
            select *, GROUP_CONCAT(name, '-') as lineUp from
            (
            select * from organizers left join linesUp on organizers.id = linesUp.organizersId
            ) sub
            Group By sub.id
            """
    result = db.exec_query(sql)
    result = OrganizersData.convert(result)
    assert len(result) == 5

if __name__ == '__main__':
    os.chdir('../')
    test_smart_contract_data_insert()