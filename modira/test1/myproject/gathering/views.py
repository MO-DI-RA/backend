from django.http import HttpResponse


def hello(request):
    return HttpResponse("안녕하세요, Django!")

