from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from .models import Page
from .forms import PageForm


def all_pages(request):
    template_vars = {'pages': Page.objects.order_by('name')}
    return render_to_response("all_pages.html", template_vars,
                              RequestContext(request))


def create_page(request):

    if request.POST:
        form = PageForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('all_pages'))
    else:
        form = PageForm()

    template_vars = {'form': form}

    return render_to_response("page_edit.html", template_vars,
                              RequestContext(request))


def view_page(request, page_slug):
    page = Page.objects.get(name_slug=page_slug)
    template_vars = {'page': page}
    
    return render_to_response("view_page.html", template_vars,
                              RequestContext(request))
