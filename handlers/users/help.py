from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from keyboard.inline.keyboard_back_menu import keyboard_back
from utils.db_api.schemas import users_db
from keyboard.inline.buy_coins import keyboard_buy_coins
from keyboard.inline.get_referal_code import keyboard_identifier


@dp.callback_query_handler(text='how_works')
async def how_works(call: types.CallbackQuery): 
    await call.answer()
    await call.message.edit_text('<b>INFO</b>\n\n'
                             '🔑<i>Как начать работать с ботом?</i>\n\n'
                             'Что бы использовать данного бота нужно перейти по реферально ссылке,'
                             'либо ввести в боте код приглашения.\n\n'
                             '🔎<i>Как искать товары?</i>\n\n'
                             'Достаточно ввести @test_zikibot, и вы увидите весь список товаров\n', 
                             reply_markup=keyboard_back)


@dp.callback_query_handler(text='back')
async def back_menu(call: types.CallbackQuery): 
    user_id = call.from_user.id
    check_user = await users_db.select_user_by_id(id=user_id)

    if await users_db.select_user_by_id(id=user_id):
        user_in_db = await users_db.select_user_by_id(id=user_id)
        try:
            await call.message.edit_text(f'<b>Добро пожаловать</b>\n\n'
                                f'Ваша реферальная ссылка:\n'
                                f'https://t.me/test_zikibot?start={check_user.referal_link}\n\n'
                                f'Код для приглашения: {check_user.referal_link}\n\n'
                                f'Ваш баланс: {str(user_in_db.wallet)}₽',
                                 reply_markup=keyboard_buy_coins)
        except AttributeError as err:
            print(f'{err}')
    else:
        await call.message.edit_text('<b>Здравствуйте!</b>\n\n'
                             'Меня зовут FlowersStoreBot🌹\n\n'
                             'Чтобы использовать этого бота введите код приглашения\n'
                             'либо пройдите по реферальной ссылке',
                             reply_markup=keyboard_identifier)