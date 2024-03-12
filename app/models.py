from tortoise import fields
from tortoise.models import Model

# models.py

class VehicleData(Model):
    id = fields.IntField(pk=True)
    data = fields.JSONField()
    timestamp = fields.DatetimeField(auto_now_add=True)