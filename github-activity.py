import sys
import urllib.request, urllib.error
import json

if len(sys.argv) != 2:
    sys.exit('Uso: github-activity <username>')

username = sys.argv[1]

url = f'https://api.github.com/users/{username}/events'


req = urllib.request.Request(url, headers={'User-Agent': 'github-activity_cli'})    #? Monta o pedido da API


try:                #! Tratando a parte do codigo que pode dar erro com try/except.
    resposta = urllib.request.urlopen(req)   #? Envia o pedido e recebe a resposta  
except urllib.error.HTTPError as e:
    if e.code == 404:           #! Cada condição trata um erro!!!!!
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

#! Agrupando os pushes por repositório.
pushes = {}     #? Crio um dicionario vazio para guardar os pushes

#! Agrupando eventos repetidos na saida.
atividades = {}             # * Inves de cada condição la em baixo utilizar um print, a gente guarda a mensagem na variavel (frase) e depois adiciona neste dicionário.
for event in events:
    tipo = event['type']
    repo = event['repo']['name']

    #! !!!!!!!!!!
    url2 = f'https://api.github.com/repos/{repo}'                           
    req_repo = urllib.request.Request(url2, headers={'User-Agent': 'github-activity_cli'})              #! Todo este bloco é uma requisição de API. Você manda a requisição recebe a informação
    reposta_repo = urllib.request.urlopen(req_repo)                                                     #! e guarda ela numa variável para uso.
    conteudo_repo = reposta_repo.read()
    stars_repo = json.loads(conteudo_repo.decode('utf-8'))
    star = stars_repo['stargazers_count']
    #! !!!!!!!!!!!!

    if tipo == 'PushEvent':
        frase = f'- Pushed to {repo}'

    elif tipo == 'WatchEvent':
        frase = f'- Starred {repo}'

    elif tipo == 'CreateEvent':
        ref_type = event['payload']['ref_type']    #! 'ref_type' Diz o que foi criado no Github. (um repositorio? branch? tag?) ele da a resposta.
        frase = f'- Created {ref_type} in {repo}'

    elif tipo == 'PullRequestEvent':        #!!!!!! Tratando outro evento
        action = event['payload']['action'] #! PullRequestEvetn == pedido para que as alterações de código sejam revisadas e implementadas ao projeto principal
        frase = f'- {action.capitalize()} a pull request in {repo}'

    else:
        frase = f'- {tipo} in {repo}'
    atividades[frase] = atividades.get(frase,0) +1

#? Resolve a questão do singular e plural. 

for frase, total in atividades.items():         # * Agora percorro o dicionario e printo ele.
    print(f'{frase} (x{total})')




