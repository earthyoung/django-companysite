from msilib.schema import Error
from django import forms
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
import bcrypt

from manager.validators import *
from manager.info import admin_email, admin_password
from manager.models import Company, CompanyImg



class JoinForm(forms.Form):
    email = forms.EmailField(label=_('이메일'))
    password = forms.CharField(min_length=8, max_length=20, validators=[validate_password], label=_('비밀번호'))
    name = forms.CharField(min_length=5, max_length=20, validators=[validate_name], label=_('이름'))
    phone = forms.CharField(min_length=11, max_length=13, validators=[validate_phone], label=_('전화번호'))
    business_name = forms.CharField(min_length=5, max_length=20, validators=[validate_business_name], label=_('회사명'))
    company_img_1 = forms.ImageField(required=False, label=_('이미지 1'))
    company_img_2 = forms.ImageField(required=False, label=_('이미지 2'))
    

    def validate(self):
        com_email = self.cleaned_data['email']
        com_password = self.cleaned_data['password']
        com_name = self.cleaned_data['name']
        com_phone = self.cleaned_data['phone']
        com_business_name = self.cleaned_data['business_name']
        com_company_img_1 = self.cleaned_data['company_img_1']
        com_company_img_2 = self.cleaned_data['company_img_2']

        try:
            company = Company.objects.get(email=com_email)
        except Company.DoesNotExist:
            try:
                # save images if exist
                if com_company_img_1 is not None:
                    new_company_img_1 = CompanyImg.objects.create(
                        img = com_company_img_1,
                    )
                    new_company_img_1.save()
                if com_company_img_2 is not None:    
                    new_company_img_2 = CompanyImg.objects.create(
                        img = com_company_img_2,
                    )
                    new_company_img_2.save()

                # encrypt password
                pw_bcrypt = bcrypt.hashpw(com_password.encode('utf-8'), bcrypt.gensalt())
                hashed_pw = pw_bcrypt.decode('utf-8')
                
                # save company
                new_company = Company.objects.create(
                    email = com_email, password = hashed_pw, name = com_name,
                    phone = com_phone, business_name = com_business_name,
                    img1 = new_company_img_1, img2 = new_company_img_2,
                )   
                new_company.save()       
            except Exception as err:
                print(err)
                raise Http404("회원가입 중 오류가 발생했습니다. 다시 시도해 주세요.")
            return True
        except Exception:
            raise Http404("회원가입 중 오류가 발생했습니다. 다시 시도해 주세요.")
        raise Http404("이미 존재하는 회원입니다.")



        
class LoginForm(forms.Form):
    email = forms.EmailField(label=_('이메일'))
    password = forms.CharField(max_length=20, validators=[validate_password] ,label=_('비밀번호'))

    def login(self):
        user_email = self.cleaned_data['email']
        user_password = self.cleaned_data['password']

        if user_email == admin_email() and user_password == admin_password():
            content = {
            'company_id': 0,
            'state': 'admin',
            }
            print("admin logged in")
            return content

        # company case
        try:
            company = Company.objects.get(email=user_email)
            company_pw = company.password   # original hashed pw

            result = bcrypt.checkpw(user_password.encode('utf-8'), company_pw.encode('utf-8'))

            if result:
                content = {
                    'company_id': company.id,
                    'state': 'company',
                }
                return content
        except Company.DoesNotExist:
            return None
        except Exception as err:
            print(err)
            return None
        return None


