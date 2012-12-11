from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import CommentForm
from pages.models import Page


@login_required
def new_comment(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    
    if not request.POST:
        return HttpResponseBadRequest("Not a POST")

    # todo: set page, user and parent comment
    form = CommentForm(request.POST)
    comment = form.save(commit=False)
    comment.page = page
    comment.user = request.user
    comment.save()

    return HttpResponseRedirect(reverse('view_page', args=[page.name_slug]))

