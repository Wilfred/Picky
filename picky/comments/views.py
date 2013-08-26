from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import CommentForm
from .models import Comment
from pages.models import Page


@login_required
def new_comment(request, page_slug, parent_id=None):
    page = get_object_or_404(Page, name_slug=page_slug)
    if parent_id:
        parent_comment = get_object_or_404(Comment, id=parent_id)
    else:
        parent_comment = None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.page = page
        comment.user = request.user
        comment.parent = parent_comment
        comment.save()

        return redirect('view_page_comments', page.name_slug)
    else:
        form = CommentForm()

    return render(request, 'comments/comment_create.html',
                  {'form': form, 'page': page})
