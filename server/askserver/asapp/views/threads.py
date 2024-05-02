from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
#from django.contrib.auth.decorators import login_required
from asapp.models import User, Thread, Tag, Report, Message
import base64, uuid, hashlib
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

def anonymize_and_hide(jsonobject, user):
    """Performs the necessary logic to redact information per-user
    This anonimyzes the author in cases where the requester does not
    have the privliges to de-anonymize them, and hides threads marked as
    hidden.
    """
    jotype = jsonobject['_METADATA'] 


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

        # Ugly edge case code if the last interaction was:
        # 1. By the OP of the thread who
        # 2. Posted anonymously and is being req'd by
        # 3. A user who cannot de-anonymize
        showAnonymous = ((last_interaction.author.uid == thread.author) and thread.anonymous and not request.user.permissions >> 2 )
        last_interaction_data = {
            "id": str(last_interaction.id),
            "author": {
                "uid": last_interaction.author.uid if not showAnonymous else hashlib.sha3_224().update(last_interaction.author.uid),
                "displayname": last_interaction.author.displayname,
                "pronouns": last_interaction.author.pronouns
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

    return JsonResponse({"threads": thread_list}, safe=False, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def threads_new(request):
    print(request.data)
    # Unmarhsal the data, and 400 if key fields are missing.
    t = request.data.get('title')
    b = request.data.get('body')
    a = request.data.get('anonymous', False)
    # Tags still need to be checked if in-db. No custom tags.
    g_candidates = request.data.get('tags', [])
    if not t or not b or not g_candidates:
        return JsonResponse({"message": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    # TODO: In a perfect world, we would have some kind of tool to make sure
    #       a user isn't spamming POST. But I'm on a deadline
    #       (if I could seriously get into this, I'd do it all in go anyway)

    # Now we have to parse the data and commit it to the database
    # if this fails, then we return a 400 if the client was stupid
    # or a 500 if we were.
    try:
        g = []
        for tag_name in g_candidates:
            tag = Tag.objects.get(name=tag_name)
            g.append(tag)

        # The only vital things to a Thread is title, anonymous, and tags
        # the rest is determined by the Message with the question bit set
        thread = Thread.objects.create(
            title=t,
            anonymous=a,
        )
        thread.tags.set(g)

        # All other fields which a thread may have are, in fact, simply
        # attributes of the Message where question=True.
        message = Message.objects.create(
            thread=thread,
            author=request.user,
            body=b,
            date=timezone.now(),
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
        return JsonResponse(thread.as_api(), status=status.HTTP_200_OK)
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