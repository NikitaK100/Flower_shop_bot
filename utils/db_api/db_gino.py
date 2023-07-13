from gino import Gino
from data.config import link_gino
from aiogram import Dispatcher
db = Gino()


async def on_startup(dispatcher: Dispatcher):
    print('Подключаюсь к PostgreSql')
    await db.set_bind(link_gino)