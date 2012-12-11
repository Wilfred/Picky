from django.http import HttpResponseBadRequest
from django.core.urlresolvers import reverse

from .forms import CommentForm


def new_comment(request, page_id):
    if not request.POST:
        return HttpResponseBadRequest

    # todo: set page, user and parent comment
    form = CommentForm(request.POST)
    form.save()

    return reverse('view_page', args=[page_id])

