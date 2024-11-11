from tortoise import Tortoise

# Iniciamos la base de datos con su ubicacion, nombre y distintos modelos que gestiona el ORM
async def init_db() -> None:
    await Tortoise.init(db_url='sqlite://data/trello', modules={'models': ['database.models']})
    await Tortoise.generate_schemas()

# Cerramos base de datos
async def close_db() -> None:
    await Tortoise.close_connections()