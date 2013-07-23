from django.db import models
from django.contrib.auth.models import User

from creoleparser import creole2html


class Comment(models.Model):
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    page = models.ForeignKey('pages.Page')

    parent = models.ForeignKey('self', null=True)

    def get_rendered_content(self):
        # todo: add favicons the same way we do for pages
        return creole2html(self.text)
