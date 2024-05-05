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
from django.urls import include, path

from asapp import views

from django.http import JsonResponse
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
    path('admin/', admin.site.urls),

    path('objs/profile/', views.objs_profile, name='objs_profile'),
    path('objs/tags/', views.objs_tags, name='objs_tags'),
    path('objs/tags/new/', views.objs_tags_new, name='objs_tags_new'),
    path('objs/tags/<str:tag>/', views.objs_tags_PPARAM, name='objs_tags_PPARAM'),
    path('objs/reporttags/', views.objs_reporttags, name='objs_reporttags'),

    path('reports/', views.reports, name='reports'),
    path('reports/new/', views.reports_new, name='reports_new'),
    path('report/<uuid:reportID>/', views.report_PPARAM, name='reports_PPARAM'),
    path('report/<uuid:reportID>/hide/', views.report_PPARAM_hide, name='reports_PPARAM_hide'),

    path('threads/', views.threads, name='threads'),
    path('threads/new/', views.threads_new, name='threads_new'),
    path('thread/<uuid:threadID>/', views.thread_PPARAM, name='thread_PPARAM'),
    path('thread/<uuid:threadID>/award/', views.thread_PPARAM_award, name='thread_PPARAM_award'),
    path('thread/<uuid:threadID>/new/', views.thread_PPARAM_new, name='thread_PPARAM_new'),
    path('thread/<uuid:threadID>/<uuid:msgID>/vote/', views.thread_PPARAM_PPARAM_vote, name='thread_PPARAM_PPARAM_vote'),

    path('auth/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    #path('auth/dummy, not_implemented)
]