from django.db import models
from django.utils.text import truncate_words
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .utils import slugify
from .rendering import render_creole


class PageManager(models.Manager):
    def all_urls(self):
        urls = set()
        for page in self.all():
            # Since we can link to both slugs and original names, we
            # consider both.
            urls.add(reverse('view_page', args=[page.name]))
            urls.add(reverse('view_page', args=[page.name_slug]))

        return urls


class Page(models.Model):
    objects = PageManager()
    
    name = models.CharField(max_length=200, unique=True)
    name_slug = models.CharField(max_length=200, editable=False, unique=True)
    name_lower = models.CharField(max_length=200, editable=False)

    content = models.TextField()

    total_revisions = models.IntegerField(default=0, editable=False)

    def get_rendered_content(self, version=None):
        """Render the creole source as an HTML snippet."""
        return render_creole(self.get_content(version))

    def get_content(self, version=None):
        """Either the current content of this page or an older version."""
        if version:
            revision = self.pagerevision_set.get(version=version)
            return revision.content
        else:
            return self.content

    def get_creation_time(self):
        first_revision = self.pagerevision_set.order_by('version')[0]
        return first_revision.time

    def get_last_edit_time(self):
        last_revision = self.pagerevision_set.order_by('-version')[0]
        return last_revision.time

    def get_latest_revision(self):
        return self.pagerevision_set.order_by('-version')[0]

    def get_change_count(self):
        return self.pagerevision_set.count() - 1

    def save(self, user):
        self.total_revisions += 1

        # We do the minimum modification possible to produce a
        # workable, attractive URL.
        self.name_slug = slugify(self.name)

        # Since we sort pages case insensitively, we store the
        # lowercase name.
        self.name_lower = self.name.lower()
        
        super(Page, self).save()

        PageRevision.objects.create(
            page=self, content=self.content, version=self.total_revisions,
            author=user)

    def __unicode__(self):
        return u"%s %s" % (self.name, truncate_words(self.content, 4))


class PageRevision(models.Model):
    class Meta:
        ordering = ["-version"]

    content = models.TextField()
    page = models.ForeignKey('Page')
    version = models.IntegerField(default=1, editable=False)
    time = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u"%s at %s" % (self.page.name, self.time)
