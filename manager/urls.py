from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('join/', JoinView.as_view(), name="join"),
    path('manage/', ManageView.as_view(), name="manage"),
    path('company/<int:company_id>', CompanyView.as_view(), name="company"),
    path('manage/update/<int:company_id>', ManageUpdateView.as_view(), name="manage_update"),
    path('manage/delete/<int:company_id>', ManageDeleteView.as_view(), name="manage_delete"),
    path('company/<str:info>/<int:company_id>', ChangeInfoView.as_view(), name="change_info"),
    path('logout/', logout, name="logout"),
    path('imageout/', ImageDeleteView.as_view(), name="delete_image"),
]


