from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard_admin = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='➕ Добавить товар',
                                 callback_data='add_item')
        ],
        [
            InlineKeyboardButton(text='➖ Удалить товар',
                                 callback_data='delete_item')
        ],
        [
            InlineKeyboardButton(text='Добавить пользователя',
                                 callback_data='add_user')
        ]
    ]
)