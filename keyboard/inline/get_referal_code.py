from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_identifier = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='✏️Ввести индентификатор',
                                 callback_data='input_id')
        ], 
        [
            InlineKeyboardButton(text='Как использовать?',
                                callback_data='how_works')
        ]
    ]
)