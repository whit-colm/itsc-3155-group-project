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
# from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from asapp import views

'''
# Not used. left around just in case.
def not_implemented(request, threadID=None, msgID=None, tag=None, reportID=None):
    if request.accepts('application/json'):
        return not_implemented_JSON(request, threadID, msgID, tag, reportID)

    text= f'<h1>501 NOT IMPLEMENTED.</h1><p>Here&#x2019s what we got:<br><ul><li>Thread ID: <code>{threadID}</code></li><li>Message ID: <code>{msgID}</code></li><li>Tag: <code>{tag}</code></li><li>Report ID: <code>{reportID}</code></li></ul></p>'
    return HttpResponse(text, status=501)
'''

def not_implemented(request, threadID=None, msgID=None, tag=None, reportID=None):
    return JsonResponse({"method":request.method, "threadID":threadID,"msgID":msgID,"tag":tag,"reportID":reportID}, safe=False, status=501)

urlpatterns = [
    # This just, doesn't work. Probably for the best.
    # path('admin/', admin.site.urls),

    path('objs/profile/', views.get_user_profile, name='user_profile'),
    path('objs/tags/', views.get_all_tags, name='get_all_tags'),
    path('objs/tags/new/', views.create_tag, name='create_tag'),
    path('objs/tags/<str:tag>/', views.delete_tag, name='delete_tag'),
    path('objs/reporttags/', views.get_report_tags, name='get_report_tags'),

    path('reports/', views.get_reports, name='get_reports'),
    path('reports/new/', views.create_report, name='create_report'),
    path('report/<uuid:reportID>/', views.get_report_by_id, name='get_report_by_id'),
    path('report/<uuid:reportID>/hide/', views.toggle_message_visibility, name='toggle_message_visibility'),

    path('threads/', views.get_threads, name='get_threads'),
    path('threads/new/', views.create_thread, name='create_thread'),
    path('thread/<uuid:threadID>/', not_implemented),
    path('thread/<uuid:threadID>/award/', not_implemented),
    path('thread/<uuid:threadID>/new/', not_implemented),
    path('thread/<uuid:threadID>/<uuid:msgID>/vote/', not_implemented),

    path('auth/oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    #path('auth/dummy, not_implemented)
]