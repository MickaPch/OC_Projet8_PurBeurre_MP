from django.shortcuts import render

def home(request):
    """Home page"""
    

    return render(request, 'home/home.html', locals())