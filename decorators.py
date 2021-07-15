import jwt
import datetime

from django.http  import JsonResponse

from my_settings  import SECRET_KEY
from users.models import User

def validate_login(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("AUTHORIZATION", None)
            if not access_token:
                return JsonResponse({'MESSAGE': 'LOGIN_REQUIRED'}, status=401)

            token_payload = jwt.decode(
                    access_token,
                    SECRET_KEY,
                    algorithms="HS256"
            )

            expiration_delta = 60000000
            now = datetime.datetime.now().timestamp()
            if now > token_payload['iat'] + expiration_delta:
                return JsonResponse({'MESSAGE': 'TOKEN_EXPIRED'}, status=401)

            request.account = User.objects.get(id=token_payload['user_id'])
            return func(self, request, *args, **kwargs)
        except jwt.DecodeError:
            return JsonResponse({'MESSAGE': 'INVALID_JWT'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
    return wrapper



