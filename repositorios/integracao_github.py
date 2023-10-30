# repositorios/integracao_github.py
# Adicionar metodo para DELETAR um repositório > SÓ DELETARÁ SE HOUVER MAIS DE X COMITS (os iniciais, para evitar deletar repositórios que já foram usados)

import requests
import base64
from decouple import config

URL_API_GITHUB = "https://api.github.com"
# Token gerado em https://github.com/settings/tokens (classic)
TOKEN_GITHUB = config("GITHUB_TOKEN", "default_token")


def criar_repositorio_github(nome_repositorio, nome_org):
    headers = {
        "Authorization": f"token {TOKEN_GITHUB}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": nome_repositorio.replace(" ", "-"),
        "description": f"Repositório do(a) {nome_repositorio}",
        "private": True  # Privar OU não repo
    }
    response = requests.post(
        f"{URL_API_GITHUB}/orgs/{nome_org}/repos", headers=headers, json=data)
    if response.status_code == 201:
        return True
    return False


def adicionar_colaborador_repositorio(nome_repositorio, identificador_github, nome_org):
    headers = {
        "Authorization": f"token {TOKEN_GITHUB}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"{URL_API_GITHUB}/repos/{nome_org}/{nome_repositorio.replace(' ', '-')}/collaborators/{identificador_github}"
    response = requests.put(url, headers=headers, json={"permission": "admin"})
    if response.status_code in [200, 201]:
        return True
    return False


def adicionar_readme(nome_repositorio, nome_aluno, nome_org):
    headers = {
        "Authorization": f"token {TOKEN_GITHUB}",
        "Accept": "application/vnd.github.v3+json"
    }
    content = """
# Repositório de Aluno(a) 📘

Olá! Este é o repositório pessoal do(a) **{nome}**. Aqui, você encontrará atividades, projetos e qualquer outro conteúdo que eu deseje compartilhar ao longo da minha jornada acadêmica.

## 📌 Principais Características

- 🎓 **Professor(a) e Aluno(a):** Tanto eu, Aluno(a) {nome}, quanto o professor temos acesso total a este repositório.
- 🛠 **Edição:** Somente eu posso editar diretamente os conteúdos aqui presentes.
- 🤝 **Colaboração:** Se você desejar contribuir ou sugerir melhorias, sinta-se à vontade para criar uma pull request. O professor também pode fazer isso.
- 🚀 **Desenvolvimento:** Estarei constantemente atualizando este repositório com novas atividades e projetos.

## 📬 Contribuições

Se você tem alguma sugestão ou identificou algum problema, não hesite em abrir uma pull request. Sua contribuição será analisada e, se aprovada, incorporada ao repositório.
""".format(nome=nome_aluno)
    data = {
        "message": "Adicionado README.md",
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8")
    }
    url = f"{URL_API_GITHUB}/repos/{nome_org}/{nome_repositorio.replace(' ', '-')}/contents/README.md"
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        return True
    return False
