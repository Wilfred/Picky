from django.db import models

from docutils.core import publish_parts

class Page(models.Model):
    name = models.CharField(max_length=200, unique=True)
    name_slug = models.CharField(max_length=200, unique=True)

    content = models.TextField()

    def get_rendered_content(self):
        """Render the reStructured text as an HTML snippet."""
        parts = publish_parts(self.content, writer_name="html")
        html_snippet = parts['body']
        return html_snippet
