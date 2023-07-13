from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.db_api.schemas import users_db


@dp.callback_query_handler(text='add_user')
async def add_new(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Отправьте ключ который будет присвоен юзеру(ENG)')
    await state.set_state('add_new_user')


@dp.message_handler(state='add_new_user')
async def input_data(message: types.Message, state: FSMContext):
    data = message.text
    await users_db.add_item(id=message.from_user.id, name=message.from_user.full_name,
                            referal_link=data, wallet=1000)
    owner = await users_db.select_user_by_referal_link(referal_link=message.text)
    print(owner.id)
    await state.finish()
