from enum import Enum
import pytest

#11:46:48
#13:28:31

#14:16
#16:40

class OPERATORS(Enum):
    AND = 0
    OR = 1

operators = {
    OPERATORS.AND: lambda a,b : a & b,
    OPERATORS.OR: lambda a,b : a | b
}

class RESTRICTIONS(Enum):
    Date = "date"
    Meteo = "meteo"
    Level = "level"
    Or = "or"
    And = "and"

restrictions = {
    RESTRICTIONS.Date: lambda a, _ : check_range_date(a[f"@{RESTRICTIONS.Date.value}"]),
    RESTRICTIONS.Meteo: lambda a, b : check_meteo(a[f"@{RESTRICTIONS.Meteo.value}"], b[RESTRICTIONS.Meteo.value]),
    RESTRICTIONS.Level: lambda a, b : check_range_value(a[f"@{RESTRICTIONS.Level.value}"], b[RESTRICTIONS.Level.value]),
    RESTRICTIONS.Or: lambda a, b : apply_restrictions(a[f"@{RESTRICTIONS.Or.value}"], b, OPERATORS.OR),
    RESTRICTIONS.And: lambda a, b : apply_restrictions(a[f"@{RESTRICTIONS.And.value}"], b, OPERATORS.AND),
}

def apply_restrictions(items, arguments, operator: OPERATORS = OPERATORS.AND):
    result = True if operator == OPERATORS.AND else False
    """
     operation = lambda a,b : a & b if operator == OPERATORS.AND else lambda a,b : a | b
    print(items)
    print(operator)
    print(arguments)
    """
    for item in items:
        for restriction in restrictions:
            if f"@{restriction.value}" in item:
                result = operators[operator](result, restrictions[restriction](item, arguments))
                break
        """
        if "@date" in item:
            result = operators[operator](result, check_range_date(item))
        elif "@meteo" in item:
            result = operators[operator](result, check_meteo(item)) 
        elif "@level" in item:
            result = operators[operator](result, check_level(item)) 
        elif "@or" in item:
            result = operators[operator](result, apply_restrictions(OPERATORS.OR, item["@or"]))
        elif "@and" in item:
            result = operators[operator](result, apply_restrictions(OPERATORS.AND, item["@and"]))
        else:
            raise Exception(f"unknown restriction {item}")
        """
        
    return result

from datetime import datetime

def check_range_date(range):
    print("check_range_date", range)
    now = datetime.now()
    after = datetime.strptime(range['after'], '%Y-%m-%d')
    before  = datetime.strptime(range['before'], '%Y-%m-%d')
    print(after)
    print(before)
    return now <= before and now >= after

def check_meteo(conditions, town):
    print("check_meteo", conditions, town)
    api = WeatherApi("test")
    weather = api.get_current_weather("1", "2")
    value =  weather["data"]["current"]["temp"]
    required = conditions["temp"]
    return check_range_value(required,value)

class RANGE_VALUE_OPERATIONS(Enum):
    EQUAL = "eq"
    LESS_THAN = "lt"
    GREATER_THAN = "gt"

def check_range_value(required, value):
    print("check_range_value", required, value)
    if RANGE_VALUE_OPERATIONS.EQUAL.value in required:
        return value == float(required[RANGE_VALUE_OPERATIONS.EQUAL.value])
    result = True
    if RANGE_VALUE_OPERATIONS.LESS_THAN.value in required:
        result &= value < float(required[RANGE_VALUE_OPERATIONS.LESS_THAN.value])
    if RANGE_VALUE_OPERATIONS.GREATER_THAN.value in required:
        result &= value > float(required[RANGE_VALUE_OPERATIONS.GREATER_THAN.value])
    return result

FAKE_TIME = datetime(2024, 3, 22)

@pytest.fixture
def patch_datetime_now(monkeypatch):

    class mydatetime(datetime):
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, 'datetime', mydatetime)

def test_should_return_false_if_date_not_in_range():
    data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-15" } }]
    arguments = {}
    assert apply_restrictions(data, arguments) == False

def test_should_return_true_if_date_in_range():
    data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }]
    arguments = {}
    assert apply_restrictions(data, arguments) == True

def test_should_return_false_if_not_eq_level():
    data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@level": { "eq": 40 } }]
    arguments = { "level": 25 }
    assert apply_restrictions(data, arguments) == False

