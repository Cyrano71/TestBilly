import pytest
import os
import asyncio
from app.database.builder import SqliteBuilder
from app.database.models.organizers import OrganizersData
from app.database.models.smart_contract import SmartContractData

@pytest.mark.asyncio
async def test_smart_contract_data_insert():
    db_builder = SqliteBuilder()
    await db_builder.build_database()
    await db_builder.build_smart_contract(os.path.join("data", "smart-contracts-data.json"))
    db = await db_builder.get_database()
    sql = """
        select *, GROUP_CONCAT(metadata, ',') as metadataList from
        (
        select * from smartContract left join metadatas on smartContract.id = metadatas.smartContractId
        ) sub
        Group By sub.id
        """
    result = await db.exec_query(sql)
    result = SmartContractData.convert(result)
    assert len(result) == 8

@pytest.mark.asyncio      
async def test_organizers_data_insert():
    db_builder = SqliteBuilder()
    await db_builder.build_database()
    await db_builder.build_organizers(os.path.join("data", "organizers-data.csv"))
    db = await db_builder.get_database()
    sql = """
            select *, GROUP_CONCAT(name, '-') as lineUp from
            (
            select * from organizers left join linesUp on organizers.id = linesUp.organizersId
            ) sub
            Group By sub.id
            """
    result = await db.exec_query(sql)
    result = OrganizersData.convert(result)
    assert len(result) == 5

if __name__ == '__main__':
    os.chdir('../')
    import nest_asyncio
    nest_asyncio.apply()
    async def main():
        await test_smart_contract_data_insert()
        await test_organizers_data_insert()
    asyncio.run(main())
