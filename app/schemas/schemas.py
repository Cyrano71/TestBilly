from pydantic import BaseModel
import datetime

class SmartContractDataRequest(BaseModel):
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
    metadataList: list  | None = None
    
class SmartContractGetRequest(BaseModel):
    id: int
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
    metadataList: list  | None = None
    
class OrganizersDataRequest(BaseModel):
    eventTitle: str | None = None
    eventStartDate: datetime.datetime | None = None
    eventEndDate: datetime.datetime | None = None
    nameLocation: str | None = None
    addressLocation: str | None = None
    totalTicketNumberInteger: int | None = None
    maximumTicketsPerUser: int | None = None
    saleStartDate: str | None = None
    eventImageVideoUrl: str | None = None
    lineUp: list | None = None
    
class OrganizersGetRequest(BaseModel):
    id: int
    eventTitle: str | None = None
    eventStartDate: datetime.datetime | None = None
    eventEndDate: datetime.datetime | None = None
    nameLocation: str | None = None
    addressLocation: str | None = None
    totalTicketNumberInteger: int | None = None
    maximumTicketsPerUser: int | None = None
    saleStartDate: str | None = None
    eventImageVideoUrl: str | None = None
    lineUp: str | None = None
    ticketCollections: list  | None = None
    