# 관리자도 회사의 구분키, 이메일, 비밀번호는 임의로 바꿀 수 없음(조회는 가능)
class CompanyUpdateForm(forms.Form):
    name = forms.CharField(min_length=5, max_length=20, label=_('이름'))
    phone = forms.CharField(min_length=11, max_length=13, validators=[validate_phone], label=_('전화번호'))
    business_name = forms.CharField(min_length=5, max_length=20, label=_('회사명'))
    img1 = forms.ImageField(required=False, label=_('이미지 1'))
    img2 = forms.ImageField(required=False, label=_('이미지 2'))


    def validate(self, company_id):
        com_name = self.cleaned_data['name']
        com_phone = self.cleaned_data['phone']
        com_business_name = self.cleaned_data['business_name']
        com_img1 = self.cleaned_data['img1']
        com_img2 = self.cleaned_data['img2']

        try:
            company = get_object_or_404(Company, pk=company_id)

            # name, business_name duplicate check
            try:
                company1 = Company.objects.get(name=com_name)
                if company1.id != company_id:
                    raise ValidationError("이미 사용 중인 이름입니다.")
            except Company.DoesNotExist:
                pass
            try:
                company2 = Company.objects.get(business_name=com_business_name)
                if company2.id != company_id:
                    raise ValidationError("이미 사용 중인 회사명입니다.")
            except Company.DoesNotExist:
                pass
                
            # img 1
            if com_img1 is not None:    # 추가한 이미지 파일이 있는 경우
                if company.img1 is not None:    # 기존의 이미지 파일이 있음 -> 기존 이미지를 삭제하고 새 이미지를 추가
                    image_1 = CompanyImg.objects.get(img=company.img1.img)   # 기존 이미지 불러와서 삭제
                    company.img1 = None
                    image_1.delete()    # Q. 이미지가 삭제될 때 로컬 디렉토리의 파일도 같이 삭제되나?
                    new_img1 = CompanyImg.objects.create(img=com_img1)
                    new_img1.save()
                    company.img1 = new_img1
                else:   # 추가한 이미지 파일이 있는데 기존에 저장된 이미지 파일은 없는 경우
                    new_img1 = CompanyImg.objects.create(img=com_img1)
                    new_img1.save()
                    company.img1 = new_img1

            # img 2
            if com_img2 is not None: 
                if company.img2 is not None: 
                    image_2 = CompanyImg.objects.get(img=company.img2.img)
                    company.img2 = None 
                    image_2.delete()
                    new_img2 = CompanyImg.objects.create(img=com_img2)
                    new_img2.save()
                    company.img2 = new_img2
                else: 
                    new_img2 = CompanyImg.objects.create(img=com_img2)
                    new_img2.save()
                    company.img2 = new_img2


            # 다른 필드 처리
            company.name = com_name; company.phone = com_phone; company.business_name = com_business_name
            company.save()
        except ValidationError as invalid:
            raise ValidationError(invalid)
        except Exception as err:
            print(err)
            raise Http404("회원 정보가 변경되지 않았습니다. 다시 시도해 주세요.")    


class ChangeEmailForm(forms.Form):
    original_email = forms.EmailField(label=_('기존 이메일'))
    new_email = forms.EmailField(label=_('새로운 이메일'))


    def validate(self, company_id):
        original_email = self.cleaned_data['original_email']
        new_email = self.cleaned_data['new_email']
        company = None; company2 = None
        try:
            company = Company.objects.get(email=original_email)
        except Company.DoesNotExist:
            raise ValidationError("현재 계정의 이메일 주소가 아닙니다. 다시 입력해주세요.")
        if company.id != company_id:
            raise ValidationError("현재 계정의 이메일 주소가 아닙니다. 다시 입력해주세요")
        try:
            company2 = Company.objects.get(email=new_email)
        except Company.DoesNotExist:
            company.email = new_email
            company.save()
            return
        if company2.id == company_id:
            raise ValidationError("현재 사용하는 이메일입니다. 다른 값을 입력해주세요.")
        raise ValidationError("다른 사용자가 사용하는 이메일입니다. 다른 값을 입력해주세요.")


class ChangePasswordForm(forms.Form):
    original_pw = forms.CharField(min_length=8, max_length=20, label=_('기존 비밀번호'))
    new_pw = forms.CharField(min_length=8, max_length=20, label=_('새 비밀번호'))


    def validate(self, company_id):
        original_pw = self.cleaned_data['original_pw']
        new_pw = self.cleaned_data['new_pw']
        try:
            company = get_object_or_404(Company, pk=company_id)
            db_pw = company.password
            result = bcrypt.checkpw(original_pw.encode('utf-8'), db_pw.encode('utf-8'))
            if result:
                pw_bcrypt = bcrypt.hashpw(new_pw.encode('utf-8'), bcrypt.gensalt())
                hashed_pw = pw_bcrypt.decode('utf-8')
                company.password = hashed_pw
                company.save()
                return
            raise ValidationError("기존 비밀번호를 잘못 입력했습니다. 다시 입력해 주세요.")
        except Exception as err:
            print(err)
            raise Exception("비밀번호 변경 중 오류가 발생했습니다.")
            
                





        



