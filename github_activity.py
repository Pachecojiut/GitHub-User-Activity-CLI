import sys
import urllib.request, urllib.error
import json

if len(sys.argv) != 2:
    sys.exit('Uso: github_activity <username>')

username = sys.argv[1]

url = f'https://api.github.com/users/{username}/events'


req = urllib.request.Request(url, headers={'User-Agent': 'github-activity_cli'})    #? Monta o pedido da API


try:                #! Tratando a parte do codigo que pode dar erro com try/except.
    resposta = urllib.request.urlopen(req)   #? Envia o pedido e recebe a resposta  
except urllib.error.HTTPError as e:
    if e.code == 404:
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
for event in events:
    tipo = event['type']
    repo = event['repo']['name']

    if tipo == 'PushEvent':
        print(f'- Pushed to {repo}')
    elif tipo == 'WatchEvent':
        print(f'- Starred {repo}')
    elif tipo == 'CreateEvent':
        ref_type = event['payload']['ref_type']
        print(f'- Created {ref_type} in {repo}')
    else:
        print(f'- {tipo} in {repo}')


