from django import forms

class PageForm(forms.Form):
    title = forms.CharField(max_length=100, label='제목')
    content = forms.CharField(widget=forms.Textarea, label='감정 상태') 
    feeling = forms.CharField(max_length=80, label='감정 상태') 
    score = forms.IntegerField(abel='감정 점수') 
    dt_created = forms.DateField(label='작성일') 