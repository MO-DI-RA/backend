from 

class ProfileSetup:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if (
            request.use.is_authenticated and
            not request.user.nickname and
            request.path_info != reverse('profile-set')
        ):
            return redirect("profile-set")
        response = self.get_response(request)
        return response