import re
import jwt
import datetime

from django.http  import JsonResponse

from my_settings  import SECRET_KEY
from users.models import User

    def validate_email(self, email):
        regex = re.compile('^[0-9a-z\-\_]{5,20}$')
        if not regex.match(email):
            return False
        return True

    def validate_password(self, password):
        regex = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,16}$')
        if not regex.match(password):
            return False
        return True

    def validate_name(self, name):
        regex = re.compile('^[가-힣a-zA-Z]+$')
        if not regex.match(name):
            return False
        return True

    def validate_birth_date(self, birth_date):
        regex = re.compile('^[\d]{4}-[\d]{2}-[\d]{2}$')
        if not regex.match(birth_date):
            return False
        return True

    def validate_phone_number(self, phone_number):
        regex = re.compile('^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
        if not regex.match(phone_number):
            return False
        return True

    def validate_duplication(self, email, phone_number):
        if User.objects.filter(email=email):
            return False
        elif User.objects.filter(phone_number=phone_number):
            return False
        return True