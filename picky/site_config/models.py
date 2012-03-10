from django.db import models

class SiteConfig(models.Model):
    site_name = models.CharField(max_length=200, unique=True)

