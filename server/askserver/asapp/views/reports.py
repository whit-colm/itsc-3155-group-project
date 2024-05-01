from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
#from django.contrib.auth.decorators import login_required
from asapp.models import User, Thread, Tag, Report, Message
import base64, uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reports(request):
    
    if request.user.permissions < 4:
        return JsonResponse({"permission": 4, "message": "Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN)

    try:
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))
        limit = max(1, min(limit, 50))  

        reports = Report.objects.all().order_by('-date')
        paginator = Paginator(reports, limit)
        page_obj = paginator.get_page(offset // limit + 1)

        reports_data = [{
            "id": report.id,
            "message": {
                "id": report.message.id,
                "threadID": report.message.thread.id,
                "author": {
                    "uid": report.message.author.uid,
                    "displayname": report.message.author.displayname,
                    "pronouns": report.message.author.pronouns
                },
                "date": int(report.message.date.timestamp()),
                "votes": report.message.votes,
                "reply": None,
                "content": report.message.body,
                "hidden": report.message.hidden
            },
            "author": {
                "uid": report.author.uid,
                "displayname": report.author.displayname,
                "pronouns": report.author.pronouns
            },
            "date": int(report.date.timestamp()),
            "reason": report.reason,
            "comment": report.comment
        } for report in page_obj]

        return JsonResponse({"reports": reports_data}, safe=False, status=status.HTTP_200_OK)
        
    except ValueError:
        return JsonResponse({"message": "Invalid input, unable to process the request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reports_new(request):
    try:
        data = request.data
        message_id = data.get('messageID')
        reasons = data.get('reason')
        comment = data.get('comment', '')

        if not message_id or not reasons:
            return JsonResponse({"message": "Required fields 'messageID' or 'reason' missing"}, status=status.HTTP_400_BAD_REQUEST)

        
        try:
            message = Message.objects.get(id=uuid.UUID(message_id))
        except Message.DoesNotExist:
            return JsonResponse({"message": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

        
        if comment:
            comment = base64.b64decode(comment).decode('utf-8')

        
        report = Report.objects.create(
            message=message,
            author=request.user,  
            date=timezone.now(),
            reason=','.join(reasons),  
            comment=comment
        )

        report_data = {
            "id": str(report.id),
            "message": {
                "id": str(message.id),
                "threadID": str(message.thread.id),
                "author": {
                    "uid": message.author.uid,
                    "displayname": message.author.displayname,
                    "pronouns": message.author.pronouns
                },
                "date": int(message.date.timestamp()),
                "votes": message.votes,
                "reply": None,
                "content": message.body,
                "hidden": message.hidden
            },
            "author": {
                "uid": request.user.uid,
                "displayname": request.user.displayname,
                "pronouns": request.user.pronouns
            },
            "date": int(report.date.timestamp()),
            "reason": reasons,
            "comment": comment
        }

        return JsonResponse({"report": report_data}, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reports_PPARAM(request, reportID):
    
    if request.user.permissions < 4:
        return JsonResponse({"permission": 4, "message": "Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN)

    try:
        
        uuid.UUID(reportID)
        report = Report.objects.get(id=reportID)
        
        report_data = {
            "id": str(report.id),
            "message": {
                "id": str(report.message.id),
                "threadID": str(report.message.thread.id),
                "author": {
                    "uid": report.message.author.uid,
                    "displayname": report.message.author.displayname,
                    "pronouns": report.message.author.pronouns
                },
                "date": int(report.message.date.timestamp()),
                "votes": report.message.votes,
                "reply": None,
                "content": report.message.body,
                "hidden": report.message.hidden
            },
            "author": {
                "uid": report.author.uid,
                "displayname": report.author.displayname,
                "pronouns": report.author.pronouns
            },
            "date": int(report.date.timestamp()),
            "reason": report.reason.split(','),
            "comment": report.comment
        }
        return JsonResponse({"report": report_data}, status=status.HTTP_200_OK)
    except Report.DoesNotExist:
        return JsonResponse({"id": reportID, "message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return JsonResponse({"message": "Invalid report ID"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reports_PPARAM_hide(request, reportID):
    
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
