from django.http import HttpResponse


def home(request):
    greeting = getattr(request, 'custom_greeting', 'No greeting found')
    
    return HttpResponse(f"<h1>{greeting}</h1><p>Welcome to the home page!</p>")