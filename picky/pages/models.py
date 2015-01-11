import re

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.functional import allow_lazy
from django.utils import six

from creoleparser import text2html

from .utils import slugify, creole_slugify, remove_links
from .rendering import render_creole


def truncate_words(s, num, end_text='...'):
    truncate = end_text and ' %s' % end_text or ''
    return Truncator(s).words(num, truncate=truncate)
truncate_words = allow_lazy(truncate_words, six.text_type)


class PageManager(models.Manager):
    def get_query_set(self):
        qs = super(PageManager, self).get_query_set()
        return qs.filter(deleted=False)
    
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
    all_objects = models.Manager()
    
    name = models.CharField(max_length=200, unique=True, null=True)
    name_slug = models.CharField(max_length=200, editable=False, unique=True, null=True)
    name_lower = models.CharField(max_length=200, editable=False, null=True)

    content = models.TextField(blank=True)

    deleted = models.BooleanField(default=False)

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
                headings.append((depth, remove_links(name)))

        # Don't bother showing a TOC if there aren't any headings.
        if not headings:
            return ""

        # Ensure the lowest depth is 1, so:
        # == foo
        # === bar
        # becomes [(1, 'foo',), (2, 'bar')]
        min_depth = min(depth for (depth, name) in headings)
        headings = [(depth + 1 - min_depth, name)
                    for (depth, name) in headings]

        # Ensure that the initial depth is 1, so:
        # === foo
        # == bar
        # === baz
        # becomes [(1, 'foo'), (1, 'bar'), (2, 'baz')]
        first_depth, _ = headings[0]
        if first_depth != 1:
            excess = first_depth - 1

            for index, (depth, name) in enumerate(headings):
                if depth == 1:
                    break
                headings[index] = (depth - excess, name)

        # FIXME:
        # = foo
        # === bar
        # should be [(1, 'foo',), (2, 'bar')]

        # Write headings as a nested bulleted list.
        headings_creole = []
        for depth, name in headings:
            link = "#%s" % (creole_slugify(name))
            headings_creole.append("%s [[%s|%s]]" % ("#" * depth, link, name))

        toc_template = "\n".join(headings_creole)

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

    def delete(self):
        self.deleted = True

        # Since we require name attributes to be unique, we need to
        # remove these attributes so we can create new pages with
        # these names.
        self.name = None
        self.name_slug = None
        self.name_lower = None
        
        self.save()

    def save(self, user=None):
        self.total_revisions += 1

        # We do the minimum modification possible to produce a
        # workable, attractive URL.
        self.name_slug = slugify(self.name)

        # Since we sort pages case insensitively, we store the
        # lowercase name.
        if self.name:
            self.name_lower = self.name.lower()
        else:
            self.name_lower = None
        
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
        return u"%s at %s" % (self.name, self.time)
