import secrets

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode
from aiogram.utils.markdown import hcode

from keyboard.inline.buy_coins import keyboard_buy_coins
from keyboard.inline.get_referal_code import keyboard_identifier
from loader import dp, bot
from aiogram import types

from utils.db_api.schemas import users_db


@dp.message_handler(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    check_user = await users_db.select_user_by_id(id=user_id)
    message_user = message.text.replace('/start ', '')
    check_referal = await users_db.select_user_by_referal_link(message_user)                                      # /start chich

    if not await users_db.select_user_by_id(id=user_id):                                                          # если id юзера нету в базе тогда проверяем его реферальную ссылку
        if check_referal:                                                                                         # если рефиральная ссылка есть в БД то регистрируем юзера
            create_code = secrets.token_hex(6)                                                                    # генерируем код для новой ссылки юзера
            await users_db.add_item(id=user_id, name=user_name, referal_link=create_code, wallet=0)               # добавляем нового юзера

            owner = await users_db.select_user_by_referal_link(referal_link=message_user)                         # узнаём чья ссылка
            await users_db.update_wallet_by_id(id=owner.id, wallet=owner.wallet + 10)                             # платим ему 10
            owner_wallet = await users_db.select_user_by_referal_link(referal_link=message_user)
            await bot.send_message(chat_id=owner.id,
                                   text=f'Кто то перешёл по вашей ссылке!\n'
                                        f'Вам начисленно 10 бонусных баллов\n\n'
                                        f'Ваш баланс: {str(owner_wallet.wallet)}₽',
                                   reply_markup=keyboard_buy_coins)                                     # сообщили

            user_in_db = await users_db.select_user_by_id(id=user_id)        # отправляем нового юзера в личный кабинет
            await message.answer('Вы зарегистрированы!\n\n'
                                 f'<b>Добро пожаловать</b>\n\n'
                                 f'Ваша реферальная ссылка:\n'
                                 f'https://t.me/test_zikibot?start={create_code}\n\n'
                                 f'Код для приглашения: {create_code}\n'
                                 f'Ваш баланс: {str(user_in_db.wallet)}',
                                 reply_markup=keyboard_buy_coins)

    if await users_db.select_user_by_id(id=user_id):
        user_in_db = await users_db.select_user_by_id(id=user_id)
        try:
            await message.answer(f'<b>Добро пожаловать</b>\n\n'
                                f'Ваша реферальная ссылка:\n'
                                f'https://t.me/test_zikibot?start={check_user.referal_link}\n\n'
                                f'Код для приглашения: {check_user.referal_link}\n\n'
                                f'Ваш баланс: {str(user_in_db.wallet)}₽',
                                 reply_markup=keyboard_buy_coins)
        except AttributeError as err:
            print(f'{err}')
    else:
        await message.answer('<b>Здравствуйте!</b>\n\n'
                             'Меня зовут FlowersStoreBot🌹\n\n'
                             'Чтобы использовать этого бота введите код приглашения\n'
                             'либо пройдите по реферальной ссылке',
                             reply_markup=keyboard_identifier)


@dp.callback_query_handler(text='input_id')
async def where_code(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Введите код приглашения:')
    await state.set_state('get_invite_code')


@dp.message_handler(state='get_invite_code')
async def get_code(message: types.Message, state: FSMContext):
    invite_code = message.text
    if not await users_db.select_user_by_referal_link(invite_code):
        await state.reset_state()
        await message.answer('Такого кода нет в базе данных',
                             reply_markup=keyboard_identifier)

    if await users_db.select_user_by_referal_link(invite_code):
        await message.answer(f"<a href='https://t.me/test_zikibot?start={invite_code}'> Ваша ссылка: </a>\n"
                             f'<pre>https://t.me/test_zikibot?start={invite_code}</pre>')
        await state.finish()







