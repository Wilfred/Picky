# -*- coding: utf-8 -*-
import re
import json
from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Page
from .test_mixins import PageTest
from .templatetags.time_format import relative_time
from users.test_base import UserTest


class RenderingTest(PageTest):
    def assertEqualIgnoringWhitespace(self, string1, string2):
        """Assert that strings are equal, other than whitespace differences."""
        # remove leading/trailing whitespace
        string1 = string1.strip()
        string2 = string2.strip()

        # collapse and normalise whitespace
        string1 = re.sub(r'\s+', ' ', string1)
        string2 = re.sub(r'\s+', ' ', string2)

        self.assertEqual(string1, string2)
    
    def test_basic_rendering(self):
        page = self.create_page(content="hello world")
        self.assertEqualIgnoringWhitespace(page.get_rendered_content(), "<p>hello world</p>")

    def test_h1_rendered(self):
        page = self.create_page(content="= foo")
        self.assertEqualIgnoringWhitespace(page.get_rendered_content(), '<h1 id="foo">foo</h1>')

    def test_h2_rendered(self):
        page = self.create_page(content="""
= bar

== foo 1

== foo 2

""")

        self.assertIn('<h2 id="foo-1">foo 1</h2>', page.get_rendered_content())
        self.assertIn('<h2 id="foo-2">foo 2</h2>', page.get_rendered_content())

    def test_newline_rendering(self):
        page = self.create_page(content="hello\nworld")
        self.assertEqualIgnoringWhitespace(page.get_rendered_content(), "<p>hello world</p>")

    def test_br_rendering(self):
        page = self.create_page(content="hello\\\\world")
        self.assertEqualIgnoringWhitespace(page.get_rendered_content(), "<p>hello<br/>world</p>")

    def test_unicode_rendering(self):
        content = u"Tú"
        page = self.create_page(content=content)
        self.assertEqualIgnoringWhitespace(
            page.get_rendered_content(), u"<p>Tú</p>")

    def test_nonexistent_url_rendering(self):
        page = self.create_page(content="[[no_such_page]]")
        self.assertEqualIgnoringWhitespace(
            page.get_rendered_content(),
            '<p><a class="nonexistent" href="/page/no_such_page">no_such_page</a></p>')


class TocTest(PageTest):
    def test_basic_toc(self):
        page = self.create_page(content="== hello world")
        self.assertIn('<a href="#hello-world">', page.get_toc())

    def test_toc_funky_chars(self):
        page = self.create_page(content="== 123, 456!")
        self.assertIn('<a href="#123-456">', page.get_toc())

    def test_empty_toc(self):
        page = self.create_page(content="hello world")
        self.assertEqual(page.get_toc(), "")


class PageCreationTest(UserTest, PageTest):
    def test_page_creation(self):
        self.client.post(reverse('create_page'),
                         {'name': 'foo', 'content': 'bar'})

        response = self.client.get(reverse('view_page', args=['foo']))
        self.assertEqual(response.status_code, 200)
        
    def test_empty_page_creation(self):
        """We should be able to create pages even with empty content."""
        self.client.post(reverse('create_page'),
                         {'name': 'foo', 'content': ''})

        response = self.client.get(reverse('view_page', args=['foo']))
        self.assertEqual(response.status_code, 200)
        
    def test_duplicate_page_name(self):
        self.create_page(name='foo')

        self.client.post(reverse('create_page'),
                         {'name': 'foo', 'content': 'bar'})

        self.assertEqual(Page.objects.count(), 1)


class PageDeletingTest(UserTest, PageTest):
    def test_page_delete(self):
        page = self.create_page()

        self.client.post(reverse('delete_page', args=[page.name_slug]))
        self.assertFalse(Page.objects.filter(id=page.id).exists())
        

class PageVersioningTest(UserTest, PageTest):
    def test_page_edit(self):
        page = self.create_page(content='foo')

        page.content = 'bar'
        page.save()

        self.assertEqual(page.total_revisions, 2)

        # check we have an old revision with the original content
        self.assertEqual(page.get_content(1), 'foo')

    def test_view_shows_latest(self):
        page = self.create_page(name='foo', content='foo')

        page.content = 'bar'
        page.save()

        response = self.client.get(reverse('view_page', args=[page.name_slug]))
        self.assertEqual(response.context['page'], page)

    def test_view_old_version(self):
        page = self.create_page(name='foo', content='foo')

        page.content = 'bar'
        page.save()

        page_v1_content = page.get_rendered_content(version=1)
        response = self.client.get(reverse('view_page', args=[page.name_slug]) + '?version=1')
        self.assertEqual(response.context['content'], page_v1_content)

class PageViewTest(UserTest, PageTest):
    def test_nonexistent_page(self):
        response = self.client.get(
            reverse('view_page', args=["no-page-with-this-name"]))

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "pages/no_such_page.html")

    def test_page_history(self):
        page = self.create_page(name='foo', content='foo')
        response = self.client.get(
            reverse('view_page_history', args=[page.name_slug]))

        self.assertEqual(response.status_code, 200)

    # todo: check crash on '30 minutes ago'

    def test_page_slugifies(self):
        """Check that we redirect unslugified page URLs."""
        page = self.create_page(name="Foo Bar")
        
        response = self.client.get(
            reverse('view_page', args=[page.name]), follow=True)
        self.assertEqual(response.status_code, 200)


class IndexTest(UserTest, PageTest):
    def test_index_render_404(self):
        """If there's no home page yet, we should get a helpful 404."""
        response = self.client.get(reverse('index'), follow=True)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "pages/no_such_page.html")

    def test_index_renders(self):
        """If we do have a home page, we should display it."""
        self.create_page(name="Home", name_slug="home")
        
        response = self.client.get(reverse('index'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/view_page.html")

class AjaxTest(UserTest, PageTest):
    def test_all_urls(self):
        page = self.create_page(name="Foo")

        response = self.client.get(reverse('all_page_names'))

        # expect a valid JSOn response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers['content-type'],
                         ('Content-Type', 'application/json'))

        expected = [reverse('view_page', args=[page.name_slug])]
        self.assertEqual(json.loads(response.content), expected)


class RecentChangesTest(UserTest):
    def test_recent_changes_renders(self):
        response = self.client.get(reverse('recent_changes'))
        self.assertEqual(response.status_code, 200)
        

class SearchTest(UserTest):
    def test_search_renders(self):
        response = self.client.post(
            reverse('search'), {'search_term': 'hello world'})
        self.assertEqual(response.status_code, 200)


class DebugTest(UserTest):
    def test_debug_renders(self):
        response = self.client.get(reverse('debug'))
        self.assertEqual(response.status_code, 200)

    def test_debug_styling_renders(self):
        response = self.client.get(reverse('debug_styling'))
        self.assertEqual(response.status_code, 200)


class TimestampTest(TestCase):
    def test_three_months(self):
        three_months_ago = datetime.now() - timedelta(days=95)
        self.assertEqual(
            relative_time(three_months_ago),
            "3 months ago")

    def test_none(self):
        self.assertEqual(relative_time(None), "never")
