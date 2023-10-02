from django import forms
from .models import User, Review

# 리뷰 작성 폼(ReviewForm) 정의
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review  # Review 모델과 연결
        fields = [
            "title",
            "restaurant_name",
            "restaurant_link",
            "rating",
            "image1",
            "image2",
            "image3",
            "content",
        ]  # 폼에서 사용할 필드 지정
        widgets = {
            "rating": forms.RadioSelect,  # rating 필드를 라디오 버튼으로 표시
        }

# 프로필 편집 폼(ProfileForm) 정의
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User  # User 모델과 연결
        fields = [
            "nickname",
            "profile_pic",
            "intro",
        ]  # 폼에서 사용할 필드 지정
        widgets = {
            "intro": forms.Textarea,  # intro 필드를 텍스트 영역으로 표시
        }
