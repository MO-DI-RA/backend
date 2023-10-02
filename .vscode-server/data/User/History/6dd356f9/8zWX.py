from django.urls import reverse
from django.shortcuts import redirect

class ProfileSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if (
            request.user.is_authenticated
            and not request.user.nickname
            and not request.user.kakao_id
            and not request.user.address
            and request.path_info != reverse('profile-set')
        ):
            return redirect("profile-set")
        
        response = self.get_response(request)
        return response