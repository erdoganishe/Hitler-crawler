from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
import json

from hitler_app.main_threaded import get_path

# Create your views here.
def home(request):
    return render(request, "index.html")

def hitler_set(request):
    if request.method == "GET":
        return HttpResponse("GEEET")
    elif request.method == "POST":
        jsonData = json.loads(request.body)
        jsonLink = jsonData["link"]

        responce = get_path(jsonLink, jsonData["isDB"])

        return JsonResponse(responce)