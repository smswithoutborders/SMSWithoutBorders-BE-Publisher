from peewee import CharField
from peewee import TextField
from peewee import ForeignKeyField
from peewee import DateTimeField

from SwobBackendPublisher.schemas.baseModel import BaseModel

from SwobBackendPublisher.schemas.users import Users

from datetime import datetime

class Wallets(BaseModel):
    username = CharField(null=True)
    token = TextField(null=True)
    uniqueId = CharField(null=True)
    uniqueIdHash = CharField(unique=True, null=True)
    iv = CharField(null=True)
    userId = ForeignKeyField(Users, column_name="userId")
    platformId = CharField(column_name="platformId")
    createdAt = DateTimeField(null=True, default=datetime.now)

    class Meta:
        indexes = ((('userId', 'platformId'), True),)