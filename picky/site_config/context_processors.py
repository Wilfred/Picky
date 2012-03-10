from .models import SiteConfig


def include_config(request):
    """A context processor that ensures we always have the site
    configuration in the template context.

    """
    return {'config': SiteConfig.objects.get()}
