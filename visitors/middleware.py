
from visitors.models import VisitorLog
from django.core.cache import cache
from django.utils import timezone



class UniqueVisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Identify the visitor using session data
        user_name = None
        session_key = request.session.session_key

        if request.user.is_authenticated:
            user_name = request.user.name

        # Check if a visitor entry already exists for the current session
        existing_visitor = VisitorLog.objects.filter(session_key=session_key).first()

        if not existing_visitor:
            VisitorLog.objects.create(
                ip_address=request.META['REMOTE_ADDR'],
                user_name=user_name,
                session_key=session_key
            )

        response = self.get_response(request)
        return response