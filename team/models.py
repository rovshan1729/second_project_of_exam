from django.db import models
from utils.models import BaseModel

class Employee(BaseModel):
    id = models.CharField(max_length=255, primary_key=True)

    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    phone = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"
