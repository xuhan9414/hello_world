"""webplat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve

from app_login import views as view_login
from app_assist import urls as assist_urls
# from app_ci import urls as ci_urls
# from app_data_analyse import urls as app_data_analyse_urls
from app_subject import urls as subject_urls

urlpatterns = [
    url('admin/', admin.site.urls),

    url(r'^$' , view_login.log_page),
    url(r'^login/' , view_login.login, name='login'),
    # url(r'^login_hw/' , view_login.login_hw, name='login_hw'),
    url(r'^index/' , view_login.index, name='index'),

    url(r'^subject/', include(subject_urls)),
    url(r'^assist/', include(assist_urls)),

    url(r'^probeMedias/(?P<path>.*)$', serve,  #设置根目录
        {'document_root': 'E:\webplatform_data\ci\output_data'}),

]