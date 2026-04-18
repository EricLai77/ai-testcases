"""
URL configuration for server_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from server_func import views
from django.urls import path
from server_func.views import UserRegistrationView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    #configure system
    path('allConfigInfo/', views.all_project_config),
    path('createConfig/', views.create_config_info),
    path('editConfig/', views.edit_config_info),
    path('deleteConfig/', views.delete_config_info),
    #login & registeration system
    path('userLogin/', views.user_login),
    path('userLogout/', views.user_logout),#你好
    path('register/', UserRegistrationView.as_view(), name='register'),
    #document sysytem
    path('mydocuments/', include('mydocuments.urls')),
    #ai api test
    path('deepseek_model', views.deepseek_model),
    path('deepseek_model/', views.deepseek_model),
    path('zhipu_model/', views.zhipu_model),
    path('zhipu_model', views.zhipu_model),
    #ai generated testcases
    path('generate_testcase/', views.generate_testcase),
    path('generate_testcase', views.generate_testcase),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 👈 关键配置

