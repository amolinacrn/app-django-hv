from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/autenticacion/logear")
def home(request):
    return render(request, "contenido_HV.html")
