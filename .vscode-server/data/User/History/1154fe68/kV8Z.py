from .models import Page

def validate_pages():
    pages = Page.objects.all()
    for page in pages :
        if page.score < 0 or page.score >10:
            