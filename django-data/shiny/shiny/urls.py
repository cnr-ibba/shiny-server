"""shiny URL Configuration

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

from django.contrib import admin
from django.urls import include, path
from serve.views import IndexView, ShinyAppListView, ShinyAppView, auth

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("auth/", auth),
    path("admin/", admin.site.urls),
    path("markdownx/", include("markdownx.urls")),
    # https://docs.djangoproject.com/en/2.2/topics/auth/default/#module-django.contrib.auth.views
    path("accounts/", include("django.contrib.auth.urls")),
    path("applications/", ShinyAppListView.as_view(), name="applications"),
    path("applications/<slug:slug>/", ShinyAppView.as_view(), name="shinyapp"),
]
