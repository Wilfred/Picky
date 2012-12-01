from __future__ import unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse

from milkman.dairy import milkman

from .models import Page
from users.test_base import UserTest


class RenderingTest(TestCase):
    def test_basic_rendering(self):
        page = milkman.deliver(Page, content="hello world")
        self.assertEqual(page.get_rendered_content().strip(), "<p>hello world</p>")

    def test_h1_rendered(self):
        page = milkman.deliver(Page, content="= foo")
        self.assertEqual(page.get_rendered_content(), '<h1>foo</h1>')

    def test_h2_rendered(self):
        page = milkman.deliver(Page, content="""
= bar

== foo 1

== foo 2

""")

        self.assertIn('<h2>foo 1</h2>', page.get_rendered_content())
        self.assertIn('<h2>foo 2</h2>', page.get_rendered_content())


class PageCreationTest(UserTest):
    def test_page_creation(self):
        self.client.post(reverse('create_page'),
                         {'name': 'foo', 'content': 'bar'})

        response = self.client.get(reverse('view_page', args=['foo']))
        self.assertEqual(response.status_code, 200)
        
    def test_duplicate_page_name(self):
        milkman.deliver(Page, name='foo')

        self.client.post(reverse('create_page'),
                         {'name': 'foo', 'content': 'bar'})

        self.assertEqual(Page.objects.count(), 1)


class PageDeletingTest(UserTest):
    def test_page_delete(self):
        page = milkman.deliver(Page)

        self.client.post(reverse('delete_page', args=[page.id]))
        self.assertFalse(Page.objects.filter(id=page.id).exists())
        

class PageVersioningTest(UserTest):
    def test_page_edit(self):
        page = milkman.deliver(Page, content='foo')

        page.content = 'bar'
        page.save()

        self.assertEqual(page.total_revisions, 2)

        # check we have an old revision with the original content
        self.assertEqual(page.get_content(1), 'foo')

    def test_view_shows_latest(self):
        page = milkman.deliver(Page, name='foo', content='foo')

        page.content = 'bar'
        page.save()

        response = self.client.get(reverse('view_page', args=[page.name_slug]))
        self.assertEqual(response.context['page'], page)

    def test_view_old_version(self):
        page = milkman.deliver(Page, name='foo', content='foo')

        page.content = 'bar'
        page.save()

        page_v1_content = page.get_rendered_content(version=1)
        response = self.client.get(reverse('view_page', args=[page.name_slug]) + '?version=1')
        self.assertEqual(response.context['content'], page_v1_content)

class PageViewTest(UserTest):
    def test_nonexistent_page(self):
        response = self.client.get(
            reverse('view_page', args=["no-page-with-this-name"]))

        self.assertEqual(response.status_code, 404)

    def test_page_history(self):
        page = milkman.deliver(Page, name='foo', content='foo')
        response = self.client.get(
            reverse('view_page_history', args=[page.id]))

        self.assertEqual(response.status_code, 200)
