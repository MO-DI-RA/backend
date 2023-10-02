from .models import Page
import random

def validate_pages():
    pages = Page.objects.all()
    for page in pages :
        if page.score < 0 or page.score >10:
            page.score = random.randit(0, 10)
            page.save()