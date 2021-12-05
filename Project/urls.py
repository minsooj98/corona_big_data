"""Project URL Configuration

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
from Web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.initFunc), 
    path('main1', views.main1Func),
    path('main2', views.main2Func),
    path('city1', views.seoulFunc),
    path('signup', views.signupFunc),
    path('insertmember', views.insertFunc),
    path('updatemember', views.updateFunc),
    path('login', views.login),
    path('memberlogin', views.loginFunc), 
    path('logout', views.logoutFunc),
    path('mypage', views.mypageFunc),
    path('check', views.checkFunc),
    path('lifestyle', views.lifestyleFunc),
    
    # path('graph', views.graphFunc),
    # path('graph2', views.graph2Func),
    # path('graph3', views.graph3Func), 
    # path('graph4', views.graph4Func),
    # path('graph5', views.graph5Func),
    # path('graph6', views.graph6Func),
    path('analysis', views.analysisFunc),
    path('save', views.saveFunc), 
    path('viewImage', views.viewImageFunc),
]
