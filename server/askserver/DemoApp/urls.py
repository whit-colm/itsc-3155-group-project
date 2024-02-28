from django.urls import path
from . import views

urlpatterns = [

    path('albums/', views.get_albums, name='get_albums'),
    path('albums/<str:id>/', views.get_album_by_id, name='get_album_by_id'),
    path('albums/', views.post_albums, name='post_albums'),
    path('album/artist/<str:id>/', views.get_artist_by_id, name='get_artist_by_id'),
    path('album/cheapest/', views.get_cheapest_album, name='get_cheapest_album'),
    path('album/expensive/', views.get_most_expensive_album, name='get_most_expensive_album'),
]
