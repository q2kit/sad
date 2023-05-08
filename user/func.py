from django.conf import settings

import jwt
import datetime
import hashlib

def generate_token(uid):
    payload = {
        'uid': uid,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
        'iat': datetime.datetime.utcnow()
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def verify_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return User.objects.get(id=payload['uid'])
    except:
        return None


def hash_password(password):
    return hashlib.sha256((password + settings.SECRET_KEY).encode()).hexdigest()
