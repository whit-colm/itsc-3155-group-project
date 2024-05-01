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
def threads(request):
    
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
def threads_new(request):
    try:
        title = request.data.get('title') if request.data.get('title') else None
        body = request.data.get('body') if request.data.get('body') else None
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
            author=thread_author,
            date=timezone.now()
        )
        thread.tags.set(tag_objects)

        message = Message.objects.create(
            thread=thread,
            author=thread_author,
            body=body,
            date=thread.date,
            question=True
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
        return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

