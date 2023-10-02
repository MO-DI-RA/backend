import re

from django.forms import ValidationError

#https://velog.io/@lob3767/ValidatorDjango
REGEX_EMAIL        = '^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD     = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

def email_validate(email):
    if not re.match(REGEX_EMAIL, email):
                raise ValidationError("이메일 형식이 아닙니다.")

def password_validate(password):
    if not re.match(REGEX_PASSWORD, password):
                raise ValidationError("비밀번호 양식이 맞지 않습니다.")
