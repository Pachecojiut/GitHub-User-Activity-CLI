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

#! Agrupando os pushes por repositório.
pushes = {}     #? Crio um dicionario vazio para guardar os pushes

#! Adicionando contagem de stars 
starred = []    #? Guarda os nomes dos repositórios

for event in events:
    tipo = event['type']
    repo = event['repo']['name']
    

    if tipo == 'PushEvent':
        pushes[repo] = pushes.get(repo, 0) + 1
    elif tipo == 'WatchEvent':
        starred.append(repo) #? Acrescenta no repo.
    elif tipo == 'CreateEvent':
        ref_type = event['payload']['ref_type']    #! 'ref_type' Diz o que foi criado no Github. (um repositorio? branch? tag?) ele da a resposta .
        print(f'- Created {ref_type} in {repo}')
    elif tipo == 'PullRequestEvent':        #!!!!!! Tratando outro evento
        action = event['payload']['action'] #! PullRequestEvetn == pedido para que as suas alterações de código sejam revisadas e incorporadas ao projeto principal
        print(f'- {action.capitalize()} a pull request in {repo}')
    else:
        print(f'- {tipo} in {repo}')
if starred:
    if len(starred) == 1:        #? Resolve a questão do singular e plural. 
        print(f'- Starred 1 repository')        #? Se star = 1, singular. 
    else:
        print(f'- Starred {len(starred)} repositories')  #? Se não, aparece quantidade normal, no plural
else:
    print(f'- 0 Starreds')      #? Caso nenhum nem outro, aparece 0 stars

for repo, total in pushes.items():          #? Percorro os pushes e os times que eu quero, e printo.
    if total == 1:
        print(f'- Pushed 1 time to {repo}')
    else:
        print(f'- Pushed {total} times to {repo}')


