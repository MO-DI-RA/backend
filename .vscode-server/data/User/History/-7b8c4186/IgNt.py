from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_no_special_characters, validate_rastaurant_link

# Create your models here.

# 사용자(User) 모델 정의
class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,  # 닉네임은 고유해야 함
        null=True,    # Null 값 허용
        validators=[validate_no_special_characters],  # validate_no_special_characters 함수를 이용한 유효성 검사
        error_messages={"unique": "이미 사용중인 닉네임입니다."},  # 중복 닉네임에 대한 에러 메시지
    )
    profile_pic = models.ImageField(default="default_profile_pic.jpg", upload_to="profile_pics")  # 기본 프로필 이미지 및 업로드 경로
    intro = models.CharField(max_length=60, blank=True)  # 최대 60자의 소개글, 빈 값 허용
    email_domain = models.CharField(max_length=30, null = True)

    def __str__(self):
        return self.email  # 객체를 문자열로 나타낼 때는 이메일을 사용

# 리뷰(Review) 모델 정의
class Review(models.Model):
    title = models.CharField(max_length=30)  # 리뷰 제목, 최대 30자
    restaurant_name = models.CharField(max_length=20)  # 레스토랑 이름, 최대 20자
    restaurant_link = models.URLField(validators=[validate_rastaurant_link])  # 레스토랑 링크, validate_rastaurant_link 함수를 이용한 유효성 검사

    RATING_CHOICES = [
        (1, "★"),     # 1점
        (2, "★★"),    # 2점
        (3, "★★★"),   # 3점
        (4, "★★★★"),  # 4점
        (5, "★★★★★"), # 5점
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=None)  # 별점, RATING_CHOICES에서 선택된 값 중 하나, 기본값은 None

    image1 = models.ImageField(upload_to="review_pics")      # 리뷰 이미지 1, review_pics 디렉토리에 업로드
    image2 = models.ImageField(upload_to="review_pics", blank=True)  # 리뷰 이미지 2, 빈 값 허용
    image3 = models.ImageField(upload_to="review_pics", blank=True)  # 리뷰 이미지 3, 빈 값 허용
    content = models.TextField()  # 리뷰 내용, 긴 텍스트를 위한 TextField 사용
    dt_created = models.DateTimeField(auto_now_add=True)  # 생성 일자와 시간, 객체 생성 시 자동으로 현재 시간으로 설정
    dt_updated = models.DateTimeField(auto_now=True)      # 업데이트 일자와 시간, 저장 시 자동으로 현재 시간으로 설정

    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 리뷰 작성자, User 모델과의 관계 설정, 작성자가 삭제되면 리뷰도 함께 삭제

    def __str__(self):
        return self.title  # 객체를 문자열로 나타낼 때는 리뷰 제목 사용
