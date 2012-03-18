from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

from .forms import UserForm


@login_required
def all_users(request):
    template_vars = {'users': User.objects.all()}
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
    

def permission_denied(request):
    response = render_to_response("users/permission_denied.html", {},
                                  RequestContext(request))
    response.status = 403
    return response


@login_required
def logout_user(request):
    logout(request)

    return HttpResponseRedirect(reverse('index'))