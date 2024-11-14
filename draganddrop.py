from __future__ import annotations

from typing import Callable, Optional

from nicegui import ui

from database.models import Task



dragged: Optional[card] = None


class column(ui.column):

    def __init__(self, name: str, on_drop: Optional[Callable[[Task, str], None]] = None) -> None:
        super().__init__()
        with self.classes('bg-blue-500 w-60 p-4 rounded shadow-2'):
            ui.label(name).classes('text-black ml-1')
        self.name = name
        self.on('dragover.prevent', self.highlight)
        self.on('dragleave', self.unhighlight)
        self.on('drop', self.move_card)
        self.on_drop = on_drop

    def highlight(self) -> None:
        self.classes(remove='bg-blue-500', add='bg-gray-300')

    def unhighlight(self) -> None:
        self.classes(remove='bg-gray-300', add='bg-blue-500')

    async def move_card(self) -> None:
        global dragged  # pylint: disable=global-statement # noqa: PLW0603
        self.unhighlight()
        
        # Obtener la tarea que se está moviendo
        task_to_move = dragged.task
        
        # Actualizar la ubicación de la tarea en la base de datos
        task_to_move.location = self.name  # Cambiar la ubicación a la nueva columna
        await task_to_move.save()  # Guardar los cambios en la base de datos

        dragged.parent_slot.parent.remove(dragged)
        with self:
            card(dragged.task)
        self.on_drop(dragged.task, self.name)
        dragged = None


class card(ui.card):

    def __init__(self, task: Task) -> None:
        super().__init__()
        self.task = task
        with self.props('draggable').classes('w-full cursor-pointer bg-gray-100'):
            ui.label(task.serial).classes('text-md text-black')  # Mostrar el título de la tarea
            ui.label(f"Tarea: {task.task}").classes('text-sm')
            ui.label(f"Item: {task.item}").classes('text-sm')
            ui.label(f"Orden: {task.orden}").classes('text-sm')
            ui.label(f"Contrato: {task.contract}").classes('text-sm')
            ui.label(f"Fecha: {task.date}").classes('text-sm')
            ui.label(f"Hora: {task.time}").classes('text-sm')
            ui.label(f"Notas: {task.notes}").classes('text-sm')
        self.on('dragstart', self.handle_dragstart)

    def handle_dragstart(self) -> None:
        global dragged  # pylint: disable=global-statement # noqa: PLW0603
        dragged = self