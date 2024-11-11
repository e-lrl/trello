from nicegui import ui
from dataclasses import dataclass
import draganddrop as dnd

@dataclass
class ToDo:
    title: str

def handle_drop(todo: ToDo, location: str):
    ui.notify(f'"{todo.title}" está en {location}')

@ui.page('/trello')
async def trello():
    with ui.header().classes('bg-gray-800 p-4 text-white rounded-b-lg shadow-lg'):
        ui.label('TrelloPy').style('font-size: 28px; font-weight: bold; font-family: "Arial", sans-serif;')

        with ui.row().classes('ml-auto'):
            ui.switch(on_change=lambda e: ui.dark_mode(e.value))
    
    with ui.row().classes('self-center').style('font-family: "Arial", sans-serif; font-weight: bold;'):
        with dnd.column('Próximo', on_drop=handle_drop):
            dnd.card(ToDo('Simplificar Diseño'))
            dnd.card(ToDo('Proveer Despliegue'))
        
        with dnd.column('En Proceso', on_drop=handle_drop):
            dnd.card(ToDo('Mejorar Documentación'))
        
        with dnd.column('Hecho', on_drop=handle_drop):
            dnd.card(ToDo('Inventar NiceGUI'))
            dnd.card(ToDo('Probar en Proyectos Propios'))
            dnd.card(ToDo('Publicar como Código Abierto'))
            dnd.card(ToDo('Lanzar Modo Nativo'))