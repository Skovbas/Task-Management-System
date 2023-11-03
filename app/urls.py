from django.urls import path
from django.conf.urls.i18n import set_language

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signUp', views.signUp, name="signUp"),
    path('login', views.loginview, name="login"),
    path('logout', views.logoutview, name="logout"),
    
    #language urls
    path('i18n/setlang/', set_language, name='set_language'),
]
