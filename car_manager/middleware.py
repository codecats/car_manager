from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin


class AutoAuth(MiddlewareMixin):
    def process_request(self, request):
        user = User.objects.filter().first()
        if user:
            request.user = user