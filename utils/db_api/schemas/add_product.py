from sqlalchemy.ext.baked import bakery

from utils.db_api.db_gino import db
from utils.db_api.schemas.create_table import Items
from gino import Gino


async def add_item(id_product: str, name: str, description: str, photo: str, price: int):
    try:
        user = Items(id_product=id_product, name=name, description=description, photo=photo, price=price)
        await user.create()
    except Exception as err:
        print('Error Table Items\n'
              '-------------------------------------------------------\n'
              f'{err}')


async def select_all_products():
    products = await Items.query.gino.all()
    return products


async def select_by_text(text: str):
    select_text = await Items.query.where(Items.name == text).gino.first()
    return select_text


async def select_by_id_product(id_product: str):
    select_id = await Items.query.where(Items.id_product == id_product).gino.first()
    return select_id


async def delete_by_name_product(name: str):
    delete = await Items.delete.where(Items.name == name).gino.first()
    return delete