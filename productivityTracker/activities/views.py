from django.shortcuts import render


def index(request):
    context = {'msg': 'Well....work hard.'}
    return render(request, 'activities/index.html', context)
