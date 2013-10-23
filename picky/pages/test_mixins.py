import string
import random

from django.test import TestCase

from milkman.dairy import milkman

from .models import Page


class PageTest(TestCase):
    def create_page(self, **kwargs):
        letters = list(string.letters)
        random.shuffle(letters)
        random_name = ''.join(letters[:10])

        page_kwargs = {'name' : random_name}
        page_kwargs.update(kwargs)
        
        return milkman.deliver(Page, **page_kwargs)


