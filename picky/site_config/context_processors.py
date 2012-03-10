from .models import SiteConfig


def include_config(request):
    """A context processor that ensures we always have the site
    configuration in the template context.

    """
    try:
        site_config = SiteConfig.objects.get()
    except SiteConfig.DoesNotExist:
        site_config = SiteConfig.objects.create()
        
    return {'config': site_config}
