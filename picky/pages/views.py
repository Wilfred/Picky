from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Page
from .forms import PageForm


@login_required
def all_pages(request):
    template_vars = {'pages': Page.objects.order_by('name_lower')}
    return render_to_response("pages/all_pages.html", template_vars,
                              RequestContext(request))


@login_required
def create_page(request):

    if request.POST:
        form = PageForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('all_pages'))
    else:
        form = PageForm()

    template_vars = {'form': form}

    return render_to_response("pages/page_create.html", template_vars,
                              RequestContext(request))


@login_required
def edit_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)

    if request.POST:
        form = PageForm(request.POST, instance=page)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_page', args=[page.name_slug]))
    else:
        form = PageForm(instance=page)

    template_vars = {'form': form, 'page': page}

    return render_to_response("pages/page_edit.html", template_vars,
                              RequestContext(request))


@login_required
def delete_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)

    # Note that request.POST is empty so it's falsy.
    if request.method == 'POST':
        page.delete()
        return HttpResponseRedirect(reverse('all_pages'))
    else:
        template_vars = {'page': page}
        return render_to_response("pages/page_delete.html", template_vars,
                                  RequestContext(request))


@login_required
def view_page(request, page_slug):
    page = Page.objects.get(name_slug=page_slug)
    template_vars = {'page': page}
    
    return render_to_response("pages/view_page.html", template_vars,
                              RequestContext(request))
