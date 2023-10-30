from django.http import JsonResponse
from .models import Estudante, Repositorio
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from .integracao_github import (criar_repositorio_github, 
                                adicionar_colaborador_repositorio,
                                adicionar_readme)

@csrf_exempt
def criar_repositorios(request):
    dados = request.POST.get('dados', '').split('\n')
    nome_org = config("NOME_ORG", "Valor-Padrao")

    for item in dados:
        nome, identificador = item.split(':')
        sucesso_repo = criar_repositorio_github(nome, nome_org)
        if sucesso_repo:
            adicionar_colaborador_repositorio(nome, identificador, nome_org)
            adicionar_readme(nome, nome, nome_org)
            estudante, _ = Estudante.objects.get_or_create(nome=nome, identificador_github=identificador)
            Repositorio.objects.create(nome=nome, estudante=estudante)
    
    return JsonResponse({"status": "Repositório criado com sucesso, você conseguirá ve-lo no github."})