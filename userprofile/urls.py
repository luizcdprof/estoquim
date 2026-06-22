from django.urls import path
from userprofile.views import userprofile_login, userprofile_view, userprofile_list, userprofile_register

urlpatterns = [
    path('login/', userprofile_login, name='userprofile_login'),
    path('view/', userprofile_view, name='userprofile_view'),
    path('list/', userprofile_list, name='userprofile_list'),
    path('register/', userprofile_register, name='userprofile_register_view')
]