from django.forms import ModelForm

from .models import SiteConfig


class SiteConfigForm(ModelForm):
    class Meta:
        model = SiteConfig
