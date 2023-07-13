from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_buy_item = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='💳Купить',
                                 callback_data='buy')
        ]
    ]
)

check_payment_keyboard = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='✅Оплатить',
                                 callback_data='everything'),
            InlineKeyboardButton(text='❌Отменить',
                                 callback_data='cancel_transaction')
        ]
    ]
)