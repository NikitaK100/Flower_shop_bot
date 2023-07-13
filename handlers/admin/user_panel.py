from random import randint

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import admins
from handlers import admin
from keyboard.inline.admin_keyboard.keyboards_confirm import keyboard_confirm_add
from loader import dp

from keyboard.inline.admin_keyboard.main_keyboard import main_keyboard_admin

from states.state_add_product import CreateProduct

from utils.db_api.schemas import add_product as add_product_db


@dp.message_handler(commands='cancel', user_id=admins, state=CreateProduct)
async def slash_cancel(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Действие отменено!\n\n'
                         '-------------------------\n'
                         f'Добро пожаловать {message.from_user.username}\n\n'
                         f'Вы находитесь в админ панеле,\n'
                         f'выберите одно из действий ниже',
                         reply_markup=main_keyboard_admin)


@dp.message_handler(Command('admin'), user_id=admins)
async def start_admin_panel(message: types.Message):
    await message.answer(f'Добро пожаловать {message.from_user.username}\n\n'
                         f'Вы находитесь в админ панеле,\n'
                         f'выберите одно из действий ниже',
                         reply_markup=main_keyboard_admin)


@dp.callback_query_handler(text='add_item')
async def add_product(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer('Как будет называться ваш товар?\n\n'
                              'Если хотите отменить: /cancel')
    await state.set_state(CreateProduct.get_name)


@dp.message_handler(state=CreateProduct.get_name)
async def get_name_item(message: types.Message, state: FSMContext):
    name = message.text.title()
    await state.update_data(
        {
            'name': name
        }
    )
    await message.answer('Опишите ваш товар:')
    await state.set_state(CreateProduct.get_description)


@dp.message_handler(state=CreateProduct.get_description)
async def get_discription(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(
        {
            'description': description
        }
    )
    await message.answer('Пришлите мне ссылку на фотографию товара:')
    await state.set_state(CreateProduct.get_photo)


@dp.message_handler(state=CreateProduct.get_photo)
async def get_photo(message: types.Message, state: FSMContext):
    photo = message.text
    await state.update_data(
        {
            'photo': photo,
        }
    )
    await message.answer('Укажите цену на ваш товар:')
    await state.set_state(CreateProduct.get_price)


@dp.message_handler(state=CreateProduct.get_price)
async def get_price(message: types.Message, state: FSMContext):
    price = message.text
    data = await state.get_data()
    name = data.get('name')
    description = data.get('description')
    photo = data.get('photo')
    id_product = randint(1000, 10000)
    await state.update_data(
        {
            'id_product': str(id_product),
            'price': price
        }
    )
    await message.answer_photo(photo=photo, caption=
                               f'id_product: {id_product}\n\n'
                               f'<b>{name}</b>\n\n'
                               f'<i>{description}</i>\n\n'
                               f'Цена: {price}₽',
                               reply_markup=keyboard_confirm_add)
    await state.set_state(CreateProduct.confirm_product)


@dp.callback_query_handler(text='add', state=CreateProduct.confirm_product)
async def confirm_add(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    name = data.get('name')
    description = data.get('description')
    photo = data.get('photo')
    id_product = data.get('id_product')
    price = data.get('price')
    await add_product_db.add_item(name=name, description=description,
                                  photo=photo, id_product=id_product, price=int(price))
    await call.message.answer('☑️Продукт успешно добавлен в список товаров!\n\n'
                              '-------------------------\n'
                              f'Добро пожаловать {call.from_user.username}\n\n'
                              f'Вы находитесь в админ панеле,\n'
                              f'выберите одно из действий ниже',
                              reply_markup=main_keyboard_admin)
    await state.finish()

#--------------------------------------------------------------------------------------------------------------------


@dp.callback_query_handler(text='cancel_add', state=CreateProduct.confirm_product)
async def cancel_add(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup()
    await state.reset_state()
    await call.message.answer('Действие отменено!\n\n'
                              '-------------------------\n'
                              f'Добро пожаловать {call.from_user.username}\n\n'
                              f'Вы находитесь в админ панеле,\n'
                              f'выберите одно из действий ниже',
                              reply_markup=main_keyboard_admin)


