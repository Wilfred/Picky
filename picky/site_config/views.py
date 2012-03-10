from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from .models import SiteConfig
from .forms import SiteConfigForm


@login_required
def configure_site(request):
    try:
        site_config = SiteConfig.objects.get()
    except SiteConfig.DoesNotExist:
        site_config = SiteConfig.objects.create()

    if request.POST:
        form = SiteConfigForm(request.POST, instance=site_config)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('all_pages'))
    else:
        form = SiteConfigForm(instance=site_config)

    template_vars = {'form': form}
    
    return render_to_response("site_config/configure_site.html", template_vars,
                              RequestContext(request))


@login_required
def not_found(request):
    return render_to_response("site_config/404.html", {},
                              RequestContext(request))
