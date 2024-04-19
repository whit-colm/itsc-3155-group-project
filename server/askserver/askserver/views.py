from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Report
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from askserver.models import User, Thread, Tag
import base64


@login_required
def get_user_profile(request):
    user = request.user
    if user:
        user_data = {
            "uid": user.uid,
            "displayname": base64.b64encode(user.displayname.encode()).decode() if user.displayname else "",
            "pronouns": base64.b64encode(user.pronouns.encode()).decode() if user.pronouns else "",
            "permissions": user.permissions,
            "threads": [str(thread.id) for thread in Thread.objects.filter(author=user)],
            "tags": [tag.name for tag in Tag.objects.filter(user=user)]  
        }
        return JsonResponse(user_data, safe=False, status=200)
    else:
        return JsonResponse({"message": "User not found"}, status=401)
    

from .models import Tag

def get_all_tags(request):
    tags = Tag.objects.all()
    tag_list = [tag.name for tag in tags]
    return JsonResponse({"tags": tag_list}, safe=False, status=200)



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Tag
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tag(request):
    
    if request.user.permissions < 4:
        return JsonResponse({"permission": 4, "message": "Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN)

    try:
        tag_data = request.data
        new_tag_name = tag_data.get('tag')
        if not new_tag_name:
            return JsonResponse({"message": "Missing 'tag' field"}, status=status.HTTP_400_BAD_REQUEST)

        new_tag, created = Tag.objects.get_or_create(name=new_tag_name)
        if not created:
            return JsonResponse({"message": "Tag already exists"}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({"tag": new_tag.name}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return JsonResponse({"message": "JSON could not be parsed"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tag(request, tag):
    if request.user.permissions < 4:
        return JsonResponse({"permission": 4, "message": "Insufficient permissions"}, status=status.HTTP_403_FORBIDDEN)

    try:
        tag_to_delete = Tag.objects.get(name=tag)
        tag_to_delete.delete()
        return JsonResponse({"tag": tag}, status=status.HTTP_200_OK)
    except Tag.DoesNotExist:
        return JsonResponse({"tag": tag, "message": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_report_tags(request):
    report_tags = [
        "Suspected violation of academic integrity",
        "Offensive or inappropriate behavior",
        "Hate speech",
        "Spam",
        "Promotion of illegal activities",
        "Something else"
    ]

    return JsonResponse({"tags": report_tags}, safe=False, status=200)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reports(request):
    
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



from .models import Report, Message, User
import uuid

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_report(request):
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
    


from .models import Report

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_report_by_id(request, reportID):
    
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
def toggle_message_visibility(request, reportID):
    
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
    
    

@api_view(['GET'])
def get_threads(request):
    
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 20))
    tags = request.GET.get('tags')
    limit = max(1, min(limit, 100))  
    query = Thread.objects.order_by('-date')

    if tags:
        tag_list = tags.split(',')
        query = query.filter(tags__name__in=tag_list).distinct()

    threads = query[offset:offset + limit]
    thread_list = []
    for thread in threads:
        last_interaction = thread.messages.filter(hidden=False).order_by('-date').first()

        last_interaction_data = {
            "id": str(last_interaction.id),
            "author": {
                "uid": last_interaction.author.uid,
                "displayname": base64.b64encode(last_interaction.author.displayname.encode()).decode(),
                "pronouns": base64.b64encode(last_interaction.author.pronouns.encode()).decode(),
            },
            "date": last_interaction.date.timestamp(),
            "bodyshort": base64.b64encode(last_interaction.body[:32].encode()).decode(),
        } if last_interaction else None

        thread_list.append({
            "threadID": str(thread.id),
            "author": {
                "uid": thread.author.uid,
                "displayname": base64.b64encode(thread.author.displayname.encode()).decode(),
                "pronouns": base64.b64encode(thread.author.pronouns.encode()).decode(),
            },
            "title": base64.b64encode(thread.title.encode()).decode(),
            "bodyshort": base64.b64encode(thread.messages.first().body[:64].encode()).decode(),
            "date": thread.date.timestamp(),
            "tags": [tag.name for tag in thread.tags.all()],
            "lastinteraction": last_interaction_data
        })

    return JsonResponse({"threads": thread_list}, safe=False, status=200)

   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_thread(request):
    try:
        title = base64.b64decode(request.data.get('title')).decode('utf-8') if request.data.get('title') else None
        body = base64.b64decode(request.data.get('body')).decode('utf-8') if request.data.get('body') else None
        anonymous = request.data.get('anonymous', False)
        tags = request.data.get('tags', [])

        if not title or not body or not tags:
            return JsonResponse({"message": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        tag_objects = []
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag)

        thread_author = request.user if not anonymous else None
        thread = Thread.objects.create(
            title=title,
            author=thread_author
        )
        thread.tags.set(tag_objects)

        message = Message.objects.create(
            thread=thread,
            author=thread_author,
            body=body,
            date=timezone.now()
        )

        thread_data = {
            "thread": {
                "title": base64.b64encode(title.encode()).decode(),
                "anonymous": anonymous,
                "question": {
                    "id": str(message.id),
                    "threadID": str(thread.id),
                    "author": {
                        "uid": request.user.uid if not anonymous else "anonymous",
                        "displayname": base64.b64encode(request.user.displayname.encode()).decode() if not anonymous else "anonymous",
                        "pronouns": base64.b64encode(request.user.pronouns.encode()).decode() if not anonymous else ""
                    },
                    "date": int(message.date.timestamp()),
                    "votes": 0,
                    "reply": None,
                    "content": base64.b64encode(body.encode()).decode(),
                    "hidden": False
                },
                "responses": [],
                "communityAward": None,
                "authorAward": None,
                "instructorAward": None,
                "tags": [tag.name for tag in tag_objects]
            }
        }

        return JsonResponse(thread_data, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({"message": "Error processing your request"}, status=status.HTTP_400_BAD_REQUEST)

