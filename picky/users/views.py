from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import (render_to_response, get_object_or_404,
                              render, redirect)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

from .forms import UserForm


@login_required
def all_users(request):
    active_users = User.objects.filter(is_active=True).order_by('email')
    inactive_users = User.objects.filter(is_active=False).order_by('email')
    
    template_vars = {'active_users': active_users,
                     'inactive_users': inactive_users}
    return render_to_response("users/all_users.html", template_vars,
                              RequestContext(request))


@login_required
def create_user(request):
    if not request.user.is_superuser:
        return permission_denied(request)
    
    if request.POST:
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('all_users'))
    else:
        form = UserForm()

    template_vars = {'form': form}

    return render_to_response("users/create_user.html", template_vars,
                              RequestContext(request))


@login_required
def edit_user(request, user_id):
    if not request.user.is_superuser:
        return permission_denied(request)
    
    user = User.objects.get(id=user_id)
    
    if request.POST:
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('all_users'))
    else:
        form = UserForm(instance=user)

    template_vars = {'form': form, 'user': user}

    return render_to_response("users/edit_user.html", template_vars,
                              RequestContext(request))


@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return permission_denied(request)

    user = get_object_or_404(User, id=user_id)

    # Note that request.POST is empty so it's falsy.
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('all_users'))
    else:
        template_vars = {'user': user}
        return render_to_response("users/delete_user.html", template_vars,
                                  RequestContext(request))



def permission_denied(request):
    response = render_to_response("users/permission_denied.html", {},
                                  RequestContext(request))
    response.status = 403
    return response


@login_required
def logout_user(request):
    logout(request)

    return HttpResponseRedirect(reverse('index'))


def login_picker(request):
    next_url = request.GET.get('next')
    return render(request, 'users/login_picker.html',
                  {'next': next_url})


def user_not_active(request):
    user = request.user
    if user.is_authenticated() and user.is_active:
        return redirect('index')
    
    return render(request, "users/user_not_active.html")
