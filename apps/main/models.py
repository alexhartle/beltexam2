from __future__ import unicode_literals
from ..login.models import User
import time, re
from django.db import models

# Create your models here.
class AppointmentsManager(models.Manager):
    def validate(self, postData):
        errors = []
        today = time.strftime("%Y-%m-%d")
        DATE_REGEX = re.compile(r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$')
        TIME_REGEX = re.compile(r'^([01]\d|2[0-3]):?([0-5]\d)$')
        if len(postData['task']) < 1:
            errors.append("Task cannot be blank.")
        if postData['date'] < today:
            errors.append("Must be a future date. Cannot add dates before today.")
        if not DATE_REGEX.match(postData['date']):
            errors.append("Dates must be in YYYY-MM-DD format")
        if not TIME_REGEX.match(postData['time']):
            errors.append("Time must be in HH:MM format")
        return errors

class Appointments(models.Model):
    task = models.CharField(max_length = 255)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length = 255, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    objects = AppointmentsManager()
