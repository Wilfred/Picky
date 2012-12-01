from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Page, PageRevision
from .forms import PageForm


@login_required
def all_pages(request):
    pages = Page.objects.order_by('name_lower')
    template_vars = {'pages': pages}
    return render_to_response("pages/all_pages.html", template_vars,
                              RequestContext(request))


@login_required
def create_page(request):

    if request.POST:
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save()
            return HttpResponseRedirect(reverse('view_page', args=[page.name_slug]))
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
    page = get_object_or_404(Page, name_slug=page_slug)

    # get the requested version number from the user
    version_specified = request.GET.get('version')
    try:
        version_specified = int(version_specified)
    except (TypeError, ValueError):
        version_specified = None

    # ensure this page has a old revision with this version number
    if not 0 < version_specified < page.total_revisions:
        version_specified = None

    content = page.get_rendered_content(version_specified)
    template_vars = {'page': page, 'content': content,
                     'version_specified': version_specified}
    
    return render_to_response("pages/view_page.html", template_vars,
                              RequestContext(request))


@login_required
def view_page_history(request, page_id):
    # we allow users to link to the history via any page revision ID
    page = Page.objects.get(id=page_id)
    all_revisions = PageRevision.objects.filter(page=page)

    template_vars = {'page': page,
                     'all_revisions': all_revisions}
    return render_to_response("pages/view_page_history.html", template_vars,
                              RequestContext(request))
