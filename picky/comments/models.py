from django.db import models
from django.contrib.auth.models import User

from creole import creole2html


class Comment(models.Model):
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    page = models.ForeignKey('pages.Page')

    parent = models.ForeignKey('self', null=True)

    def get_rendered_content(self):
        return creole2html(self.text)
