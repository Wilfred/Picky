from django.forms import ModelForm, ValidationError

from .models import Page
from .utils import slugify


class PageForm(ModelForm):
    class Meta:
        model = Page

    def clean_name(self):
        """Check that this name doesn't match any other name when
        converted to a slug.

        """
        name = self.cleaned_data['name']
        name_slug = slugify(name)

        same_slug_pages = Page.objects.filter(name_slug=name_slug)

        if self.instance.id:
            # We are editing an existing Page, so we only want to
            # check for other pages with the same slug.
            same_slug_pages = same_slug_pages.exclude(id=self.instance)

        if same_slug_pages.exists():
            raise ValidationError("That name clashes with another page's URL.")

        return name
