from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.admin_keyboard.main_keyboard import main_keyboard_admin
from utils.db_api.schemas import add_product
from loader import dp


@dp.callback_query_handler(text='delete_item')
async def pick_delete_item(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Введите имя товара:')
    await state.set_state('get_name_item')


@dp.message_handler(state='get_name_item')
async def get_name_for_delete(message: types.Message, state: FSMContext):
    name = message.text.title()

    if not await add_product.select_by_text(text=name):
        await message.answer('Такого товара не существует, либо вы не правильно указали наименование товара.',
                             reply_markup=main_keyboard_admin)
        await state.finish()

    if await add_product.select_by_text(text=name):
        await add_product.delete_by_name_product(name=name)
        await message.answer('Товар успешно удалён!',
                             reply_markup=main_keyboard_admin)
        await state.finish()




