import os
import datetime
from django.db import models


class FilesModel(models.Model):
    image = models.FileField(upload_to='%Y/%m/%d/')
    size = models.IntegerField()
    name = models.CharField(max_length=90, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.size = self.image.size
        self.name = self.image.name
        super(FilesModel, self).save(*args, **kwargs)