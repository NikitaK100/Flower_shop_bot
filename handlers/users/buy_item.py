from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from data.config import admins
from keyboard.inline.buy_coins import keyboard_buy_coins
from keyboard.inline.keyboard_buy import keyboard_buy_item, check_payment_keyboard
from loader import dp, bot
from utils.db_api.schemas import add_product, users_db


@dp.message_handler(Command('product'))
async def search_product(message: types.Message, state: FSMContext):
    message_user = message.from_user.id
    if await users_db.select_user_by_id(id=message_user):
        message_text = message.text.replace('/product ', '')
        items = await add_product.select_by_id_product(id_product=message_text)
        await state.update_data({
            'id_product': message_text,
            'product_name': items.name
        })
        await message.answer_photo(photo=items.photo, caption=
                                    f'<b>{items.name}</b>\n\n'
                                    f'<i>{items.description}</i>\n\n'
                                    f'Цена: {items.price}₽',
                                   reply_markup=keyboard_buy_item)
        await state.set_state('button_buy')

    if not await users_db.select_user_by_id(id=message_user):
        return False


@dp.callback_query_handler(text='buy', state='button_buy')
async def pick_buy_button(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer('Укажите кол-во штук:\n\n'
                              'Что бы отменить /cancel')
    await state.set_state('get_quantity')


@dp.message_handler(Command('cancel'), state='get_quantity')
async def cancel_buy(message: types.Message, state: FSMContext):
    user_name = message.from_user.id
    user_db = await users_db.select_user_by_id(id=user_name)
    await state.reset_state()
    await message.answer('Вы отменили это действие!\n\n'
                         f'<b>Добро пожаловать</b>\n\n'
                         f'Ваша реферальная ссылка:\n'
                         f'<pre>https://t.me/test_zikibot?start={user_db.referal_link}</pre>\n\n'
                         f'Код для приглашения: {user_db.referal_link}\n'
                         f'Ваш баланс: {str(user_db.wallet)}₽',
                         reply_markup=keyboard_buy_coins)


@dp.message_handler(state='get_quantity')
async def quantity(message: types.Message, state: FSMContext):
    quantity = int(message.text)
    await state.update_data(
        {
            'quantity': quantity
        }
    )
    await message.answer('Укажите адрес доставки и ваш номер телефона:\n\n'
                         'Учтите, что доставка производится только по Москве и Московской области.\n'
                         'Доставка уже включена в стоимость')
    await state.set_state('get_address')


@dp.message_handler(state='get_address')
async def buy_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id_product = data.get('id_product')
    items_db = await add_product.select_by_id_product(id_product=id_product)
    user_db = await users_db.select_user_by_id(id=message.from_user.id)
    quantity = data.get('quantity')
    address = message.text
    await state.update_data(
        {
            'address': address
        }
    )

    if quantity == 0:
        await state.reset_state()
        await message.edit_text('Вы отменили это действие!\n\n'
                             f'<b>Добро пожаловать</b>\n\n'
                             f'Ваша реферальная ссылка:\n'
                             f'<pre>https://t.me/test_zikibot?start={user_db.referal_link}</pre>\n\n'
                             f'Код для приглашения: {user_db.referal_link}\n'
                             f'Ваш баланс: {str(user_db.wallet)}₽',
                             reply_markup=keyboard_buy_coins)

    if quantity >= 1:
        await message.answer(f'К оплате {items_db.price * quantity + 200}₽\n'
                             f'Сумма с учётом доставки\n\n'
                             f'<b>{items_db.name}</b>\n\n'
                             f'Кол_во: {quantity}\n\n'
                             f'Адрес:\n'
                             f'{address}',
                             reply_markup=check_payment_keyboard)

        await state.set_state('check_buy')


@dp.callback_query_handler(text='everything', state='check_buy')
async def check_payment(call: types.CallbackQuery, state: FSMContext):
    user_db = await users_db.select_user_by_id(id=call.from_user.id)
    data = await state.get_data()
    id_product = data.get('id_product')
    item_db = await add_product.select_by_id_product(id_product=id_product)
    member = call.from_user
    await call.answer(cache_time=1)
    data = await state.get_data()
    quantity = data.get('quantity')
    if user_db.wallet < item_db.price * quantity + 200:
        await state.reset_state()
        await call.message.edit_reply_markup()
        await call.message.answer('На вашем счету не достаточно средств',
                                  reply_markup=keyboard_buy_coins)
    if user_db.wallet >= item_db.price + 200:

        await users_db.update_wallet_by_id(id=call.from_user.id, wallet=user_db.wallet - (item_db.price * quantity + 200))
        await bot.send_message(admins, text='❗️Поступил заказ❗️\n\n'
                                            f'Товар: <b>{data.get("product_name")}</b>\n\n'
                                            f'Кол-во: {data.get("quantity")}\n\n'
                                            f'Адрес доставки и телефон:\n'
                                            f'{data.get("address")}\n\n'
                                            f'Заказал: {member.get_mention(as_html=True)}')
        await call.message.answer('📌Всё прошло успешно!📌\n\n'
                                  'С вами скоро свяжется наш менеджер\n\n'
                                  'Телефон техподдержки: +7(123)123-12-12')
        await state.finish()


@dp.callback_query_handler(text='cancel_transaction', state='check_buy')
async def cancel_transaction(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user_db = await users_db.select_user_by_id(call.from_user.id)
    await state.reset_state()
    await call.message.edit_text('Вы отменили это действие!\n\n'
                                f'<b>Добро пожаловать</b>\n\n'
                                f'Ваша реферальная ссылка:\n'
                                f'<pre>https://t.me/test_zikibot?start={user_db.referal_link}</pre>\n\n'
                                f'Код для приглашения: {user_db.referal_link}\n'
                                f'Ваш баланс: {str(user_db.wallet)}₽',
                                reply_markup=keyboard_buy_coins)