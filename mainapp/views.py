from django.shortcuts import render

def home(request):
    return render(request, 'index-2.html')