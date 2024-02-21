from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def home_view(request):
    return HttpResponse("Hello, Django!")

def new_page(request):
    return HttpResponse("this is a new page")



home_view('')
new_page('')