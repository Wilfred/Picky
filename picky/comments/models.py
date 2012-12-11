from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    page = models.ForeignKey('pages.Page')

    parent = models.ForeignKey('self', null=True)