def test_should_return_true_if_eq_level():
    data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@level": { "eq": 25 } }]
    arguments = { "level": 25 }
    assert apply_restrictions(data, arguments) == True

def test_should_return_false_if_not_lt_level():
    data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@level": { "lt": 40 } }]
    arguments = { "level": 50 }
    assert apply_restrictions(data, arguments) == False

def test_should_return_true_if_lt_level():
    data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@level": { "lt": 40 } }]
    arguments = { "level": 30 }
    assert apply_restrictions(data, arguments) == True

def test_should_return_false_if_not_gt_lt_level():
    data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@level": { "gt": 20, "lt": 40 } }]
    arguments = { "level": 50 }
    assert apply_restrictions(data, arguments) == False

def test_should_return_true_if_gt_lt_level():
    data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@level": { "gt": 20, "lt": 40 } }]
    arguments = { "level": 30 }
    assert apply_restrictions(data, arguments) == True

def test_should_return_false_if_and_and_one_is_false():
    data = [ { "@and": [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@level": { "lt": 30, "gt": 15 } } ] }]
    arguments = { "level": 10 }
    assert apply_restrictions(data, arguments, OPERATORS.AND) == False

def test_should_return_true_if_and_and_both_are_true():
    data = [ { "@and": [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@level": { "lt": 30, "gt": 15 } } ] }]
    arguments = { "level": 20 }
    assert apply_restrictions(data, arguments, OPERATORS.AND) == True

def test_should_return_true_if_or_and_one_is_true():
    data = [ { "@or": [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@level": { "lt": 30, "gt": 15 } } ] }]
    arguments = { "level": 10 }
    assert apply_restrictions(data, arguments, OPERATORS.OR) == True

def test_should_return_false_if_or_and_both_are_false():
    data = [ { "@or": [ { "@date": { "after": "2024-01-18", "before": "2024-03-21" } }, { "@level": { "lt": 30, "gt": 15 } } ] }]
    arguments = { "level": 10 }
    assert apply_restrictions(data, arguments, OPERATORS.OR) == False

import requests

class GeocodingApi:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        #https://openweathermap.org/api/geocoding-api
        self.base_url = "http://api.openweathermap.org/geo/1.0/"
        self.session = requests.Session()

    def get_geocoding(self, town):
        response = self.session.get(self.base_url + f"direct?q={town}&limit=5&appid={self.api_key}")
        try:
            data = response.json()
        except Exception:
            raise Exception(f"Failed fetching geocoding : {response.text}")
        return data

#api = GeocodingApi("6da1f36812c612a185fc90019e2f2522")
#api.get_geocoding("Chambon")
        
class WeatherApi:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        #https://openweathermap.org/current
        self.base_url = "https://api.openweathermap.org/data/2.5/"
        self.session = requests.Session()

    def get_current_weather(self, lat, lon):
        response = self.session.get(self.base_url + f"weather?lat={lat}&lon={lon}&appid={self.api_key}")
        try:
            data = response.json()
        except Exception:
            raise Exception(f"Failed fetching weather : {response.text}")
        return data
        
#api = WeatherApi("6da1f36812c612a185fc90019e2f2522")
#api.get_current_weather(44.34, 10.99)

from unittest import mock
        
@mock.patch.object(requests.Session, 'get')
def test_fetch_geocoding(mockget):
    mockresponse = mock.Mock()
    mockget.return_value = mockresponse
    lat = 51.5156177
    lon = -0.0919983
    mockresponse.json = lambda : {"data": [ {
      "name":"City of London",
      "local_names":{
         "es":"City de Londres",
      },
      "lat":lat,
      "lon":lon,
      "country":"GB",
      "state":"England"
   }]}

    api = GeocodingApi("test")
    response = api.get_geocoding("London")
    mockget.assert_called_once_with('http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid=test')
    assert len(response["data"]) == 1
    assert response["data"][0]["lat"] == lat
    assert response["data"][0]["lon"] == lon

@mock.patch.object(requests.Session, 'get')
def test_should_return_false_if_weather_less_than_required(mockget):
    mockresponse = mock.Mock()
    mockget.return_value = mockresponse
    mockresponse.json = lambda : {"data": {
            "lat":33.44,
            "lon":-94.04,
            "timezone":"America/Chicago",
            "timezone_offset":-18000,
            "current":{
                "dt":1684929490,
                "sunrise":1684926645,
                "sunset":1684977332,
                "temp":292.55,
                "feels_like":292.87,
                "pressure":1014,
                "humidity":89,
                "dew_point":290.69,
                "uvi":0.16,
                "clouds":53,
                "visibility":10000,
                "wind_speed":3.13,
                "wind_deg":93,
                "wind_gust":6.71
                }
            }
    }
    data = [ { "@meteo": { "is": "clear", "temp": { "lt": "15" } } } ]
    arguments = {"meteo": { "town": "Chambon" }}
    assert apply_restrictions(data, arguments) == False

@mock.patch.object(requests.Session, 'get')
def test_should_return_true_if_weather_temp_greater_than_required(mockget):
    mockresponse = mock.Mock()
    mockget.return_value = mockresponse
    mockresponse.json = lambda : {"data": {
            "lat":33.44,
            "lon":-94.04,
            "timezone":"America/Chicago",
            "timezone_offset":-18000,
            "current":{
                "dt":1684929490,
                "sunrise":1684926645,
                "sunset":1684977332,
                "temp":292.55,
                "feels_like":292.87,
                "pressure":1014,
                "humidity":89,
                "dew_point":290.69,
                "uvi":0.16,
                "clouds":53,
                "visibility":10000,
                "wind_speed":3.13,
                "wind_deg":93,
                "wind_gust":6.71
                }
            }
    }
    data = [ { "@meteo": { "is": "clear", "temp": { "gt": "15" } } } ]
    arguments = {"meteo": { "town": "Chambon" }}
    assert apply_restrictions(data, arguments) == True

@mock.patch.object(requests.Session, 'get')
def test_should_return_true_if_tree_is_good(mockget):
    mockresponse = mock.Mock()
    mockget.return_value = mockresponse
    mockresponse.json = lambda : {"data": {
            "lat":33.44,
            "lon":-94.04,
            "timezone":"America/Chicago",
            "timezone_offset":-18000,
            "current":{
                "dt":1684929490,
                "sunrise":1684926645,
                "sunset":1684977332,
                "temp": 292.55,
                "feels_like":292.87,
                "pressure":1014,
                "humidity":89,
                "dew_point":290.69,
                "uvi":0.16,
                "clouds":53,
                "visibility":10000,
                "wind_speed":3.13,
                "wind_deg":93,
                "wind_gust":6.71
                }
            }
    }
    data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@or": [ { "@level": { "eq": 40 } }, { "@and": [ { "@level": { "lt": 30, "gt": 15 } }, { "@meteo": { "is": "clear", "temp": { "gt": "15" } } } ] } ] } ]
    arguments = { "level": 25, "meteo": { "town": "Chambon" } }
    assert apply_restrictions(data, arguments) == True

@mock.patch.object(requests.Session, 'get')
def test_should_return_false_if_tree_is_false(mockget):
    mockresponse = mock.Mock()
    mockget.return_value = mockresponse
    mockresponse.json = lambda : {"data": {
            "lat":33.44,
            "lon":-94.04,
            "timezone":"America/Chicago",
            "timezone_offset":-18000,
            "current":{
                "dt":1684929490,
                "sunrise":1684926645,
                "sunset":1684977332,
                "temp": 0,
                "feels_like":292.87,
                "pressure":1014,
                "humidity":89,
                "dew_point":290.69,
                "uvi":0.16,
                "clouds":53,
                "visibility":10000,
                "wind_speed":3.13,
                "wind_deg":93,
                "wind_gust":6.71
                }
            }
    }
    data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@or": [ { "@level": { "eq": 40 } }, { "@and": [ { "@level": { "lt": 30, "gt": 15 } }, { "@meteo": { "is": "clear", "temp": { "gt": "15" } } } ] } ] } ]
    arguments = { "level": 25, "meteo": { "town": "Chambon" } }
    assert apply_restrictions(data, arguments) == False

"""
if __name__ == '__main__':
 
      data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-15" } }, { "@or": [ { "@level": { "eq": 40 } }, { "@and": [ { "@level": { "lt": 30, "gt": 15 } }, { "@meteo": { "is": "clear", "temp": { "gt": "15" } } } ] } ] } ]
    arguments = { "level": 25, "meteo": { "town": "Chambon" } }
    print("result : ", apply_restrictions(OPERATORS.AND, data, arguments))  
"""