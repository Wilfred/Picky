from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def not_found(request):
    return render_to_response("site_config/404.html", {},
                              RequestContext(request))
