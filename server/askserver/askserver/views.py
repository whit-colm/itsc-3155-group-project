from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Report
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import User, Thread, Tag
from django.core.exceptions import ObjectDoesNotExist
import base64

def get_reports(request):
   
    offset = request.GET.get('offset', 0)
    limit = request.GET.get('limit', 10)
     
    try:
        limit = max(1, min(int(limit), 50))
        offset = max(0, int(offset))
    except ValueError:
        
        limit = 10
        offset = 0
    
    reports = Report.objects.all().order_by('-date')
    paginator = Paginator(reports, limit)
    page_number = offset // limit + 1
    page_obj = paginator.get_page(page_number)
    
    reports_data = [{
        'id': report.id,
        'author': report.author.displayname,
        'date': report.date,
        'reason': report.reason,
        'comment': report.comment,
    } for report in page_obj]
    return JsonResponse(reports_data, safe=False)  

#############################################################

@login_required
def get_user_profile(request):
    try:
        user = request.user
        user_data = {
            "uid": user.uid,
            "displayname": base64.b64encode(user.displayname.encode()).decode(),
            "pronouns": base64.b64encode(user.pronouns.encode()).decode() if user.pronouns else None,
            "permissions": user.permissions,
            "threads": [str(thread.id) for thread in Thread.objects.filter(author=user)],
            "tags": [tag.name for tag in Tag.objects.filter(subscribed_users=user)]
        }
        return JsonResponse(user_data, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "User not found"}, status=404)

def unauthorized_response():
    return JsonResponse({"message": "No token associated with request"}, status=401)