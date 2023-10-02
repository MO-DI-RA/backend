from django.db import models

# Create your models here.

class Post(models.Model) : 
    # 글의 제목, 내용, 작성일, 마지막 수정일
    title = models.CharField(max_length = 50)
    content = models.TextField()
    dt_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True) #처음 생성 시간을 필드에 저장, 데이터 생성일
    dt_modified = models.DateTimeField(verbose_name="Date Modified", auto_now = True) #마지막 저장 시간을 필드에 저장, 데이터 마지막 수정일
    #두 DateField 모두 True인 경우 오류 발생
    
    def __str__(self) :
        return self.title
    