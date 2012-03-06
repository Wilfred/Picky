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
    return render_to_response("all_users.html", template_vars,
                              RequestContext(request))


@login_required
def create_user(request):
    if request.POST:
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('all_users'))
    else:
        form = UserForm()

    template_vars = {'form': form}

    return render_to_response("create_user.html", template_vars,
                              RequestContext(request))


@login_required
def logout_user(request):
    logout(request)

    return HttpResponseRedirect(reverse('index'))
