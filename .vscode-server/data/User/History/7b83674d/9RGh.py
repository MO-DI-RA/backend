from django.shortcuts import render, redirect
from .models import Page
from .forms import PageForm

# Create your views here.
def page_list(request):
    object_list = Page.objects.all()
    return render(request, 'diary/page_list.html', {'object_list': object_list})

def info(request):
    return render(request, 'diary/info.html')

def page_detail(request, page_id):
    object = Page.objects.get(id=page_id)
    return render(request, 'diary/page_detail.html', {'object': object})

def page_create(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        new_page = form.save()
        return redirect('page-detail', page_id=new_page.id)
    else:
        form = PageForm()
        return render(request, 'diary/page_form.html', {'form' : form})