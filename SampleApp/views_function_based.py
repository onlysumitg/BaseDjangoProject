from django.http import HttpResponse

from django.shortcuts import render


# Create your views here.
def function_based_view_1(request):
    """
    http://127.0.0.1:8000/en/sample/functionview1
    """
    return HttpResponse("A basic view. Returns a string.")
