import ormar
import os
import databases
import sqlalchemy
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR/'.env'))

database = databases.Database(os.getenv('DB_ENGINE'))
metadata = sqlalchemy.MetaData()

SECRET_KEY = os.getenv('SECRET_KEY')

SENDING_NUMBER = os.getenv('SENDING_NUMBER')
API_KEY = os.getenv('API_KEY')

class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


try:
    os.mkdir(os.path.join(BASE_DIR, 'media'))
    print('directory for save manage is created')
except:
    print('directory is exits')



