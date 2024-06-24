"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

import mysite.views as views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include([
        path("users/", views.CreateUsersView.as_view()),
        path("login/", views.LoginUserView.as_view()),
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path("test/", views.testAPI),
        path("test/login/", views.LoginView.as_view(), name="test_login")
    ])),
    path("api/blog/", include(("blog.urls","blog"), namespace="blog")),
    path("api/chat/", include(("chatapp.urls","chatapp"), namespace="chatapp")),
]

