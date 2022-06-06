from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # return HttpResponse("Demo App")
    return render(request, template_name='index.html', context= {
        'name':'Hoang Van'
    })
# Create your views here.
