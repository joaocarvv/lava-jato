from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente, Carro
import re

TEMPLATE_CLIENTES = 'clientes.html'

def clientes(request):
    if request.method == 'GET':
        return render(request, TEMPLATE_CLIENTES)
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros= request.POST.getlist('carro')
        placas= request.POST.getlist('placa')
        anos= request.POST.getlist('ano')

        cliente = Cliente.objects.filter(cpf=cpf)



        if cliente.exists():
            return render(request, TEMPLATE_CLIENTES, {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf': cpf, 'carros': zip(carros,placas,anos)})
           

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, TEMPLATE_CLIENTES, {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'carros': zip(carros,placas,anos)})


        cliente= Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )
        cliente.save()

        for x,y,z in zip(carros,placas,anos):
            carro = Carro(
                carro = x,
                placa = y,
                ano = z,
                cliente = cliente
            )
            carro.save()
        


        return HttpResponse(f'{carros}, {placas}, {anos}')