import re

from django.db import models
from django.utils.text import truncate_words
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from creoleparser import text2html

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

    def get_toc(self):
        """Render a table of contents for this content."""
        content = self.get_content()

        # Extract anything that looks like a heading.
        headings = []
        for row in content.splitlines():
            row = row.strip()
            match = re.match(r'(=+)(.*?)=*$', row)

            if match:
                depth = len(match.groups()[0])
                name = match.groups()[1].strip()
                headings.append((depth, name))

        # Don't bother showing a TOC if there aren't any headings.
        if not headings:
            return ""

        # Ensure the lowest depth is 1.
        min_depth = None
        for (depth, name) in headings:
            if min_depth is None:
                min_depth = depth
            elif depth < min_depth:
                min_depth = depth

        headings = [(depth + 1 - min_depth, name)
                    for (depth, name) in headings]

        # Write headings as a nested bulleted list.
        headings_creole = []
        for depth, name in headings:
            link = "#%s" % (name.lower().replace(' ', '-'))
            headings_creole.append("%s [[%s|%s]]" % ("*" * depth, link, name))

        toc_template = "=== Table Of Contents\n%s" % "\n".join(headings_creole)

        return text2html(toc_template)

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

    def get_absolute_url(self):
        return reverse('view_page', args=[self.name_slug])

    def save(self, user=None):
        self.total_revisions += 1

        # We do the minimum modification possible to produce a
        # workable, attractive URL.
        self.name_slug = slugify(self.name)

        # Since we sort pages case insensitively, we store the
        # lowercase name.
        self.name_lower = self.name.lower()
        
        super(Page, self).save()

        PageRevision.objects.create(
            page=self, content=self.content, name=self.name,
            version=self.total_revisions,
            author=user)

    def __unicode__(self):
        return u"%s %s" % (self.name, truncate_words(self.content, 4))


class PageRevision(models.Model):
    class Meta:
        ordering = ["-version"]

    content = models.TextField()
    name = models.CharField(max_length=200, null=True)
    page = models.ForeignKey('Page')
    version = models.IntegerField(default=1, editable=False)
    time = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u"%s at %s" % (self.page.name, self.time)
