from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Report
from django.utils import timezone

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
