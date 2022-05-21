from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator

from urllib.parse import urljoin
import os

from django.views import View
from website.settings import *
from .models import *
from .forms import *


# Create your views here.

class IndexView(View):

    def get(self, request):
        return render(request, 'manager/index.html')


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        content = {'form': form}
        return render(request, 'manager/login.html', content)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            company_info = form.login()
            if company_info is None:
                return redirect('login')
            if company_info['state'] == 'admin':
                request.session['admin'] = 'admin'  # 관리자 계정으로 로그인
                return redirect('manage')            
            if company_info['state'] == 'company':      
                request.session['company'] = company_info['company_id']  # 일반 기업으로 로그인
                return redirect('company', request.session.get('company'))
        return redirect('index')
       

class JoinView(View):
    
    def get(self, request):
        form = JoinForm()
        content = {'form': form}
        return render(request, 'manager/join.html', content)

    def post(self, request):
        form = JoinForm(request.POST, request.FILES)
        if form.is_valid():
            if form.validate():
                # 회원가입 성공하면 완성된 폼 보여주기
                return render(request, 'manager/join.html', {'form': form})
        return redirect('join')


class CompanyView(View):

    def get(self, request, company_id):
        if request.session.get('company') == company_id:
            try:
                company = get_object_or_404(Company, pk=company_id)
                return render(request, 'manager/company.html', {'company': company })
            except Exception as err:
                print(err)
                return redirect('logout')
        return redirect('index')
        

class ManageView(View):

    def get(self, request):
        if request.session.get('admin') == "admin":
            companyList = Company.objects.all().select_related().order_by('-id')

            paginator = Paginator(companyList, 5)
            page = request.GET.get('page')
            companies = paginator.get_page(page)

            content = {
                'companies': companies,
            }
            return render(request, 'manager/manage.html', content)
        return redirect('index')


class ManageUpdateView(View):

    def get(self, request, company_id):
        
        if request.session.get('admin') == "admin": # 관리자만 접근 가능
            try:
                company = Company.objects.select_related().get(id=company_id)
            except Exception:
                raise Http404("존재하지 않는 회원입니다.")

            img_1 = img_2 = ""
            if company.img1 is not None:
                img_1 = company.img1.img
            if company.img2 is not None:
                img_2 = company.img2.img

            form = CompanyUpdateForm({
                'name': company.name, 'phone': company.phone, 'business_name': company.business_name,
                'img1': img_1, 
                'img2': img_2,
            })

            return render(request, 'manager/company_update.html', 
            {'company_id': company.id, 'form': form})
        return redirect('manage')

        
    def post(self, request, company_id):
        if request.session.get('admin') == "admin":
            form = CompanyUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                form.validate(company_id)
                return redirect('manage')
            raise Http404("회원 정보가 업데이트 되지 않았습니다.")
        return redirect('index')


class ManageDeleteView(View):

    def get(self, request, company_id):
        if request.session.get('admin') == "admin":
            delete_images('1', company_id)
            delete_images('2', company_id)
            try:
                company = get_object_or_404(Company, pk=company_id)
                company.delete()
            except Exception as err:
                print(err)
                raise Http404("회원이 삭제되지 않았습니다.")
            return redirect('manage')
        return redirect('index')


def logout(request):
    session_admin = request.session.get('admin')
    session_company = request.session.get('company')
    if session_admin:
        del (request.session['admin'])
    if session_company:
        del (request.session['company'])
    return redirect('index')


class ImageDeleteView(View):

    def post(self, request):
        if request.session.get('admin') == "admin":    # 관리자가 POST로 접속해야만 접근 가능
            company_id = request.POST['company__id']
            option = request.POST['option']

            result = delete_images(option, company_id)

            if result == 'COMPLETE':
                return redirect('manage_update', company_id)
            elif result == 'UNDONE' or result == 'ERROR':
                return redirect('manage')
        return redirect('index')    # 관리자가 아니거나, 세션이 만료되었을 경우



def delete_images(option, company_id):
    try:
        company = get_object_or_404(Company, pk=company_id)
        if (option == '1' and company.img1 is not None) or (option == '2' and company.img2 is not None):
            # get image instance
            if option == '1':
                image = CompanyImg.objects.get(img=company.img1.img)
            elif option == '2':
                image = CompanyImg.objects.get(img=company.img2.img)
                
            # delete file in local directory
            image_path = str(image.img)
            basic_path = str(MEDIA_URL).replace('/', '', 1)
            file_path = urljoin(basic_path, image_path)
            if os.path.exists(file_path):
                os.remove(file_path)

            # remove connection(ForeignKey) and delete image instance
            if option == '1': company.img1 = None
            elif option == '2': company.img2 = None
            image.delete()
            return 'COMPLETE'

    except Exception as err:
        print(err)
        return 'ERROR'
    return 'UNDONE'


class ChangeInfoView(View):
    
    def get(self, request, info, company_id):
        if info == 'email':
            return render(request, 'manager/change_info.html', 
            {'form': ChangeEmailForm(), 'email': 'email', 'company_id': company_id})
        elif info == 'password':
            return render(request, 'manager/change_info.html', 
            {'form': ChangePasswordForm(), 'password': 'password', 'company_id': company_id})
        else:
            return redirect('company', company_id)


    def post(self, request, info, company_id):
        if info == 'email':
            form = ChangeEmailForm(request.POST)
        elif info == 'password':
            form = ChangePasswordForm(request.POST)
        else:
            return redirect('change_info', info, company_id)    # 빈 폼을 반환
        if form.is_valid():
            form.validate(company_id)
            return redirect('company', company_id)

        
