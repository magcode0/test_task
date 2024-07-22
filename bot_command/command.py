from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import html, Router

from course_data import DataCourse

command_router = Router()
dc = DataCourse()

@command_router.message(Command('exchange'))
async def exchange(message: Message):
    text = message.text.split()[1:]
    
    if len(text) == 3:
        symbol1 = text[0].upper()
        symbol2 = text[1].upper()
        cost = float(text[2])
        
        r = await dc.connect_redis()
        get_symbol1 = float(r.get(symbol1))
        resualt = get_symbol1 * cost 
        await message.answer(f'Итого: {html.bold(resualt)} {html.bold(symbol2)}')
        
    else:
        await message.answer(
            'Неправильно сформирован запрос или неправильно указана валюта.'
            '\n\nШаблон запроса: [Валюта с которой нужно конвертировать] [Валюта в которую нужно конвертировать] [Колличество]'
            '\nНапример: /exchange USD RUB 10'
            )
        

@command_router.message(Command('rates'))
async def rates(message: Message):
    r = await dc.connect_redis()
        
    res = ""
    keys = r.keys("*")
    for key in keys:
        if key != b'last_update':
            price = r.get(key)
            res += f"{key.decode('utf-8')}: {price.decode('utf-8'):^5}\n"
            
    await message.answer(html.pre_language(
                        f'Дата: {r.get("last_update").decode("utf-8")}\n'
                        'Валюта Цена\n\n'
                        f'{res}',
                        language='bash'                
    ))