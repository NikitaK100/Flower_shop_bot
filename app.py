from aiogram import executor
from loader import db, dp


async def on_startup(dp):
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    from utils.db_api.db_gino import on_startup
    create_tables = on_startup(dp)
    print('Подключаюсь к БД')
    await create_tables
    print('Создаю таблицы')
    await db.gino.create_all()


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
