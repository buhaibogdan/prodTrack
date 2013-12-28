from django.shortcuts import render


def index(request):
    context = {'msg': 'basic stuff'}
    return render(request, 'index.html', context)