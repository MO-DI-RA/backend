from django.shortcuts import render

# index.html 페이지를 부르는 index 함수
def index(request):
    return render(request, 'main/index.html')

def gathering(request):
    return render(request, 'main/test1.html')