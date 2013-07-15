from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Page, PageRevision
from .forms import PageForm
from comments.forms import CommentForm


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
def edit_page(request, page_slug):
    page = get_object_or_404(Page, name_slug=page_slug)

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
def view_page_actions(request, page_slug):
    page = get_object_or_404(Page, name_slug=page_slug)
    template_vars = {'page': page}

    return render_to_response("pages/page_actions.html", template_vars,
                              RequestContext(request))


@login_required
def delete_page(request, page_slug):
    page = get_object_or_404(Page, name_slug=page_slug)

    # Note that request.POST is empty so it's falsy.
    if request.method == 'POST':
        page.delete()
        return redirect('all_pages')
    else:
        template_vars = {'page': page}
        return render_to_response("pages/page_delete.html", template_vars,
                                  RequestContext(request))


@login_required
def view_page(request, page_slug):
    try:
        page = Page.objects.get(name_slug=page_slug)
    except Page.DoesNotExist:
        return page_404(request, page_slug)
        
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
def view_page_comments(request, page_slug):
    page = get_object_or_404(Page, name_slug=page_slug)
    comments = page.comment_set.all()

    form = CommentForm()

    template_vars = {'page': page, 'comments': comments, 'form': form}
    return render(request, "pages/view_page_comments.html", template_vars)


@login_required
def view_page_history(request, page_slug):
    page = get_object_or_404(Page, name_slug=page_slug)
    all_revisions = PageRevision.objects.filter(page=page)

    template_vars = {'page': page,
                     'all_revisions': all_revisions}
    return render_to_response("pages/view_page_history.html", template_vars,
                              RequestContext(request))


def page_404(request, page_slug):
    """Return a helpful 404 if the user was looking for a page that
    doesn't exist.

    """
    return render(request, "pages/no_such_page.html",
                  {'name_slug': page_slug})
