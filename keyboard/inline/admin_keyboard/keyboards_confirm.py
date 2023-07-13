from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_confirm_add = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Добавить',
                                 callback_data='add'),
            InlineKeyboardButton(text='Отменить',
                                 callback_data='cancel_add')
        ]
    ]
)