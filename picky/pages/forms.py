from django.forms import ModelForm, ValidationError, Textarea

from .models import Page
from .utils import slugify


class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
        widgets = {'content': Textarea(attrs={'rows': 22})}

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = "warn-on-unload"
        self.fields['content'].widget.attrs['class'] = "warn-on-unload"

    def save(self, *args, **kwargs):
        user = kwargs.pop('user')
        
        kwargs['commit'] = False
        page = super(PageForm, self).save(*args, **kwargs)

        page.save(user=user)
        return page

    def clean_name(self):
        """Check that this name doesn't match any other name when converted to
        a slug. We also check that this page name won't introduce a
        clash with other URLs.

        """
        name = self.cleaned_data['name']
        name_slug = slugify(name)

        # don't allow slashes in names
        if '/' in name_slug:
            raise ValidationError("You can't have / in a page name.")

        same_slug_pages = Page.objects.filter(name_slug=name_slug)

        if self.instance.id:
            # We are editing an existing Page, so we only want to
            # check for other pages with the same slug.
            same_slug_pages = same_slug_pages.exclude(id=self.instance.id)

        if same_slug_pages.exists():
            raise ValidationError("That name clashes with another page's URL.")

        return name
