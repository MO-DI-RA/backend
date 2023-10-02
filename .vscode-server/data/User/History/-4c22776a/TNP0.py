from django.shortcuts import render
from .models import Page
# Create your views here.
def page_list(request):
    object_list = Page.objects.all()
    return render(request, 'diary/page_list.html', {'object_list':object_list})