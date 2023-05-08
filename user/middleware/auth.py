from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

from user.models import User

import jwt

SECRET_KEY = settings.SECRET_KEY


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.path.startswith('/admin/'):
            try:
                request.user = None
                token = request.headers.get('Authorization', None).split('Bearer ')[1]
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                user = User.objects.get(id=payload['uid'])
                request.user = user
            except:
                pass
