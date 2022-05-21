from django.core.exceptions import ValidationError
from .models import *
import re


reg_special = re.compile('[`~!@#$%^&*=+{}|;:<>?/]')    # -와 _를 제외한 특수문자 포함/미포함
# reg_special = re.compile('[`~!@#$%^&*()_=+{}|;:<>,.?/]')   # 특수문자 포함/미포함
reg_loweren = re.compile(r'[a-z]')
reg_upperen = re.compile(r'[A-Z]')
reg_number = re.compile(r'[0-9]')
reg_phone_hyphen = re.compile(r'^((02)|(031)|(010)|(070))-\d{3,4}-\d{4}$')
reg_phone = re.compile(r'^((02)|(031)|(010)|(070))\d{7,8}$')


def validate_password(value):
    if reg_loweren.search(value) and reg_upperen.search(value) and reg_number.search(value):
        pass
    else:
        raise ValidationError("비밀번호는 숫자, 영어 소문자, 대문자를 모두 포함해야 합니다.")

    if not reg_special.search(value):
        raise ValidationError("비밀번호는 1개 이상의 특수문자를 포함해야 합니다.")


def validate_name(value):
    if reg_special.search(value):
        raise ValidationError("이름은 특수문자를 포함할 수 없습니다.")
    try:
        company = Company.objects.get(name=value)
    except Company.DoesNotExist:
        return
    raise ValidationError("이미 존재하는 이름입니다.")


def validate_phone(value):
    if reg_phone_hyphen.search(value) or reg_phone.search(value):
        pass
    else:
        raise ValidationError("올바른 전화번호 형식이 아닙니다. 다시 입력해주세요.")


def validate_business_name(value):
    if reg_special.search(value):
        raise ValidationError("회사명은 특수문자를 포함할 수 없습니다.")
    try:
        company = Company.objects.get(business_name=value)
    except Company.DoesNotExist:
        return
    raise ValidationError("이미 존재하는 회사명입니다.")


