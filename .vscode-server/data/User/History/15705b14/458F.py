from django.shortcuts import render
from django.http import HttpResponse

def index(request) :
    return HttpResponse('<h1> 레스토랑 오픈 </h1>')
# Create your views here.
