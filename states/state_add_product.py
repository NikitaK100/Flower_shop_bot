from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateProduct(StatesGroup):
    get_name = State()
    get_description = State()
    get_photo = State()
    get_price = State()
    confirm_product = State()