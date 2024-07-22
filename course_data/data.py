import aiohttp
import xml.etree.ElementTree as ET
import redis
import asyncio
from datetime import datetime


class DataCourse:
    
    
    def __init__(self) -> None:
        self._url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    
    
    async def _get_url(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f'[INFO] Ошибка получения данных. Попробуйте позже. Код запроса: {response.status}')
        
    
    async def _data_xml(self):
        get = await self._get_url()
        root = ET.fromstring(get)
        return root
    
    
    async def connect_redis(self):
        return redis.Redis(host="localhost", port=6379, db=0)
        
        
    async def write_redis(self):
        data = await self._data_xml()
        r = await self.connect_redis()
        
        for valute in data.findall("Valute"):
            ticker = valute.find('CharCode').text.strip()
            price = float(valute.find('Value').text.strip().replace(',', '.'))
            r.set(ticker, price)

        r.set('last_update', datetime.now().strftime('%Y-%m-%d'))
        print('[INFO] Данные добавлены!')
        
    
            