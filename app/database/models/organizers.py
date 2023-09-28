import json
import csv
from dataclasses import dataclass
import time
import datetime
import re
from app.database.models.base import BaseData

@dataclass
class OrganizersData(BaseData):
    id: int
    eventTitle: str
    eventStartDate: int
    eventEndDate: int
    nameLocation: str
    addressLocation: str
    totalTicketNumberInteger: int
    maximumTicketsPerUser: int
    saleStartDate: str
    lineUp: bytes
    eventImageVideoUrl: str
 
    @staticmethod
    def read(path: str):
        with open(path, 'r') as file:
          csvreader = csv.reader(file, delimiter=',')
          data = []
          next(csvreader, None)
          for row in csvreader: 
            start_date = int(time.mktime(datetime.datetime.strptime(row[2],
                                                "%d/%m/%Y %H:%M").timetuple()))
            end_date = int(time.mktime(datetime.datetime.strptime(row[3],
                                                "%d/%m/%Y %H:%M").timetuple()))
            url = None
            match = re.search("(png|mp4|jpeg)$", row[10])
            if match:
                url = row[10]
            data.append(OrganizersData(
                id = int(row[0]),
                eventTitle = row[1],
                eventStartDate = start_date,
                eventEndDate = end_date,
                nameLocation = row[4],
                addressLocation = row[5],
                totalTicketNumberInteger = int(row[6]),
                maximumTicketsPerUser = int(row[7]),
                saleStartDate = row[8],
                lineUp = row[9].encode(),
                eventImageVideoUrl = url,
                ))
        return data

    @staticmethod
    def convert(l: list):
        data = []
        for t in l:
            data.append(OrganizersData(
                id = t[0],
                eventTitle = t[1],
                eventStartDate = datetime.datetime.fromtimestamp(t[2]).strftime("%d/%m/%Y %H:%M"),
                eventEndDate = datetime.datetime.fromtimestamp(t[3]).strftime("%d/%m/%Y %H:%M"),
                nameLocation = t[4],
                addressLocation = t[5],
                totalTicketNumberInteger = t[6],
                maximumTicketsPerUser = t[7],
                saleStartDate = t[8],
                lineUp = t[9].decode(),
                eventImageVideoUrl = t[10],
                ))
        return data
    