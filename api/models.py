from django.contrib.postgres.fields import JSONField
from django.db import models


class EmailData(models.Model):
    email = models.EmailField(unique=True)
    data = JSONField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
