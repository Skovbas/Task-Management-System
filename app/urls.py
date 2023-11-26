from django.urls import path
from django.conf.urls.i18n import set_language

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signUp', views.signUp, name="signUp"),
    path('login', views.loginview, name="login"),
    path('logout', views.logoutview, name="logout"),
    path('NewTask', views.taskCreation, name="task"),
    path('taskPage/<int:id>', views.taskPage, name="taskPage"),
    path('profile/<int:id>', views.userPage, name="profile"),
    path('profileUpdate', views.updateUserInfo, name='updateUserInfo'),

    
    #language urls
    path('i18n/setlang/', set_language, name='set_language'),
]
