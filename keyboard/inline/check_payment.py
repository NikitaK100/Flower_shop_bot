from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_payment_coins = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='✅Оплатил',
                                 callback_data='end_payment'),
            InlineKeyboardButton(text='❌Отменить',
                                 callback_data='cancellation')
        ]
    ]
)