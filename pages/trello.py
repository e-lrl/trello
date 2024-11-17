from nicegui import ui
from datetime import datetime
import draganddrop as dnd
from database.models import Task
from tortoise.exceptions import DoesNotExist


def handle_drop(todo: Task, location: str):
    ui.notify(f'"{todo.serial}" ha sido movido a {location}')



@ui.refreshable
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
                    dnd.card(task=task).on('click', lambda task=task: edit_task_dialog(task))
        ui.button('Agregar Tarea', icon='add', on_click=open_new_task_dialog)  # Asegúrate de que el evento esté aquí
 
 # Agregar un método para manejar la creación de una nueva tarea
def open_new_task_dialog():
    with ui.dialog() as dialog, ui.card():
        serial_input = ui.input(label='Numero de Serie', placeholder='start typing')
        task_input = ui.input(label='Tarea', placeholder='start typing')
        item_input = ui.input(label='Item', placeholder='start typing')
        orden_input = ui.input(label='Orden', placeholder='start typing')
        contract_input = ui.input(label='Contrato', placeholder='start typing')
        datetime_input = datetime.now()
        notes_input = ui.input(label='Notas', placeholder='start typing')
        location_input = ('Próximo')
        ui.button('Guardar', on_click=lambda: save_new_task(serial=serial_input.value, task=task_input.value, item=item_input.value, orden=orden_input.value, contract=contract_input.value, datetime=datetime_input.value, notes=notes_input.value, location=location_input.value, dialog=dialog))
        ui.button('Cerrar', on_click=dialog.close)
        dialog.open()

# Función para guardar la nueva tarea (debes implementarla según tu lógica)
async def save_new_task(serial, task, item, orden, contract, datetime, notes, location, dialog):
    # Aquí puedes agregar la lógica para guardar la tarea en la base de datos
    await Task.create(serial=serial, task=task, item=item, orden=orden, contract=contract, datetime=datetime, notes=notes, location=location)
    dialog.close()
    ui.notify(f'Tarea "{serial}" creada.')
    await get_data.refresh()  # Actualizar la interfaz para mostrar la nueva tarea

def edit_task_dialog(task):
        with ui.dialog() as dialog, ui.card():
            serial_input = ui.input(label='Numero de Serie', placeholder='start typing', value=task.serial)
            task_input = ui.input(label='Tarea', placeholder='start typing', value=task.task)
            item_input = ui.input(label='Item', placeholder='start typing', value=task.item)
            orden_input = ui.input(label='Orden', placeholder='start typing', value=task.orden)
            contract_input = ui.input(label='Contrato', placeholder='start typing', value=task.contract)
            datetime_input = ui.input(label='Dia', placeholder='start typing', value=task.datetime)
            notes_input = ui.input(label='Notas', placeholder='start typing', value=task.notes)
            location_input = ui.input(label='Localizacion', placeholder='start typing', value=task.location)
            ui.button('Guardar', on_click=lambda: save_edit_task(serial=serial_input.value, task=task_input.value, item=item_input.value, orden=orden_input.value, contract=contract_input.value, date=date_input.value, time=time_input.value, notes=notes_input.value, location=location_input.value, dialog=dialog))
            ui.button('Cerrar', on_click=dialog.close)
            dialog.open()
# Función para guardar la nueva tarea (debes implementarla según tu lógica)
async def save_edit_task(serial, task, item, orden, contract, datetime, notes, location, dialog):
    try:
        # Obtener la tarea existente por su serial
        existing_task = await Task.get(serial=serial)
        
        # Actualizar los campos de la tarea
        existing_task.task = task
        existing_task.item = item
        existing_task.orden = orden
        existing_task.contract = contract
        existing_task.datetime = datetime
        existing_task.notes = notes
        existing_task.location = location
        
        # Guardar los cambios en la base de datos
        await existing_task.save()
        
        dialog.close()  # Cierra el diálogo
        ui.notify(f'Tarea "{serial}" actualizada.')  # Notificación de éxito
        await get_data.refresh()  # Actualizar la interfaz para mostrar la tarea actualizada
    except DoesNotExist:
        ui.notify(f'Tarea con serial "{serial}" no encontrada.')  # Notificación de error si no se encuentra la tarea

@ui.page('/trello')

async def trello():
    with ui.header().classes('bg-gray-800 p-4 text-white rounded-b-lg shadow-lg'):
        ui.label('TrelloPy').style('font-size: 28px; font-weight: bold; font-family: "Arial", sans-serif;')

        with ui.row().classes('ml-auto'):
            ui.switch(on_change=lambda e: ui.dark_mode(e.value))
    await get_data()

