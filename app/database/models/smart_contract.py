import json
from dataclasses import dataclass

@dataclass
class SmartContractData:
    event_id: int
    collection_name: str
    start_time: int
    end_time: int
    price_per_token: float
    max_mint_per_user: float
    sale_size: float
 
def read_json_data(path: str):
    f = open(path)
    items = json.load(f)
    data = []
    for item in items:
        data.append(SmartContractData(
            event_id = item['event_id'],
            collection_name = item['collection_name'],
            start_time = item['smart_contract']["sale_params"]["start_time"],
            end_time = item['smart_contract']["sale_params"]["end_time"],
            price_per_token = item['smart_contract']["sale_params"]["price_per_token"],
            max_mint_per_user = item['smart_contract']["sale_params"]["max_mint_per_user"],
            sale_size = item['smart_contract']["sale_params"]["sale_size"],
            ))
    return data
    