from tortoise import fields, models

# Definimos la plantilla para crear usuarios
class Card(models.Model):
    id = fields.IntField(pk=True)
    serial = fields.CharField(max_length=128, unique=True)
    task = fields.CharField(max_length=128)
    item = fields.CharField(max_length=128)
    orden = fields.CharField(max_length=128)
    contract = fields.CharField(max_length=128)
    date = fields.CharField(max_length=128)
    time = fields.CharField(max_length=128)
    notes = fields.CharField(max_length=128)

# Nombre de la tabla
class Meta:
        table = "Cards"