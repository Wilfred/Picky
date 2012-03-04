from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User


def all_users(request):
    template_vars = {'users': User.objects.all()}
    return render_to_response("all_users.html", template_vars,
                              RequestContext(request))

