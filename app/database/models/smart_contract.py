import json
from dataclasses import dataclass
from app.database.models.base import BaseData

@dataclass
class SmartContractData(BaseData):
    eventId: int
    collectionName: str
    
    crowdsale: str
    collection: str
    multisig: str
    startTime: int
    endTime: int
    
    isPresale: bool
    metadataList: bytes
    pricePerToken: float
    maxMintPerUser: float
    saleSize: float
    saleCurrency: bytes
 
    @staticmethod
    def read(path: str):
        with open(path, 'r') as f:
            f = open(path)
            items = json.load(f)
            data = []
            for item in items:
                data.append(SmartContractData(
                    eventId = item['event_id'],
                    collectionName = item['collection_name'],
                    crowdsale = item['smart_contract']['crowdsale'],
                    collection = item['smart_contract']['collection'],
                    multisig = item['smart_contract']['multisig'],
                    startTime = item['smart_contract']["sale_params"]["start_time"],
                    endTime = item['smart_contract']["sale_params"]["end_time"],
                    
                    isPresale = item['smart_contract']["sale_params"]["is_presale"],
                    metadataList = json.dumps(item['smart_contract']["sale_params"]["metadata_list"]).encode(),
                    
                    pricePerToken = item['smart_contract']["sale_params"]["price_per_token"],
                    maxMintPerUser = item['smart_contract']["sale_params"]["max_mint_per_user"],
                    saleSize = item['smart_contract']["sale_params"]["sale_size"],
                    saleCurrency = json.dumps(item['smart_contract']["sale_params"]["sale_currency"]).encode(),
                    ))
            return data
        
    @staticmethod
    def convert(l: list):
        data = []
        for t in l:
            data.append(SmartContractData(
                eventId = t[1],
                collectionName = t[2],
                crowdsale = t[3],
                collection = t[4],
                multisig = t[5],
                startTime = t[6],
                endTime = t[7],
                isPresale = t[8],
                metadataList = t[9].decode(),
                pricePerToken = t[10],
                maxMintPerUser = t[11],
                saleSize = t[12],
                saleCurrency = t[13].decode(),   
                ))
        return data
    