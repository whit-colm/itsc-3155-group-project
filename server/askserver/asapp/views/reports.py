from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
#from django.contrib.auth.decorators import login_required
from asapp.models import User, Thread, Tag, Report, Message, ReportTag
import base64, uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from asapp.b64url_enhancement import check_base64

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reports(request):
    
    if not request.user.permissions >> 2:
        return JsonResponse({"permission": 4, "message": "Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN)

    try:
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))
        limit = max(1, min(limit, 50))  

        reports = Report.objects.all().order_by('-date')
        paginator = Paginator(reports, limit)
        page_obj = paginator.get_page(offset // limit + 1)

        reports_data = []
        for report in page_obj:
            reports_data.append(report.as_api())

        return JsonResponse({"reports": reports_data}, safe=False, status=status.HTTP_200_OK)
        
    except ValueError:
        return JsonResponse({"message": "Invalid input, unable to process the request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reports_new(request):
    data = request.data
    message_id = data.get('messageID')
    reasons = data.get('reason')
    comment = data.get('comment', '')

    if not message_id or not reasons:
        return JsonResponse({"message": "Required fields 'messageID' or 'reason' missing"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        r_msg = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return JsonResponse({"message": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        filtered_reasons = []
        for reason in reasons:
            rt = ReportTag.objects.get(name=reason)
            filtered_reasons.append(rt)
    except ReportTag.DoesNotExist:
        return JsonResponse({"message": "Report tag is invalid"}, status=status.HTTP_400_BAD_REQUEST)
    
    c = None
    if comment and check_base64(comment):
        c = comment
    elif comment and not check_base64(comment):
        return JsonResponse({"message": "Malformed comment base64"}, status=status.HTTP_400_BAD_REQUEST)

    report = Report.objects.create(
        message=r_msg,
        author=request.user,
        comment=c
    )
    report.reason.set(filtered_reasons)

    try:
        return JsonResponse({"report": report.as_api()}, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_PPARAM(request, reportID):
    
    if not request.user.permissions >> 2:
        return JsonResponse({"permission": 4, "message": "Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN)

    try:
        
        uuid.UUID(reportID)
        report = Report.objects.get(id=reportID).as_api()

        return JsonResponse({"report": report}, status=status.HTTP_200_OK)
    except Report.DoesNotExist:
        return JsonResponse({"id": reportID, "message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return JsonResponse({"message": "Invalid report ID"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_PPARAM_hide(request, reportID):
    
    if request.user.permissions < 4:
        return JsonResponse({"permission": 4, "message": "Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN)

    try:
        
        uuid.UUID(reportID)
        report = Report.objects.get(id=reportID)
        
        
        hide = request.data.get('hide')
        if hide is None:
            return JsonResponse({"message": "Required JSON parameter 'hide' missing"}, status=status.HTTP_400_BAD_REQUEST)

        
        if report.message.hidden != hide:
            report.message.hidden = hide
            report.message.save()
            action = "hidden" if hide else "unhidden"
            return JsonResponse({"message": f"Message has been {action} successfully."}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"message": "No change in message visibility needed."}, status=status.HTTP_200_OK)

    except Report.DoesNotExist:
        return JsonResponse({"id": reportID, "message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return JsonResponse({"message": "Invalid report ID"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
