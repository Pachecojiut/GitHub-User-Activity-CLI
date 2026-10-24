# GitHub Activity CLI

CLI em Python que mostra no terminal a atividade de um usuário no GitHub, usando a API pública do GitHub. Não usa bibliotecas externas.

## Funcionalidades

- Busca eventos recentes do usuário do GitHub digitado.
- Agrupa eventos repetidos.
- Mostra as estrelas de cada repositorio mencionado.
- Trata erros comuns (usuário inexistente, limite da API, falta de conexão)

## Instalação

1. Clone o repositório:
    ```
    git clone <url-do-seu-repositório>
    ```
2. (Windows) Crie um `github-activity.bat` chamando o script e adicione a pasta ao PATH, para rodar o comando de qualquer lugar.

## Como usar

```
github-activity <username>
```

## Limitações

- Sem token, a API permite 60 requisições por hora, e cada repositório diferente
  gasta uma delas na busca de estrelas.
- A API de eventos não informa o número de commits de cada push, então o programa
  conta pushes, não commits.
- Mostra só os eventos recentes que a API devolve (até 30).

