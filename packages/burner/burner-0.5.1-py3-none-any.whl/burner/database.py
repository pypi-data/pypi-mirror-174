from peewee import (
    Model,
    ForeignKeyField,
    TextField,
    CharField,
    FloatField,
    BooleanField,
    Proxy,
)

proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database = proxy


class Country(BaseModel):
    image = TextField()
    name = CharField(unique=True)
    code = CharField(2, unique=True)


class Service(BaseModel):
    image = TextField()
    name = CharField(unique=True)
    code = CharField(2, unique=True)


class Price(BaseModel):
    price = FloatField()
    enabled = BooleanField()
    country = ForeignKeyField(Country)
    service = ForeignKeyField(Service)
