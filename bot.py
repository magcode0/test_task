from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import asyncio
import logging
import sys

from config import Config
from course_data import DataCourse


bot = Bot(token=Config.API_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dc = DataCourse()


async def main():
    from bot_command import command_router
    from course_data import update_every_day
    
    try:
        dp.include_routers(
            command_router,
        )
        
        await dc.write_redis()
        
        loop = asyncio.get_event_loop()
        loop.create_task(update_every_day())
        await dp.start_polling(bot)
        
    finally:
        await bot.session.close()
    
    
if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
        
        
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')