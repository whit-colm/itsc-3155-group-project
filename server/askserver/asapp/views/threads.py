from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
#from django.contrib.auth.decorators import login_required
from asapp.models import User, Thread, Tag, Report, Message
import base64, uuid, hashlib, binascii
from rest_framework.decorators import api_view, permission_classes
from django.db import models
from django.db.models import Max, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from asapp.b64url_enhancement import check_base64, b64url_encode_str, b64url_decode_str

def anonymize_and_hide(jsonobject: dict, user: User, messageThreadAnonymous=None, messageThreadOP=None):
    """
    Performs the necessary logic to redact information per-user
    
    This anonimyzes the author in cases where the requester does not
    have the privliges to de-anonymize them, and hides threads marked as
    hidden.

    Parameters
    ----------
    jsonobject
        The JSON being operated on. It should have a `_METADATA` key or else it will raise a KeyError
    user
        The User to censure for, checking permissions and identity.
    messageThreadAnonymous : bool, optional
        Set to true or false if the thread a given message belongs to was done anonymously.
        This is a small optimization to save unecessary calls to the DB. Do not use it unless you know what you are doing.
    messageThreadOP : optional
        The UID of the OP of the thread a message belongs to.
        This is a small optimization to save unecessary calls to the DB. Do not use it unless you know what you are doing.

    Returns
    -------
    result
        The censored JSON.

    Raises
    ------
    KeyError
        If the `_METADATA` wasn't understood or was empty.
    
    """
    # This is how we can make sure the correct operations are done
    jotype = jsonobject.get('_METADATA', {})
    user_permissions = user.permissions
    user_uid = user.uid

    if jotype == "message.askhole.api.dotfile.sh/v1alpha1":
        # Message anonimyzes:
        # - Author UID -> sha3_224(UID)
        # - Author displayname -> None
        # - Author pronouns -> dGhleS90aGVt
        # Message hides:
        # - Author UID -> HiddenMessageUser
        # - Author displayname -> None
        # - Author pronouns -> None
        # - Message body -> None
        # - Message votes -> None

        # Figure out if the thread was posted anonymously
        thread_anonymous = messageThreadAnonymous if messageThreadAnonymous is not None else Thread.objects.get(id=jsonobject['threadID']).anonymous
        # Figure out the author of the thread
        thread_author = messageThreadOP if messageThreadOP is not None else Thread.objects.get(id=jsonobject['threadID']).author.uid

        # match all 4 conditions:
        # 1. the thread was submitted anonymously
        # 2. the user does not have sufficient perms to de-anonymize
        # 3. the user is not the OP of the thread
        # 4. the message is from the OP of the thread
        if (thread_anonymous and not user.permissions >> 2 and (thread_author != user.uid) and thread_author == jsonobject['author']['uid']):
            jsonobject['author'].pop('displayname', None)
            jsonobject['author']['pronouns'] = "dGhleS90aGVt"
            a_uid = jsonobject['author']['uid']
            a_uid = hashlib.sha3_224(a_uid.encode()).hexdigest()
            jsonobject['author']['uid'] = f"sha3-224:{a_uid}"
        
        # Match all 3 conditions:
        # 1. the message is set hidden
        # 2. The user does not have sufficient perms to unhide
        # 3. the user is not the OP of the message
        message_hidden = jsonobject.get('hidden', False)
        # We use dictionary notation here as we need it to fail if there's no author.
        message_author = jsonobject['author']['uid']

        if (message_hidden and not user.permissions >> 1 and (message_author != user.uid)):
            jsonobject['author']['uid'] = "HiddenMessageUser"
            jsonobject['author'].pop('displayname', None)
            jsonobject['author'].pop('pronouns', None)
            jsonobject['body'] = ""
            jsonobject.pop('votes', None)
            jsonobject.pop('reply', None)

        return jsonobject


    elif jotype == "thread.askhole.api.dotfile.sh/v1alpha1":
        # Thread anonymizes:
        # 1. See messages
        # Thread hides:
        # 1. See messages
        # In short: we can just recursively call this on every message.

        # extract some values for optimization's sake
        thread_anonymous = jsonobject['anonymous']
        thread_author = jsonobject['question']['author']['uid']

        jsonobject['question'] = anonymize_and_hide(jsonobject['question'], user, thread_anonymous, thread_author)

        # Now we do so for all responses in the thread:
        for msg in jsonobject['responses']:
            anonymize_and_hide(msg, user, thread_anonymous, thread_author)
        return jsonobject

    elif jotype == "threadsummary.askhole.api.dotfile.sh/v1alpha1":
        # If a thread is hidden from the user, just remove it from the list
        # Anonymize thread/last interaction.

        for thread in jsonobject['threads']:
            # Remove the thread and go on to next one
            if (thread.get('hidden', False) and not user.permissions >> 1 and (thread['author']['uid'] != user.uid)):
                jsonobject['threads'].pop(thread, None)
                continue

            # Anonymize thread author
            # 1. Thread is set to anonymous
            # 2. User does not de-anonymize users
            # 3. User is not OP of thread
            if (thread.get('anonymous', False) and not user.permissions >> 2 and ((thread['author']['uid'] != user.uid))):
                thread['author'].pop('displayname', None)
                thread['author']['pronouns'] = "dGhleS90aGVt"
                a_uid = thread['author']['uid']
                a_hash_uid = hashlib.sha3_224(a_uid.encode()).hexdigest()
                thread['author']['uid'] = f"sha3-224:{a_hash_uid}"

                # Anonymize last interaction author
                # 1. Thread is set to anonymous
                # 2. User does not de-anonymize users
                # 3. User is not OP of thread
                # 4. Message is by OP of thread

                # Now, the estute among you will realize we did 3 of those,
                # i.e. only in this situation could a message ever be anonymous
                # so just do that fourth check
                if (a_uid == thread['lastinteraction']['author']['uid']):
                    thread['lastinteraction']['author']['uid'] = thread['author']['uid']
                    thread['lastinteraction']['author']['pronouns'] = thread['author']['pronouns']



        return jsonobject

    # If the passed object was none of these, then something has gone wrong.    
    else:
        if jotype is None:
            raise KeyError("No metadata was found for the JSON.")
        else:
            raise KeyError(f"Cannot anonimyze JSON object of metadata type `{jotype}`.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def threads(request):
    
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 20))
    tags = request.GET.get('tags')
    limit = max(1, min(limit, 100))
    query = Thread.objects.annotate(
        question_date=Max('messages__date', filter=Q(messages__question=True))
    ).order_by('-question_date')

    if tags:
        tag_list = tags.split(',')
        query = query.filter(tags__name__in=tag_list).distinct()

    threads = query[offset:offset + limit]
    thread_list = {
        "_METADATA": "threadsummary.askhole.api.dotfile.sh/v1alpha1",
        "threads": []
    }
    for thread in threads:
        # We want to get the most recent message in the thread that isn't hidden and isn't the question
        last_interaction = thread.messages.filter(question=False).filter(hidden=False).order_by('-date').first()

        # We decode the thread body to get the first couple characters,
        # then re-encode for transit.
        t_bodyshort = b64url_decode_str(thread.question_message.body)[:280]
        t_bodyshort = b64url_encode_str(t_bodyshort)

        last_interaction_data = None
        if last_interaction:
            l_bodyshort = b64url_decode_str(last_interaction.body)[:140]
            l_bodyshort = b64url_encode_str(l_bodyshort)

            last_interaction_data = {
                "id": str(last_interaction.id),
                "author": {
                    "uid": last_interaction.author.uid,
                    "displayname": last_interaction.author.displayname,
                    "pronouns": last_interaction.author.pronouns
                },
                "date": int(last_interaction.date.timestamp()),
                "bodyshort": l_bodyshort
            }

        thread_list['threads'].append({
            "threadID": str(thread.id),
            "author": {
                "uid": thread.author.uid,
                "displayname": thread.author.displayname,
                "pronouns": thread.author.pronouns
            },
            "title": thread.title,
            "bodyshort": t_bodyshort,
            "date": int(thread.date.timestamp()),
            "tags": list(thread.tags.values_list('name', flat=True)),
            "anonymous": thread.anonymous,
            "hidden": thread.hidden,
            "lastinteraction": last_interaction_data
        })

    return JsonResponse(anonymize_and_hide(thread_list, request.user), safe=False, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def threads_new(request):
    # Unmarhsal the data, and 400 if key fields are missing.
    t = request.data.get('title')
    b = request.data.get('body')
    a = request.data.get('anonymous', False)
    # Tags still need to be checked if in-db. No custom tags.
    g_candidates = request.data.get('tags', [])
    if not t or not b or not g_candidates:
        return JsonResponse({"message": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    if not (check_base64(t) and check_base64(b)):
        return JsonResponse({"message": "Fields not in URLSafe base64."}, status=status.HTTP_400_BAD_REQUEST)

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
def thread_PPARAM(request, threadID):
    try:
        requested_thread = Thread.objects.get(id=threadID)

        if requested_thread.hidden and not request.user.permissions >> 1:
            return JsonResponse({"permission": 2}, status=status.HTTP_403_FORBIDDEN)
        return JsonResponse(anonymize_and_hide(requested_thread.as_api(), request.user), status=200)
    except Thread.DoesNotExist:
        return JsonResponse({"id": str(threadID)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JsonResponse({"message": "What an asshole!"}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def thread_PPARAM_award(request, threadID):
    # Try to get the thread and message passed fromt their IDs.
    try:
        requested_thread = Thread.objects.get(id=threadID)
        msg_id = request.data.get('id')
        requested_message = Message.objects.get(msg_id)
    except Thread.DoesNotExist:
        return JsonResponse({"error": "InvalidThread", "uuid": str(threadID)}, status=status.HTTP_404_NOT_FOUND)
    except Message.DoesNotExist:
        return JsonResponse({"error": "InvalidMessage", "uuid": str(threadID)}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return JsonResponse({"message": "Could not retrieve message ID."})
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Now hand out the first available award (author -> instructor -> none)
    if (requested_thread.author.uid == request.user.uid):
        requested_thread.authoraward = requested_message
        requested_thread.save()
        return JsonResponse({"message": anonymize_and_hide(requested_message(), request.user), "award": "AuthorAward"},
            status=status.HTTP_200_OK)
    elif (request.user.permissions >> 1):
        requested_thread.instructoraward = requested_message
        requested_thread.save()
        return JsonResponse({"message": anonymize_and_hide(requested_message(), request.user), "award": "InstructorAward"},
            status=status.HTTP_200_OK)
    else:
        return JsonResponse({"permission": 2}, status=status.HTTP_403_FORBIDDEN)
    return JsonResponse({"message": "What an asshole!"}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def thread_PPARAM_new(request, threadID):
    # first check to make sure base64. This is as close as I get to db santization
    # if it's not, scream at user.
    if request.data.get('body', None) is None:
        return JsonResponse({"message": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    if not check_base64(request.data.get('body')):
        return JsonResponse({"message": "Fields not in URLSafe base64."}, status=status.HTTP_400_BAD_REQUEST)

    # First do a check to make sure the reply is valid
    try:
        reply_msg = None
        if request.data.get('reply', None) is not None:
            reply_msg = Message.objects.get(id=request.data.get('reply')) if not Message.objects.get(id=request.data.get('reply')).question else None
    except Message.DoesNotExist:
        return JsonResponse({"error": "InvalidMessage", "uuid": request.data.get('reply')}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return JsonResponse({"message": "Could not retrieve reply message ID."})
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        message = Message.objects.create(
                thread=Thread.objects.get(id=threadID),
                author=request.user,
                body=request.data.get('body'),
                date=timezone.now(),
                reply=reply_msg 
            )
    except Thread.DoesNotExist:
        return JsonResponse({"error": "InvalidThread", "uuid": str(threadID)}, status=status.HTTP_404_NOT_FOUND)
    except Message.DoesNotExist:
        return JsonResponse({"error": "InvalidMessage", "uuid": str(threadID)}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return JsonResponse({"message": "Could not retrieve message body."})
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({"message": message.as_api()})
    return JsonResponse({"message": "What an asshole!"}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def thread_PPARAM_PPARAM_vote(request, threadID, msgID):
    try:
        msg = Message.objects.get(msgID)
    except Message.DoesNotExist:
        return JsonResponse({"error": "InvalidMessage", "uuid": request.data.get('reply')}, status=status.HTTP_404_NOT_FOUND)
    
    voted = msg.voters.filter(user=request.user).exists()
    try:
        will_vote = request.data.get('vote')
    except KeyError:
        return JsonResponse({"message": "Could not retrieve vote status."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if will_vote:
        if voted:
            return JsonResponse({"delta": 0}, status=status.HTTP_200_OK)
        else:
            msg.voters.add(request.user)
            return JsonResponse({"delta": 1}, status=status.HTTP_200_OK)
    else:
        if voted:
            msg.voters.remove(request.user)
            return JsonResponse({"delta": -1}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"delta": 0}, status=status.HTTP_200_OK)

    return JsonResponse({"message": "What an asshole!"}, status=status.HTTP_501_NOT_IMPLEMENTED)