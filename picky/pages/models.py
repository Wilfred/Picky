from django.db import models

from docutils.core import publish_parts

from .utils import slugify

class Page(models.Model):
    name = models.CharField(max_length=200)
    name_slug = models.CharField(max_length=200, editable=False)
    name_lower = models.CharField(max_length=200, editable=False)

    version = models.IntegerField(default=1, editable=False)
    is_latest_version = models.BooleanField(default=True, editable=False)
    current_version = models.ForeignKey('self', editable=False)

    content = models.TextField()

    def get_rendered_content(self):
        """Render the reStructured text as an HTML snippet."""
        parts = publish_parts(self.content, writer_name="html",
                              settings_overrides={'doctitle_xform': False})
        html_snippet = parts['html_body']
        return html_snippet

    def create_revision(self):
        """Take the last saved state of this page, and save it as a
        separate revision. This ensures that we can update the latest
        version without losing old states.

        """
        last_saved_state = Page.objects.get(id=self.id)
        last_saved_state.is_latest_version = False
        last_saved_state.id = None
        super(Page, last_saved_state).save() # avoiding infinite loop

    def save(self):
        # if this was editing an existing page:
        if self.id:
            self.create_revision()
            self.version += 1
            
        else: # page creation
            self.current_version = self
        
        # We do the minimum modification possible to produce a
        # workable, attractive URL.
        self.name_slug = slugify(self.name)

        # Since we sort pages case insensitively, we store the
        # lowercase name.
        self.name_lower = self.name.lower()
        
        super(Page, self).save()
