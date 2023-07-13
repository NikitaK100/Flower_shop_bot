import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
admins = os.getenv('ADMIN_ID')

qiwi_token = os.getenv('QIWI_TOKEN')
qiwi_key = os.getenv('QIWI_PUBKEY')
qiwi_number = os.getenv('QIWI_NUMBER')

USER_DB = os.getenv('PG_USER')
PASSWORD_DB = os.getenv('PG_PASSWORD')
HOST_DB = os.getenv('PG_HOST')
DATABASE = os.getenv('PG_NAME_DB')

link_gino = f"postgresql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}/{DATABASE}"