from nicegui import ui
from dataclasses import dataclass
import draganddrop as dnd
from database.models import Task

'''
@dataclass
class ToDo:
    title: str
'''



def handle_drop(todo: Task, location: str):
    ui.notify(f'"{todo.serial}" ha sido movido a {location}')

@ui.page('/trello')
async def get_data():
# Obtener todas las tareas de la base de datos
    tasks = await Task.all()

    # Crear un diccionario para almacenar las tareas por ubicación
    grouped_tasks = {
        "Próximo": [],
        "En Proceso": [],
        "Hecho": []
    }

    # Agrupar tareas por su campo 'location'
    for task in tasks:
        if task.location in grouped_tasks:
            grouped_tasks[task.location].append(task)

    # Crear columnas fijas
    with ui.row().classes('self-center').style('font-family: "Arial", sans-serif;'):
        for location in grouped_tasks.keys():
            with dnd.column(location, on_drop=handle_drop):
                for task in grouped_tasks[location]:
                    dnd.card(task=task)

async def trello():
    with ui.header().classes('bg-gray-800 p-4 text-white rounded-b-lg shadow-lg'):
        ui.label('TrelloPy').style('font-size: 28px; font-weight: bold; font-family: "Arial", sans-serif;')

        with ui.row().classes('ml-auto'):
            ui.switch(on_change=lambda e: ui.dark_mode(e.value))
    await get_data()