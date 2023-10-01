from pydantic import BaseModel

class SmartContractPutRequest(BaseModel):
    eventId: int | None = None
    collectionName: str | None = None
    crowdsale: str | None = None
    collection: str | None = None
    multisig: str | None = None
    startTime: int | None = None
    endTime: int | None = None
    isPresale: bool | None = None
    pricePerToken: float | None = None
    maxMintPerUser: float | None = None
    saleSize: float | None = None
    saleCurrency: dict | None = None