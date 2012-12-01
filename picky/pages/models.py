from django.db import models
from django.utils.text import truncate_words

from creole import creole2html

from .utils import slugify

class Page(models.Model):
    name = models.CharField(max_length=200, unique=True)
    name_slug = models.CharField(max_length=200, editable=False, unique=True)
    name_lower = models.CharField(max_length=200, editable=False)

    content = models.TextField()

    total_revisions = models.IntegerField(default=0, editable=False)

    def get_rendered_content(self, version=None):
        """Render the creole source as an HTML snippet."""
        return creole2html(self.get_content(version))

    def get_content(self, version=None):
        """Either the current content of this page or an older version."""
        if version:
            revision = PageRevision.objects.get(page=self, version=version)
            return revision.content
        else:
            return self.content

    def get_all_versions(self):
        return PageRevision.objects.filter(page=self).order_by('version')

    def save(self):
        self.total_revisions += 1

        # We do the minimum modification possible to produce a
        # workable, attractive URL.
        self.name_slug = slugify(self.name)

        # Since we sort pages case insensitively, we store the
        # lowercase name.
        self.name_lower = self.name.lower()
        
        super(Page, self).save()

        PageRevision.objects.create(
            page=self, content=self.content, version=self.total_revisions)

    def __unicode__(self):
        return "%s %s" % (self.name, truncate_words(self.content, 4))


class PageRevision(models.Model):
    class Meta:
        ordering = ["-version"]

    content = models.TextField()
    page = models.ForeignKey('Page')
    version = models.IntegerField(default=1, editable=False)
