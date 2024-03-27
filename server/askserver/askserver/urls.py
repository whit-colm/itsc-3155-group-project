"""
URL configuration for askserver project.

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
from django.http import HttpResponse
from django.urls import path

def not_implemented(request):
    return HttpResponse(status=501)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('/objs/profile/', not_implemented),
    path('/objs/tags/new/', not_implemented),
    path('/objs/tags/{tags}/', not_implemented),
    path('/objs/reporttags/', not_implemented),

    path('/reports/', not_implemented),
    path('/reports/new/', not_implemented),
    path('/reports/{reportID}/', not_implemented),
    path('/reports/{reportID}/hide/', not_implemented),

    path('/threads/', not_implemented),
    path('/threads/new/', not_implemented),
    path('/threads/{threadID}/', not_implemented),
    path('/threads/{threadID}/award/', not_implemented),
    path('/threads/{threadID}/new/', not_implemented),
    path('/threads/{threadID}/{msgID}/vote/', not_implemented),
]