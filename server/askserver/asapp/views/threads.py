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
    # Unmarhsal the data, and 400 if key fields are missing.
    title = request.data.get('title') if request.data.get('title') else None
    body = request.data.get('body') if request.data.get('body') else None
    anonymous = request.data.get('anonymous', False)
    tags = request.data.get('tags', [])
    if not title or not body or not tags:
        return JsonResponse({"message": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    # TODO: In a perfect world, we would have some kind of tool to make sure
    #       a user isn't spamming POST. But I'm on a deadline
    #       (if I could seriously get into this, I'd do it all in go anyway)

    # Now we have to parse the data and commit it to the database
    # if this fails, then we return a 400 if the client was stupid
    # or a 500 if we were.
    try:
        tag_objects = []
        for tag_name in tags:
            tag, created = Tag.objects.get(name=tag_name)
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
    except Tag.DoesNotExist:
        return JsonResponse({"message": "No such tag(s)"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # The object has been successfully put into the DB, now we relay it to the user
    # if something goes wrong here, we still want to send a 2XX as the tx *was*
    # successful. It's just that for some reason there was a cock-up in 
    # encoding the JSON.
    try:
        thread_data = {
            "thread": {
                "title": title,
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
        return JsonResponse({"message": str(e)}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def thread_PPARAM(request):
    return JsonResponse({"message": "What an asshole!"}, status=status.HTTP_501_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def thread_PPARAM_award(request):
    return JsonResponse({"message": "What an asshole!"}, status=status.HTTP_501_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def thread_PPARAM_new(request):
    return JsonResponse({"message": "What an asshole!"}, status=status.HTTP_501_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def thread_PPARAM_PPARAM_vote(request):
    return JsonResponse({"message": "What an asshole!"}, status=status.HTTP_501_INTERNAL_SERVER_ERROR)