from django.db import models

class Page(models.Model):
    name = models.CharField(max_length=200, unique=True)
    name_slug = models.CharField(max_length=200, unique=True)

    content = models.TextField()
