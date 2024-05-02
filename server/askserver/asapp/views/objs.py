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
def objs_profile(request):
    """Gets the profile of the current user
    Given an authenticated request, returns information of the user object
    associated with the token
    """
    try:
        u = request.user
        if u:
            user_data = {
                "uid": u.uid,
                "displayname": u.displayname if u.displayname else "",
                "pronouns": u.pronouns if u.pronouns else "",
                "permissions": u.permissions,
                "threads": [str(thread.id) for thread in Thread.objects.filter(author=u)],
                "tags": [ tag for tag in u.tags.all()]
            }
            return JsonResponse(user_data, safe=False, status=200)
        else:
            return JsonResponse({"message": "No user associated with token. How did that happen?"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def objs_tags(request):
    """Lists all available tags
    This does not check for authentication.
    """
    tags = Tag.objects.all()
    tag_list = [tag.name for tag in tags]
    return JsonResponse({"tags": tag_list}, safe=False, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def objs_tags_new(request):
    if not request.user.permissions >> 2:
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
def objs_tags_PPARAM(request, tag):
    if not request.user.permissions >> 2:
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
def objs_reporttags(request):
    report_tags = [
        "Suspected violation of academic integrity",
        "Offensive or inappropriate behavior",
        "Hate speech",
        "Spam",
        "Promotion of illegal activities",
        "Something else"
    ]

    return JsonResponse({"tags": report_tags}, safe=False, status=200)