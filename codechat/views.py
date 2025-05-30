from django.http import HttpResponse

def index(request):
    return HttpResponse("Collaborative Coding + Video Chat Server is running!")