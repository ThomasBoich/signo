from datetime import datetime
from django.db import models


class HiddenDeletedMixin(models.Model):
    hidden = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True


class DateTimeMixin(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True