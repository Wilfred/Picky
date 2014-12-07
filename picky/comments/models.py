from django.db import models
from django.contrib.auth.models import User

from picky.pages.rendering import render_creole


class Comment(models.Model):
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    page = models.ForeignKey('pages.Page')

    parent = models.ForeignKey('self', null=True)

    def get_rendered_content(self):
        return render_creole(self.text)
