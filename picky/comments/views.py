from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .forms import CommentForm
from pages.models import Page


@login_required
@require_http_methods(["POST"])
def new_comment(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    
    # todo: set page, user and parent comment
    form = CommentForm(request.POST)
    comment = form.save(commit=False)
    comment.page = page
    comment.user = request.user
    comment.save()

    return HttpResponseRedirect(reverse('view_page', args=[page.name_slug]))

