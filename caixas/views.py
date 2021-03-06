# This Python file uses the following encoding: utf-8
# ANOTAÇÃO PARA USAR CARACTERES ESPECIAIS AQUI. (MESMO PARA ANOTAÇÕES.)
""" 
@edsonlb
https://www.facebook.com/groups/pythonmania/
"""

from django.shortcuts import render, HttpResponseRedirect
from datetime import datetime, date
from django.db.models import Q #Queries complexas
from caixas.models import Conta
from pessoas.models import Pessoa


def caixaListar(request):
    contas = Conta.objects.all()[0:10]

    return render(request, 'caixas/listaCaixas.html', {'contas': contas})


def caixaAdicionar(request):
    pessoas = Pessoa.objects.all().order_by('nome')

    return render(request, 'caixas/formCaixas.html', {'pessoas': pessoas})

def caixaSalvar(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '0')

        try:
            conta = Conta.objects.get(pk=codigo)
        except:
            conta = Conta()

        conta.pessoa_id = request.POST.get('pessoa_id', '1')
        conta.tipo = request.POST.get('tipo', '').upper()
        conta.descricao = request.POST.get('descricao', 'CONTA SEM DESCRIÇÃO').upper()
        conta.valor = request.POST.get('valor', '0.00').replace(',','.')
        conta.data = datetime.strptime(request.POST.get('data', ''), '%d/%m/%Y %H:%M:%S')

        conta.save()
    return HttpResponseRedirect('/caixas/')

def caixaPesquisar(request):
    if request.method == 'POST':
        textoBusca = request.POST.get('textoBusca', 'TUDO').upper()

        try:
            if textoBusca == 'TUDO':
                contas = Conta.objects.all()
            else:
                sql = ("select cc.* from caixas_conta cc inner join pessoas_pessoa pp on pp.id = cc.pessoa_id where pp.nome like '%s' or cc.descricao like '%s' order by data") % ('%%'+textoBusca+'%%', '%%'+textoBusca+'%%')
                contas = Conta.objects.raw(sql)
        except:
            contas = []

        return render(request, 'caixas/listaCaixas.html', {'contas': contas, 'textoBusca': textoBusca})

def caixaEditar(request, pk=0):
    try:
        conta = Conta.objects.get(pk=pk)
        pessoas = Pessoa.objects.all().order_by('nome')
    except:
        return HttpResponseRedirect('/caixas/')

    return render(request, 'caixas/formCaixas.html', {'conta': conta, 'pessoas':pessoas})

def caixaExcluir(request, pk=0):
    try:
        conta = Conta.objects.get(pk=pk)
        conta.delete()
        return HttpResponseRedirect('/caixas/')
    except:
        return HttpResponseRedirect('/caixas/')

def caixaFluxo(request):
    pessoas = Pessoa.objects.all()
    return render(request, 'caixas/caixaFluxo.html',{'pessoas':pessoas})

def pesquisaFluxo(request):
    pessoa_id = request.POST.get('pessoa_id')
    data = request.POST.get('data', '')
    data2 = request.POST.get('data2', '')

    datasplit1 = data[0:10].split('/') 
    datasplit2 = data2[0:10].split('/')

    pessoas = Pessoa.objects.all()

    totalReceber = 0
    totalPagar = 0

    try:
        if int(pessoa_id) == 0:
            contas = Conta.objects.filter(data__gte=date( int(datasplit1[2]), int(datasplit1[1]), int(datasplit1[0]) ) 
                                        , data__lte=date( int(datasplit2[2]), int(datasplit2[1]), int(datasplit2[0]) ))
        else:
            contas = Conta.objects.filter(pessoa_id = pessoa_id, data__gte=date( int(datasplit1[2]), int(datasplit1[1]), int(datasplit1[0]) ) 
                                        , data__lte=date( int(datasplit2[2]), int(datasplit2[1]), int(datasplit2[0]) ))
        for conta in contas:
            if conta.tipo == 'E':
                totalReceber = totalReceber + conta.valor
            else:
                totalPagar = totalPagar + conta.valor
    except:
       contas = []
    
    return render(request, 'caixas/caixaFluxo.html',{'pessoas':pessoas, 'contas':contas, 'totalPagar':totalPagar, 'totalReceber':totalReceber})



