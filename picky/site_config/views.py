from django.template import RequestContext
from django.shortcuts import render_to_response


def not_found(request):
    return render_to_response("site_config/404.html", {},
                              RequestContext(request))
