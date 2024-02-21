from django.urls import path
from DemoApp import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('newpage/', views.new_page, name='newpage'),

]