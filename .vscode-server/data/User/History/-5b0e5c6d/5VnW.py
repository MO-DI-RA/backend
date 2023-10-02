from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress
from .functions import confirmation_required_redirect

class LoginAndVerificationRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect

    def test_func(self, user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()