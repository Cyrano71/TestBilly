from starlette.testclient import TestClient
from unittest.mock import  ANY, AsyncMock, patch
from app.database.models.models import Organizers, LinesUp, TypeTable
from main import app
import pytest
import datetime

client = TestClient(app)

@patch('app.service.db_service.get_db')
def test_get_all_organizers(mock_get_db):
    mock_db = AsyncMock()
    mock_get_db.return_value = mock_db
    mock_db.select.return_value = [Organizers(id = 1,
      eventTitle = "title",
      eventStartDate = datetime.datetime(2022, 12, 25, 15, 20),
      eventEndDate = datetime.datetime(2022, 12, 25, 17, 35),
      nameLocation = "location",
      addressLocation = "somewhere",
      totalTicketNumberInteger = 50,
      maximumTicketsPerUser = 5,
      saleStartDate = "04/05/2022",
      lineUp = [LinesUp(organizer_id=1, data='test1'), LinesUp(organizer_id=1, data='test2')],
      eventImageVideoUrl = "http://test.png",
      ticketCollections = [])
      ]
    response = client.get('/get_all_organizers/')
    assert response.status_code == 200
    organizers = response.json()["result"]
    assert len(organizers) == 1
    assert organizers[0]["lineUp"] == "test1-test2"
    mock_db.select.assert_called_once_with(TypeTable.Organizers)
    
@patch('app.service.db_service.get_db')
def test_get_organizer_raise_exception_if_not_found(mock_get_db):
    mock_db = AsyncMock()
    mock_get_db.return_value = mock_db
    mock_db.select.return_value = []
    id = -1
    response = client.get(f'/get_organizer/{id}')
    assert response.status_code == 404
    assert response.json()['detail'] == f"No organizer with this id: `{id}` found"
    mock_db.select.assert_called_once_with(TypeTable.Organizers, where_id=id)
    
@patch('app.service.db_service.get_db')
def test_insert_organizer_with_different_url(mock_get_db):
    mock_db = AsyncMock()
    mock_get_db.return_value = mock_db
    id = 999
    mock_db.insert_single.return_value = id
    data =  {
              "eventTitle": "string",
              "eventStartDate": "2023-10-04T12:18:29.030Z",
              "eventEndDate": "2023-10-04T12:18:29.030Z",
              "nameLocation": "string",
              "addressLocation": "string",
              "totalTicketNumberInteger": 0,
              "maximumTicketsPerUser": 0,
              "saleStartDate": "string",
              "eventImageVideoUrl": "",
              "lineUp": [
                "string"
              ]
            }
    data["eventImageVideoUrl"] = "http://wrong.url"
    response = client.post('/create_organizer/', json =data)
    assert response.status_code == 200
    assert response.json() == {"Status": "Success","id": id}
    mock_db.insert_single.assert_called_once_with(ANY)
    assert not mock_db.insert_single.call_args.args[0].eventImageVideoUrl
    
    data["eventImageVideoUrl"] = "http://good.url.png"
    response = client.post('/create_organizer/', json =data)
    assert mock_db.insert_single.call_args.args[0].eventImageVideoUrl == data["eventImageVideoUrl"]
    
@patch('app.service.db_service.get_db')
def test_update_organizer(mock_get_db):
    mock_db = AsyncMock()
    mock_get_db.return_value = mock_db
    mock_db.update.return_value = None
    id = 1
    data = {"eventTitle" : "test"}
    response = client.put(f'/update_organizer/{id}', json=data)
    assert response.status_code == 200
    assert response.json() == {"Status": "Success", "id": id}
    mock_db.update.assert_called_once_with(TypeTable.Organizers, id, data)
    
if __name__ == '__main__':
    test_insert_organizer_with_different_url()