from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse
from .models import Page
from .forms import PageForm

# Create your views here.
def index(request):
    return render(request, 'diary/index.html')

class PageListView(ListView):
    model = Page
    template_name = 'diary/page_list.html'
    ordering = ['-dt_created']
    paginate_by = 8
    page_kwarg = 'page'

def info(request):
    return render(request, 'diary/info.html')

class PageCreateView(CreateView):
    model = Page
    form_class = PageForm
    template_name = 'diary/page_form.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse('page-create', kwargs={'page_id': self.object.id})    

class PageDetailView(DetailView):
    model = Page
    template_name = 'diary/page_detail.html'
    pk_url_kwarg = 'page_id'
    context_object_name = 'object'

class PageUpdateView(UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'diary/page_form.html'
    pk_url_kwarg = 'page_id'
    def get_success_url(self):
        return reverse('page-detail', kwargs={'page_id': self.object.id})
    
def page_delete(request, page_id):
    object = Page.objects.get(id=page_id)
    if request.method == 'POST':
        object.delete()
        return redirect('page-list')
    else:
        return render(request, 'diary/page_confirm_delete.html', {'object': object})