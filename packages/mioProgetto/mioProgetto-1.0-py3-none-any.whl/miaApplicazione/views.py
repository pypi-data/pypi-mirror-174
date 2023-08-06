from django.shortcuts import render
from django.http import HttpResponse
from .models import Utenza

def index(_):
    return HttpResponse("Benvenuti nel progetto del gruppo ITIS")
   
def utenti(request):
    utenza = Utenza.objects.all()
    return render(request, 'utenti.html', {'utenza': utenza})

def inserimento(request):
    try:
        if request.method == 'POST' and request.POST.get('CF'):
            post = Utenza()
            post.CF = request.POST.get('CF')
            post.Nome = request.POST.get('Nome')
            post.Cognome = request.POST.get('Cognome')
            post.DataNascita = request.POST.get('DataNascita')
            post.save()
            return utenti(request)
        return render(request, 'inserimento.html')
    except Exception:
        return render(request,'inserimento.html')
