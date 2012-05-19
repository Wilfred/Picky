from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Page
from .forms import PageForm


@login_required
def all_pages(request):
    pages = Page.objects.filter(is_latest_revision=True).order_by('name_lower')
    template_vars = {'pages': pages}
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
    version_specified = request.GET.get('version')
    try:
        version_specified = int(version_specified)
    except (TypeError, ValueError):
        version_specified = None

    # todo: what if two pages had the same name for a given version
    # number?
    if version_specified:
        page = get_object_or_404(Page, name_slug=page_slug, version=version_specified)
    else:
        page = get_object_or_404(Page, name_slug=page_slug, is_latest_revision=True)

    template_vars = {'page': page}
    
    return render_to_response("pages/view_page.html", template_vars,
                              RequestContext(request))


@login_required
def view_page_history(request, page_id):
    # we allow users to link to the history via any page revision ID
    page_revision = Page.objects.get(id=page_id)

    current_revision = page_revision.current_revision
    all_revisions = Page.objects.filter(current_revision=current_revision).order_by('-version')

    template_vars = {'page': current_revision,
                     'all_revisions': all_revisions}
    return render_to_response("pages/view_page_history.html", template_vars,
                              RequestContext(request))
