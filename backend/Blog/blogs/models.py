from django.db import models

# Create your models here.

class BlogModel(models.Model):
    summary = models.TextField(max_length=None, blank = False, default = '')
    title = models.CharField(max_length= 250)
    source_url = models.URLField("", max_length=200)