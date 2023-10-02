from django.shortucts import redirect


def confirmation_required_redirect(self, request):
    return redirect("account_email_confirmation_required")