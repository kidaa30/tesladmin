from django.http import HttpResponse
from django.shortcuts import render

def static(request, path):
    return HttpResponse('123')
