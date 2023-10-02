from re import template
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress
from allauth.account.views import PasswordChangeView
from coplate.models import Review, User
from coplate.forms import ReviewForm, ProfileForm
from coplate.functions import confirmation_required_redirect

# Create your views here.

# 메인 페이지 뷰(IndexView) - Review 모델의 데이터를 목록으로 표시
class IndexView(ListView):
    model = Review
    template_name = "coplate/index.html"
    context_object_name = "reviews"
    paginate_by = 4
    ordering = ["-dt_created"]

# 리뷰 상세 페이지 뷰(ReviewDetailView) - Review 모델의 특정 데이터를 상세하게 표시
class ReviewDetailView(DetailView):
    model = Review
    template_name = "coplate/review_detail.html"
    pk_url_kwarg = "review_id"

# 리뷰 작성 페이지 뷰(ReviewCreateView) - Review 모델에 데이터를 추가하는 폼을 제공
class ReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "coplate/review_form.html"

    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("review-detail", kwargs={"review_id": self.object.id})

    def test_func(self, user):
        # 사용자의 이메일이 확인되어야 리뷰 작성이 가능한지 확인하는 함수
        return EmailAddress.objects.filter(user=user, verified=True).exists()

# 리뷰 수정 페이지 뷰(ReviewUpdateView) - Review 모델의 데이터를 수정하는 폼을 제공
class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "coplate/review_form.html"
    pk_url_kwarg = "review_id"

    raise_exception = True

    def get_success_url(self):
        return reverse("review-detail", kwargs={"review_id": self.object.id})

    def test_func(self, user):
        # 리뷰 작성자인지 확인하여 리뷰 수정 권한을 부여하는 함수
        review = self.get_object()
        return review.author == user

# 리뷰 삭제 페이지 뷰(ReviewDeleteView) - Review 모델의 데이터를 삭제하는 화면을 제공
class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = "coplate/review_confirm_delete.html"
    pk_url_kwarg = "review_id"

    raise_exception = True

    def get_success_url(self):
        return reverse("index")

    def test_func(self, user):
        # 리뷰 작성자인지 확인하여 리뷰 삭제 권한을 부여하는 함수
        review = self.get_object()
        return review.author == user

# 프로필 페이지 뷰(ProfileView) - User 모델의 데이터와 관련된 리뷰를 표시
class ProfileView(DetailView):
    model = User
    template_name = "coplate/profile.html"
    pk_url_kwarg = "user_id"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("user_id")
        context["user_reviews"] = Review.objects.filter(author__id=user_id).order_by("-dt_created")[:4]
        return context

# 특정 사용자의 리뷰 목록 페이지 뷰(UserReviewListView) - 특정 사용자가 작성한 리뷰를 목록으로 표시
class UserReviewListView(ListView):
    model = Review
    template_name = "coplate/user_review_list.html"
    context_object_name = "user_reviews"
    paginate_by = 4

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Review.objects.filter(author__id=user_id).order_by("-dt_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = get_object_or_404(User, id=self.kwargs.get("user_id"))
        return context

# 프로필 설정 페이지 뷰(ProfileSetView) - 사용자 프로필 정보를 설정하는 폼 제공
class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "coplate/profile_set_form.html"
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse("index")

# 프로필 업데이트 페이지 뷰(ProfileUpdateView) - 사용자 프로필 정보를 업데이트하는 폼 제공
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "coplate/profile_update_form.html"
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse("profile", kwargs=({"user_id": self.request.user.id}))

# 사용자 정의 비밀번호 변경 뷰(CustomPasswordChangeView) - 사용자 정의 비밀번호 변경 기능 제공
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse("profile", kwargs=({"user_id": self.request.user.id}))
