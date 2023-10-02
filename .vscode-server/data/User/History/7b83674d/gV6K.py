from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse
from .models import Page
from .forms import PageForm

# Create your views here.
def index(request):
    return render(request, 'diary/index.html')

class PageListView(ListView):
    model = Page
    ordering = ['-dt_created']
    paginate_by = 8

def info(request):
    return render(request, 'diary/info.html')

class PageCreateView(CreateView):
    model = Page
    form_class = PageForm
    context_object_name = 'form'
    def get_success_url(self):
        return reverse('page-create', kwargs={'page_id': self.object.id})    

class PageDetailView(DetailView):
    model = Page
    context_object_name = 'object'

class PageUpdateView(UpdateView):
    model = Page
    form_class = PageForm
    def get_success_url(self):
        return reverse('page-detail', kwargs={'page_id': self.object.id})

class PageDeleteView(UpdateView):
    model = Page
    def get_success_url(self):
        return reverse('page-list', kwargs={'page_id': self.object.id})