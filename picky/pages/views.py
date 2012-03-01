from django.http import HttpResponse


def all_pages(request):
    return HttpResponse('hello world')
