from django.db import models

from docutils.core import publish_parts

from .utils import slugify

class Page(models.Model):
    name = models.CharField(max_length=200, unique=True)
    name_slug = models.CharField(max_length=200, unique=True, editable=False)
    name_lower = models.CharField(max_length=200, editable=False)

    content = models.TextField()

    def get_rendered_content(self):
        """Render the reStructured text as an HTML snippet."""
        parts = publish_parts(self.content, writer_name="html")
        html_snippet = parts['body']
        return html_snippet

    def save(self):
        # We do the minimum modification possible to produce a
        # workable, attractive URL.
        self.name_slug = slugify(self.name)

        # Since we sort pages case insensitively, we store the
        # lowercase name.
        self.name_lower = self.name.lower()
        
        return super(Page, self).save()
