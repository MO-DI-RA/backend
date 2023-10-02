from django.db import models

# Create your models here.
class Post(models.Model): 
    #글의 제목, 내용, 작성일, 마지막 수정일
    title = models.CharField(max_length=50, unique=True, error_messages={'unique': '이미 존재하는 제목입니다'})
    content = models.TextField()
    dt_created = models.DateTimeField(verbose_name ="Date Created", auto_now_add = True) #마지막 저장 시간을 해당 필드에 저장
    dt_modified = models.DateTimeField(verbose_name = "Date Modified", auto_now = True) #처음 생성될 때의 시간을 해당 필드에 저장
    #두 가지 DateTimeField 모두 True면 에러 발생
    
    def __str__(self) :
        return self.title
    