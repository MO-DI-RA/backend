from django.shortcuts import render
from .models import Page


# Create your views here.
def page_list(request):
    object_list = Page.objects.all()
    return render(request, 'diary/page_list.html', {'object_list': object_list})

def info(request):
    return render(request, 'diary/info.html')

def page_detail(request, page_id):
    object = Page.objects.get(id=page_id)
    return render(request, 'diary/page_detail.html', {'object': object})
