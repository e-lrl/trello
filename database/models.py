from tortoise import fields, models

# Definimos la plantilla para crear nuevas tareas
class Task(models.Model):
    id = fields.IntField(pk=True)
    serial = fields.CharField(max_length=128, unique=True)
    task = fields.CharField(max_length=128)
    item = fields.CharField(max_length=128)
    orden = fields.CharField(max_length=128)
    contract = fields.CharField(max_length=128)
    datetime = fields.CharField(max_length=128)
    notes = fields.CharField(max_length=128)
    location = fields.CharField(max_length=128)

# Nombre de la tabla
class Meta:
        table = "Tasks"