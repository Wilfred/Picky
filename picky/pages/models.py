from django.db import models

from docutils.core import publish_parts

from .utils import slugify

class Page(models.Model):
    name = models.CharField(max_length=200)
    name_slug = models.CharField(max_length=200, editable=False)
    name_lower = models.CharField(max_length=200, editable=False)
    version = models.IntegerField(default=1, editable=False)
    is_latest_version = models.BooleanField(default=True, editable=False)

    content = models.TextField()

    def get_rendered_content(self):
        """Render the reStructured text as an HTML snippet."""
        parts = publish_parts(self.content, writer_name="html",
                              settings_overrides={'doctitle_xform': False})
        html_snippet = parts['html_body']
        return html_snippet

    def save(self):
        # if this was editing an existing page:
        if self.id:
            # first, make an old revision of the previous state
            old_revision = Page.objects.get(id=self.id)
            old_revision.is_latest_version = False
            super(Page, old_revision).save() # avoiding infinite loop

            # now create a new revision
            self.id = None
            self.version += 1
        
        # We do the minimum modification possible to produce a
        # workable, attractive URL.
        self.name_slug = slugify(self.name)

        # Since we sort pages case insensitively, we store the
        # lowercase name.
        self.name_lower = self.name.lower()
        
        super(Page, self).save()
