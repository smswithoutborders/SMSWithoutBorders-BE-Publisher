from peewee import Model

from SwobBackendPublisher.main import Lib

db = Lib.DB

class BaseModel(Model):
    class Meta:
        database = db
