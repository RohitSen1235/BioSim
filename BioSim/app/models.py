from django.db import models

# Create your models here.
class FileStorage(models.Model):
    zip_file = models.FileField(upload_to='results/')