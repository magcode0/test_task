import asyncio
from datetime import datetime
from .data import DataCourse

dc = DataCourse()

async def update_every_day():
    r = await dc.connect_redis()
    date = datetime.now().strftime('%Y-%m-%d')
    
    while True:
        if date == r.get("last_update").decode("utf-8"):
            await asyncio.sleep(1800)
        else:
            await dc.write_redis()

    