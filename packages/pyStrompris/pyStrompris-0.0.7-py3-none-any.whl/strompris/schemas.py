from datetime import datetime
import json
from os import stat

class Periode():
    start_tid: datetime
    slutt_tid: datetime
    
    def __init__(self, start: datetime, slutt: datetime) -> None:
        self.start_tid = start
        self.slutt_tid = slutt


class Prising():
    start: datetime
    slutt: datetime
    NOK_kwh: float
    EUR_kwh: float
    kwh: float # Defaults to NOK
    exr: float # Exchange Rate
    tax: float = 0.0
    total: float = 0.0
    
    def __init__(self, periode: Periode, data: dict) -> None:
        self.start = periode.start_tid
        self.slutt = periode.slutt_tid
        self.NOK_kwh = data['NOK_per_kWh']
        self.EUR_kwh = data['EUR_per_kWh']
        self.kwh = round(self.NOK_kwh, 3)
        self.exr = data['EXR']
    
    def __dict__(self):
        return {
            "start": self.start,
            "slutt": self.slutt,
            "NOK_kwh": self.NOK_kwh,
            "EUR_kwh": self.EUR_kwh,
            "kwh": self.kwh,
            "exr": self.exr,
            "tax": self.tax,
            "total": self.total
        }
        
    def __repr__(self):
        return json.dumps(self.__dict__)

    def __iter__(self):
        yield "start", self.start,
        yield "slutt", self.slutt,
        yield "NOK_kwh", self.NOK_kwh,
        yield "EUR_kwh", self.EUR_kwh,
        yield "kwh", self.kwh,
        yield "exr", self.exr,
        yield "tax", self.tax
        yield "total", self.total