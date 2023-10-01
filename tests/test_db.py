import pytest
import os
import configparser
from app.database.builder import SqliteBuilder
from app.database.models.organizers import OrganizersData
from app.database.models.smart_contract import SmartContractData
    
def test_smart_contract_data_insert():
    db_builder = SqliteBuilder()
    db_builder.buildSmartContract(os.path.join("data", "smart-contracts-data.json"))
    with db_builder.getDatabase() as db:
        sql = """
            select *, GROUP_CONCAT(metadata, ',') as metadataList from
            (
            select * from smartContract left join metadatas on smartContract.id = metadatas.smartContractId
            ) sub
            Group By sub.id
            """
        result = db.exec_query(sql)
        result = SmartContractData.convert(result)
        assert len(result) == 8
        
def test_organizers_data_insert():
    db_builder = SqliteBuilder()
    db_builder.buildOrganizers(os.path.join("data", "organizers-data.csv"))
    db = db_builder.getDatabase()
    with db_builder.getDatabase() as db:    
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
