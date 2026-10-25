import sys
import urllib.request, urllib.error
import json
import os

token=os.environ.get('GITHUB_TOKEN')

headers = {'User-Agent': 'github-activity_cli'}
if token:
    headers['Authorization'] = f'Bearer {token}'

def buscar(url): #* Função para pegar os commits do usuário.
    req_commits = urllib.request.Request(url, headers=headers)
    try:
        respota_commits = urllib.request.urlopen(req_commits, timeout=10)
        conteudo_commits = respota_commits.read()
        dados_commits = json.loads(conteudo_commits.decode('utf-8'))
        return dados_commits
    except (urllib.error.URLError, TimeoutError, ValueError):
        return None

if len(sys.argv) != 2:
    sys.exit('Uso: github-activity <username>')

username = sys.argv[1]

url = f'https://api.github.com/users/{username}/events'


req = urllib.request.Request(url, headers=headers)    #? Monta o pedido da API


try:                #! Tratando a parte do codigo que pode dar erro com try/except.
    resposta = urllib.request.urlopen(req, timeout=10)   #? Envia o pedido e recebe a resposta  
except urllib.error.HTTPError as e:
    if e.code == 404:           #! Cada condição trata um erro
        sys.exit('Erro: usuário não encontrado')
    elif e.code == 403:
        sys.exit('Erro: Limite de requisições de API atingido. Tente mais tarde.')
    else:
        sys.exit(f'Erro da API: código {e.code}')
except urllib.error.URLError:
    sys.exit('Erro de conexão: verifique sua conexão com a internet.')
conteudo = resposta.read()                                                                     
events = json.loads(conteudo.decode('utf-8'))

if not events:
    sys.exit('Nenhuma atividade recente encontrada.')

#! Agrupando eventos repetidos na saida.
commits = {}
atividades = {}         # * Inves de cada condição la em baixo utilizar um print, a gente guarda a mensagem na variavel (frase) e depois adiciona neste dicionário.
repositorios = {}       #* Guarda as estrelas por repositorios

for event in events:
    tipo = event['type']
    repo = event['repo']['name']

    if repo not in repositorios:
        url2 = f'https://api.github.com/repos/{repo}'                           
        req_repo = urllib.request.Request(url2, headers=headers)  
        try:
            reposta_repo = urllib.request.urlopen(req_repo, timeout=10)   
            conteudo_repo = reposta_repo.read()
            stars_repo = json.loads(conteudo_repo.decode('utf-8'))
            repositorios[repo] = stars_repo['stargazers_count']

        except urllib.error.HTTPError as e:
            if e.code == 403:
                repositorios[repo] = None

        except urllib.error.URLError:
            repositorios[repo] = None 

    if tipo == 'PushEvent':
        before = event['payload']['before']
        head = event['payload']['head']
        dados_push = None                       # começa vazio, evita NameError

        if before != '0' * 40:                  # pula o primeiro push da branch
            url3 = f'https://api.github.com/repos/{repo}/compare/{before}...{head}'
            dados_push = buscar(url3)

        frase = f'- Pushed to {repo}'

        if dados_push:                          # só soma se a função não devolveu None
            commits[frase] = commits.get(frase, 0) + dados_push['total_commits']
        
    elif tipo == 'WatchEvent':
        frase = f'- Starred {repo}'

    elif tipo == 'CreateEvent':
        ref_type = event['payload']['ref_type']    #! 'ref_type' Diz o que foi criado no Github. (um repositorio? branch? tag?) ele da a resposta.
        frase = f'- Created {ref_type} in {repo}'

    elif tipo == 'PullRequestEvent':        #? Tratando outro evento.
        action = event['payload']['action'] #! PullRequestEvetn == pedido para que as alterações de código sejam revisadas e implementadas ao projeto principal
        frase = f'- {action.capitalize()} a pull request in {repo}'

    #! Adicionando IssuesEvent um registro de uma tarefa, bug ou ideia dentro de um repositório do GitHub quadro de avisos do projeto, onde as pessoas anotam o que precisa ser feito ou corrigido
    elif tipo == 'IssuesEvent':
        action = event['payload']['action']
        number_issue = event['payload']['issue']['number']
        title_issue = event['payload']['issue']['title']
        frase = f'- {action.capitalize()} issue #{number_issue} "{title_issue}" in {repo}'

    else:
        frase = f'- {tipo} in {repo}'
    atividades[frase] = atividades.get(frase,0) +1 

# * Agora percorro o dicionario e printo ele.
linhas = []
for frase, total in atividades.items():
    texto = frase.removeprefix('- ')
    if frase in commits:
        n = commits[frase]
        nome = 'commit' if n == 1 else 'commits'
        texto = texto.replace('Pushed to', f'Pushed {n} {nome} to', 1)
    linhas.append((texto, total))

largura = max(len(t) for t, _ in linhas)
largura_repo = max(len(r) for r in repositorios)
tamanho_linha = max(largura + 10, largura_repo + 20)

print(f'\nGitHub activity for {username}')
print('=' * tamanho_linha)

print('\nRecent activity')
print('-' * tamanho_linha)
for texto, total in linhas:
    vezes = f'x{total}' if total > 1 else ''
    print(f'  - {texto:<{largura}}  {vezes:>4}')


# * Resolvendo o problema das stars
print('\nRepository stars')
print('-' * tamanho_linha)
for repo, star in repositorios.items():
    if star is not None:
        nome = 'star' if star == 1 else 'stars'
        print(f'  - {repo:<{largura_repo}}  {star:>5} {nome}')
    else:
        print(f'  - {repo:<{largura_repo}}  Unable to retrieve the stars')
