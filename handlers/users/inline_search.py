from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from loader import dp
from aiogram import types

from utils.db_api.schemas import add_product, users_db


@dp.inline_handler()
async def start_inline(query: types.InlineQuery):

    if query.query == '':
        name_product = await add_product.select_all_products()
        name = []
        for product in name_product:                 # цикл сортировки списка имён
            name.append(product.name)
        linked_list = sorted(name)

        items = []
        for titles in linked_list:
            select_item = await add_product.select_by_text(text=titles)   # поиск по имение товара('элементы последовательны от сортированного списка)

            items.append(InlineQueryResultArticle(
                        id=select_item.id_product,
                        title=select_item.name,
                        description=f'{select_item.price} ₽',
                        thumb_url=select_item.photo,
                        input_message_content=InputTextMessageContent(
                            message_text=f'/product {select_item.id_product}')
                        )
                    )
        await query.answer(results=items, cache_time=3)

    if query.query != None:
        message_text = query.query.title()
        items = []
        select_item = await add_product.select_by_text(text=message_text)
        items.append(InlineQueryResultArticle(
                id=select_item.id_product,
                title=select_item.name,
                description=f'{select_item.price} ₽',
                thumb_url=select_item.photo,
                input_message_content=InputTextMessageContent(
                    message_text=f'/product {select_item.id_product}')
            )
            )
        await query.answer(results=items, cache_time=3)







