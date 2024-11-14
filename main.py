from nicegui import app, ui
from tortoise.exceptions import DoesNotExist
from pages.trello import trello
from database.config import init_db, close_db
from database.models import Task

# Iniciamos la base de datos y la cerramos cuando se cierre la aplicacion
app.on_startup(init_db)
app.on_shutdown(close_db)

# Iniciamos la aplicacion
app.on_startup(trello)

async def run():
    # Generar y guardar 5 tareas ficticias
    for x in range(5):
        try:
        # Verificar si existen tareas
            await Task.get(serial=x)
            print(f"tarea {x} ya existe.")
        except DoesNotExist:
        # Si no existe, crearlas
            await Task.create(
                serial=str(x),
                task=str(x),
                item=str(x),
                orden=str(x),
                contract=str(x),
                date=str(x),
                time=str(x),
                notes=str(x),
                location="Próximo"
            )
            print("5 tareas ficticias han sido creadas.")
app.on_startup(run)



ui.run(title='TrelloPy', language='es', port=443, favicon='img/favicon.png', dark=False, fastapi_docs=True, reload=True)