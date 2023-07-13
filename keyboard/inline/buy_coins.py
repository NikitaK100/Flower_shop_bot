from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_buy_coins  = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='💵Пополнить',
                                 callback_data='buy_coins'
            )
        ], 
        [
            InlineKeyboardButton(text='Как использовать?',
                                 callback_data='how_works')
        ]
    ]
)