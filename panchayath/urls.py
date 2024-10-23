"""panchayath URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('index/',index,name="index"),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('detail_user/<int:user_id>/', profile_detail, name='profile_detail'),
    path('posts/<int:pk>/like',add_like_view,name="add-like"),
    path('posts/<int:pk>/comments/add',add_comment_view,name="add-comment"),
    path('comments/<int:pk>/remove/',remove_comment_view,name="removecomment"),
    # path('profiles/<int:pk>/coverpic/change/',change_cover_pic_view,name="coverpic-change"),
    path('',district,name='district'),
    path('thrissur/',thrissur,name='thrissur'),
    path('logout/', logout_view, name='logout'),
    path('history/', history_list_view, name='history-list'),
    path('services/', service_list, name='service_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
