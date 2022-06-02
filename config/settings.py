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


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
