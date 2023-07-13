from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink, hcode

from data import config
from keyboard.inline.check_payment import check_payment_coins
from keyboard.inline.buy_coins import keyboard_buy_coins
from loader import dp
# from utils.misc.qiwi import Payment, NotPaymentFound, NotEnoughMoney

from utils.db_api.schemas import users_db


@dp.callback_query_handler(text='buy_coins')
async def top_up_your_wallet(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state('get_quantity_coins')
    await call.message.edit_text('На какую сумму вы хотите пополнить кошелёк?\n'
                              'P.S.Отправьте число\n\n'
                              '/cancel_operation')


@dp.message_handler(Command('cancel_operation'), state='get_quantity_coins')
async def cancel_operation(message: types.Message, state: FSMContext):
    await state.reset_state()
    user_name = message.from_user.id
    user_db = await users_db.select_user_by_id(id=user_name)
    await message.answer('Вы отменили это действие!\n\n'
                         f'<b>Добро пожаловать</b>\n\n'
                         f'Ваша реферальная ссылка:\n'
                         f'<pre>https://t.me/test_zikibot?start={user_db.referal_link}</pre>\n\n'
                         f'Код для приглашения: {user_db.referal_link}\n'
                         f'Ваш баланс: {str(user_db.wallet)}',
                         reply_markup=keyboard_buy_coins)


@dp.message_handler(state='get_quantity_coins')
async def get_quantity_coins(message: types.Message, state: FSMContext):
    quantity = int(message.text)
    payment = Payment(amount=quantity)
    payment.create()
    await state.update_data(
        {
            'payment': payment,
            'coins': quantity
        }
    )
    await message.answer('\n'.join(
        [f"Сумма платежа составляет {quantity} RUB",
         '',
         "Оплатите по номеру телефона или по адресу",
         hlink(config.qiwi_number, url=payment.invoice),
         'Обязательно платите по ID платежа',
         hcode(payment.id)]), reply_markup=check_payment_coins)
    await state.set_state('ending_payment')


@dp.callback_query_handler(state='ending_payment', text='cancellation')
async def cancel_check_payment(call: types.CallbackQuery, state: FSMContext):
    user_name = call.from_user.id
    user_db = await users_db.select_user_by_id(id=user_name)
    await call.answer()
    await call.message.edit_text('Вы отменили это действие!\n\n'
                                 f'<b>Добро пожаловать</b>\n\n'
                                 f'Ваша реферальная ссылка:\n'
                                 f'<pre>https://t.me/test_zikibot?start={user_db.referal_link}</pre>\n\n'
                                 f'Код для приглашения: {user_db.referal_link}\n'
                                 f'Ваш баланс: {str(user_db.wallet)}₽',
                                 reply_markup=keyboard_buy_coins)
    await state.finish()


@dp.callback_query_handler(state='ending_payment', text='end_payment')
async def end_payment(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    user_id = call.from_user.id
    user_db = await users_db.select_user_by_id(id=user_id)
    payment: Payment = data.get('payment')
    try:
        payment.check_payment()
    except NotPaymentFound:
        await call.message.answer('Транзакция не найдена')
        return
    except NotEnoughMoney:
        await call.message.answer('Оплаченная сумма меньше необходимой')
        return
    else:
        await users_db.update_wallet_by_id(id=user_id, wallet=data.get('coins') + user_db.wallet)
        await call.message.answer('Вы успешно пополнили счёт!\n\n'
                                  f'<b>Добро пожаловать</b>\n\n'
                                  f'Ваша реферальная ссылка:\n'
                                  f'<pre>https://t.me/test_zikibot?start={user_db.referal_link}</pre>\n\n'
                                  f'Код для приглашения: {user_db.referal_link}\n'
                                  f'Ваш баланс: {user_db.wallet + data.get("coins")}₽',
                                  reply_markup=keyboard_buy_coins)
        await state.finish()







