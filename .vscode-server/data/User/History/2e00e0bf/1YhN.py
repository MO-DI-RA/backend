from django.http import HttpResponse


def hello(request):
    return HttpResponse("<h2>안녕하세요, Django!</h2>")

