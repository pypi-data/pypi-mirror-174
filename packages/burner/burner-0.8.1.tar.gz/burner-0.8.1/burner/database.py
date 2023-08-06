from peewee import (
    Model,
    ForeignKeyField,
    TextField,
    CharField,
    FloatField,
    BooleanField,
    Proxy,
    SqliteDatabase,
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
    code = CharField(5, unique=True)


class Price(BaseModel):
    price = FloatField()
    enabled = BooleanField()
    country = ForeignKeyField(Country)
    service = ForeignKeyField(Service)


def create(database_path: str) -> SqliteDatabase:
    """
    Create a connection to the database and initialise it with the necessary tables.

    Args:
        database_path (str): Where to save the database to.

    Returns:
        The new database connection.
    """
    conn = SqliteDatabase(database_path)
    proxy.initialize(conn)
    conn.create_tables([Country, Price, Service])

    return conn
