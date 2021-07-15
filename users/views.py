import json
import bcrypt
import jwt
import datetime
from json.decoder           import JSONDecodeError

from django.http            import JsonResponse
from django.views           import View

from users.models           import User, Gender, Coupon
from users.validations      import Validation
from my_settings            import SECRET_KEY
from decorators             import validate_login


class SignupView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            email         = data['email']
            password      = data['password']
            name          = data['name']
            birth_date    = data['birth_date']
            phone_number  = data['phone_number']
            gender_string = data['gender']
            gender        = Gender.objects.get(gender=gender_string)

            if not Validation.validate_email(self, email):
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)
            if not Validation.validate_password(self, password):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)
            if not Validation.validate_name(self, name):
                return JsonResponse({'message':'INVALID_NAME'}, status=400)
            if not Validation.validate_birth_date(self, birth_date):
                return JsonResponse({'message':'INVALID_BIRTH_DATE'}, status=400)
            if not Validation.validate_phone_number(self, phone_number):
                return JsonResponse({'message':'INVALID_PHONE_NUMBER'}, status=400)
            if not Validation.validate_duplication(self, email, phone_number):
                return JsonResponse({'message':'DUPLICATED_USER'}, status=400)


            password = bcrypt.hashpw(
                    password.encode('utf-8'),
                    bcrypt.gensalt()
            ).decode('utf-8')

            User.objects.create(
                    email        = email,
                    password     = password,
                    name         = name,
                    birth_date   = birth_date,
                    phone_number = phone_number,
                    gender       = gender
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'NO_BODY'}, status=400)
        except Gender.DoesNotExist:
            return JsonResponse({'message': 'INVALID_GENDER'}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            users = User.objects.filter(email=email)
            if not users.exists():
                return JsonResponse({'message':'INVALID_EMAIL'}, status=401)

            user = users.first()
            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=401)
            
            access_token = jwt.encode(
                    {
                        'user_id': user.id,
                        'iat'    : datetime.datetime.now().timestamp()
                    },
                    SECRET_KEY,
                    algorithm = 'HS256'
            ).decode('UTF-8')

            return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message':'NO_BODY'}, status=400)

class CouponView(View):
    @validate_login
    def get(self, request, coupon):
        try:
            coupon = Coupon.objects.get(coupon=coupon).coupon
            return JsonResponse({'message': coupon}, status=200)
        except Coupon.DoesNotExist:
            return JsonResponse({'message': 'INVALID_COUPON'}, status=200)

class UserView(View):
    @validate_login
    def get(self, request):
        user = request.account
        user_info = {
                'user_name'  : user.name,
                'user_email' : user.email+'@lifefriends.com'
        }
        return JsonResponse({'message': 'SUCCESS', 'user_info': user_info}, status=200)
