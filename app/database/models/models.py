from __future__ import annotations

import json
import csv
import time
import datetime
import re

import asyncio
import datetime
from typing import List
from typing import Any
from typing import Dict

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.types import JSON


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {
        Dict[str, Any]: JSON
    }
    
class Metadatas(Base):
    __tablename__ = "metadatas"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    smart_contract_id: Mapped[int] = mapped_column(ForeignKey("smartContracts.id"))
    data: Mapped[str]
    
class SmartContracts(Base):
    __tablename__ = "smartContracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    organizer_id: Mapped[int] = mapped_column(ForeignKey("organizers.id"))
    
    eventId: Mapped[int]
    collectionName: Mapped[str]
    crowdsale: Mapped[str]
    collection: Mapped[str]
    multisig: Mapped[str]
    startTime: Mapped[int]
    endTime: Mapped[int]
    isPresale: Mapped[bool]
    pricePerToken: Mapped[float]
    maxMintPerUser: Mapped[float]
    saleSize: Mapped[float]
    saleCurrency: Mapped[Dict[str, Any]]
     
    metadataList: Mapped[List[Metadatas]] = relationship()
    
    @staticmethod
    def read(path: str):
        with open(path, 'r') as f:
            f = open(path)
            items = json.load(f)
            data = []
            for item in items:
                metadatas = []
                for metadata in item['smart_contract']["sale_params"]["metadata_list"]:
                    metadatas.append(Metadatas(data=metadata))
                    
                data.append(SmartContracts(
                    eventId = item['event_id'],
                    collectionName = item['collection_name'],
                    crowdsale = item['smart_contract']['crowdsale'],
                    collection = item['smart_contract']['collection'],
                    multisig = item['smart_contract']['multisig'],
                    startTime = item['smart_contract']["sale_params"]["start_time"],
                    endTime = item['smart_contract']["sale_params"]["end_time"],    
                    isPresale = item['smart_contract']["sale_params"]["is_presale"],
                    metadataList = metadatas,                    
                    pricePerToken = item['smart_contract']["sale_params"]["price_per_token"],
                    maxMintPerUser = item['smart_contract']["sale_params"]["max_mint_per_user"],
                    saleSize = item['smart_contract']["sale_params"]["sale_size"],
                    saleCurrency = item['smart_contract']["sale_params"]["sale_currency"],
                    ))
            return data

class LinesUp(Base):
    __tablename__ = "linesUp"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    organizer_id: Mapped[int] = mapped_column(ForeignKey("organizers.id"))
    data: Mapped[str]
    
class Organizers(Base):
    __tablename__ = "organizers"

    id: Mapped[int] = mapped_column(primary_key=True)
    eventTitle: Mapped[str]
    eventStartDate: Mapped[datetime.datetime]
    eventEndDate: Mapped[datetime.datetime]
    nameLocation: Mapped[str]
    addressLocation: Mapped[str]
    totalTicketNumberInteger: Mapped[int]
    maximumTicketsPerUser: Mapped[int]
    saleStartDate: Mapped[str]
    eventImageVideoUrl: Mapped[str | None]
    
    lineUp: Mapped[List[LinesUp]] = relationship()
    ticketCollections: Mapped[List[SmartContracts]] = relationship()
    
    @staticmethod
    def read(path: str):
        with open(path, 'r') as file:
          csvreader = csv.reader(file, delimiter=',')
          organizers = []
          next(csvreader, None)
          for row in csvreader: 
            start_date = datetime.datetime.strptime(row[2],
                                                "%d/%m/%Y %H:%M")
            end_date = datetime.datetime.strptime(row[3],
                                                "%d/%m/%Y %H:%M")
            url = row[10] if re.search("(png|mp4|jpeg)$", row[10]) else None
            id = int(row[0])
            lineUp = []
            if row[9]:
                for item in row[9].split('-'):
                    lineUp.append(LinesUp(organizer_id=id, data=item))
            
            organizers.append(Organizers(
                id = id,
                eventTitle = row[1],
                eventStartDate = start_date,
                eventEndDate = end_date,
                nameLocation = row[4],
                addressLocation = row[5],
                totalTicketNumberInteger = int(row[6]),
                maximumTicketsPerUser = int(row[7]),
                saleStartDate = row[8],
                lineUp = lineUp,
                eventImageVideoUrl = url,
                ))
        return organizers