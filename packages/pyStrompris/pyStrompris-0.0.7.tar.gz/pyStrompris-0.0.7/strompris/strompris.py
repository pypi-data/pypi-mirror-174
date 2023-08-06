
from datetime import datetime
from typing import Any, Final, List, Optional, final
from .schemas import *
from .common import *
from .PriceSource import *
from .const import *

class Strompris(Common):
    
    priceSource: PriceSource
    
    def __init__(self, source: str, zone: int) -> None:
        if (source is SOURCE_HVAKOSTERSTROMMEN):
            self.priceSource = Hvakosterstrommen(price_zone=zone)
        else:
            raise Exception("Could not find source:",source)
    
    @final
    def showPriceZones(self) -> None:
        print("NO1", "Øst-Norge")
        print("NO2", "Sør-Norge")
        print("NO3", "Midt-Norge")
        print("NO4", "Nord-Norge")
        print("NO5", "Vest-Norge")
        
    def _apply_tax(self, prices:list[Prising]) -> None:
        """Applies tax to items in list."""    
        if (self.priceSource._price_zone != 4):
            """Price Zone NO4 is not subjected to Electricity Tax as of now"""
            for price in prices:
                price.tax = self.getTax(price.kwh) 
                price.total = price.kwh + price.tax
        
    async def async_get_prices_for_today(self) -> list[Prising]:
        today = await self.priceSource.async_fetch_for_today()
        if (today is None):
            return []              
        self._apply_tax(today)
        return today 
    
    async def async_get_prices_for_tomorrow(self) -> list[Prising]:
        try:
            tomorrow = await self.priceSource.async_fetch_for_tomorrow()
            if (tomorrow is None):
                return []
            self._apply_tax(tomorrow)
            return tomorrow   
        except PriceNotAvailable:
            print("Price data is not available for tomorrow")
        return []
        
    async def async_get_available_prices(self) -> list[Prising]:    
        """Fetches prices for today + tomorrow (if available)

        Returns:
            list[Prising]: Prices
        """
        today = await self.async_get_prices_for_today()
        tomorrow = await self.async_get_prices_for_tomorrow()
        return (today + tomorrow)
        
    def get_prices_for_today(self) -> list[Prising]:
        return self.sync(self.async_get_prices_for_today())
    
    def get_prices_for_tomorrow(self) -> list[Prising]:
        return self.sync(self.async_get_prices_for_tomorrow())
    
    def get_available_prices(self) -> list[Prising]:    
        today = self.get_prices_for_today()
        tomorrow = self.get_prices_for_tomorrow()
        return (today + tomorrow)
    
    async def async_get_current_price(self) -> Optional[Prising]:
        if (not self.priceSource._price_today or len(self.priceSource._price_today) == 0):
            await self.async_get_prices_for_today()
        return next((x for x in self.priceSource._price_today if x.start.hour == getNorwayTime().hour), [None])
        
    def get_current_price(self) -> Optional[Prising]:
        return self.sync(self.async_get_current_price())
                
    async def async_get_current_price_attrs(self) -> dict[str, Any]:
        now = await self.async_get_current_price()
        common = Common()
        return {
            "start": now.start.isoformat(),
            "end": now.slutt.isoformat(),
            "kwh": now.kwh,
            "tax": now.tax,
            "total": now.total,
            "max": common.getMax(self.priceSource._price_today),
            "avg": common.getAverage(self.priceSource._price_today),
            "min": common.getMin(self.priceSource._price_today),
            "price_level": common.getPriceLevel(now, self.priceSource._price_today)
        }
    
    async def async_get_price_attrs(self, price: Prising) -> dict[str, Any]:
        common = Common()
        return {
            "start": price.start.isoformat(),
            "end": price.slutt.isoformat(),
            "kwh": price.kwh,
            "tax": price.tax,
            "total": price.total,
            "max": common.getMax(self.priceSource._price_today),
            "avg": common.getAverage(self.priceSource._price_today),
            "min": common.getMin(self.priceSource._price_today),
            "price_level": common.getPriceLevel(price, self.priceSource._price_today)
        }
    
    def get_current_price_attrs(self) -> dict[str, Any]:
        return self.sync(self.async_get_current_price_attrs())
    
    def get_price_attrs(self, price: Prising) -> dict[str, Any]:
        return self.sync(self.async_get_price_attrs(price))
    