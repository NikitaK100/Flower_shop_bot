from utils.db_api.schemas.create_table import Users


async def add_item(id: int, name: str, referal_link: str, wallet: int = 0):
    try:
        user = Users(id=id, name=name, referal_link=referal_link, wallet=wallet)
        await user.create()
    except Exception as err:
        print('Error Table Users\n'
              '-------------------------------------------------------\n'
              f'{err}')


async def select_user_by_referal_link(referal_link: str):
    user = await Users.query.where(Users.referal_link == referal_link).gino.first()
    return user


async def select_user_by_id(id: int):
    user = await Users.query.where(Users.id == id).gino.first()
    return user


async def update_wallet_by_id(id: int, wallet: int):
    user = await Users.get(id)
    await user.update(id=id, wallet=wallet).apply()


async def select_all_users():
    users = await Users.query.gino.all()
    return users

