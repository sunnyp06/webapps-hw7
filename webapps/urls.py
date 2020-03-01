"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from socialnetwork import views

urlpatterns = [
    path('', views.global_stream, name = 'home'),
    path('login', views.login_user, name = 'login'),
    path('logout', views.logout_user, name = 'logout'),
    path('register', views.register_user, name = 'register'),
    path('global', views.global_stream, name = 'global'),
    path('follower', views.follower_stream, name = 'follower'),
    path('profile', views.profile, name = 'profile'),
    path('profile/<int:profile_pk>', views.profile_pk, name = 'profile'),
    path('profile/<str:username>', views.profile_id, name = 'profile'),
    path('profile_picture/<str:username>', views.profile_picture, 
         name = 'profile_picture'),
    path('socialnetwork/refresh-global', views.refresh_global, name = "refresh_global"),
    path('socialnetwork/refresh-follower', views.refresh_follower, name = "refresh_follower"),
    path('socialnetwork/add-comment', views.add_comment, name = "add_comment"),
]
