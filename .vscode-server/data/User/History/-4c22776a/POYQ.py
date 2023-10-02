from django.shortcuts import render

# Create your views here.
def page_list(request):
    return rendeer(request, 'diary/page_list.html')