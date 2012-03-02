from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Page


def all_pages(request):
    template_vars = {'pages': Page.objects.order_by('name')}
    return render_to_response("all_pages.html", template_vars,
                              RequestContext(request))
