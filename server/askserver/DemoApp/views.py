from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json #import the json module to parse json data
from .data import albums #importing the album data from the local data module


# a function to handle GET requests for fetching all albums
#========================================================================================================================
@require_http_methods(["GET"])
def get_albums(request):
    #returns all albums as a json response. `safe=False` is used because albums is a list, not a dictionary
    return JsonResponse(albums, safe=False)
#========================================================================================================================


#function to handle POST requests for adding a new album
#========================================================================================================================
@csrf_exempt
@require_http_methods(["POST"])
def post_albums(request):
    # attempt to parse the json data from the request 
    try:
        new_album = json.loads(request.body)
          # append the new album to the list of existing albums
        albums.append(new_album)
        # return the new album as a json response with HTTP status 201
        return JsonResponse(new_album, status=201)
    except json.JSONDecodeError:
        # if json parsing fails, return an error response with HTTP status 400 (Bad Request)
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
#========================================================================================================================
    

# a function to handle GET requests for fetching a single album by its ID
#========================================================================================================================
@require_http_methods(["GET"])
def get_album_by_id(request, id):
    # attempt to find the album in the list by its ID. Returns None if not found
    album = next((album for album in albums if album["ID"] == id), None)
    # if the album is found, return it as a JSON response
    if album:
        return JsonResponse(album)
    # if the album is not found, return a JSON response with an error message (missing status code)
        # it appears there's an error here: should return a specific status such as status=404 for erroe
    else:
        return JsonResponse({'message': 'Album not found'}, status=404)
#========================================================================================================================
    

# a function to get just the artist name using id
#========================================================================================================================
@require_http_methods(["GET"])
def get_artist_by_id(request, id):
    # attempt to find the artist in the list by album ID. return none if not found
    artist_info = next((album for album in albums if album["ID"] == id), None)
    # if the artist is found, return the artist name as json response
    if artist_info:
        return JsonResponse({'Artist': artist_info['Artist']})
    else:
        # if the artist is not found, return a json response with an error message and status code 404
        return JsonResponse({'message': 'Artist not found'}, status=404)    
#========================================================================================================================
    

#a function to get the album details of the cheapest album in the data structure
#========================================================================================================================
@require_http_methods(["GET"])
def get_cheapest_album(request):
    # find the album with the lowest price
    cheapest_album = min(albums, key=lambda x: float(x["Price"]))
    #return the album details of the album with the lowest price
    return JsonResponse(cheapest_album)
#========================================================================================================================


#a function to get the album details of the most expensive album in the data structure
#========================================================================================================================
@require_http_methods(["GET"])
def get_most_expensive_album(request):
    # find the album with the highest price
    most_expensive_album = max(albums, key=lambda x: float(x["Price"]))
    #return the album details of the most expensive album
    return JsonResponse(most_expensive_album)
#========================================================================================================================