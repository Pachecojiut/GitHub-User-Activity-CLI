# GitHub Activity CLI

CLI em Python que mostra no terminal a atividade de um usuário no GitHub, usando a API pública do GitHub. Não usa bibliotecas externas.

## Funcionalidades

- Busca eventos recentes do usuário do GitHub digitado.
- Agrupa eventos repetidos.
- Mostra as estrelas de cada repositório mencionado.
- Mostra quantidade de commits e pushes em um repositório.
- Trata erros comuns. (usuário inexistente, limite da API, falta de conexão)

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


# GITUHB_TOKEN (opcional)

É possivel configurar um GITHUB_TOKEN para aumentar o limite de requisições da API do GitHub.

**Sem token o limite de requisições por hora é de 60;
com `GITHUB_TOKEN` são 5.000 requisições por hora.**

### Como configurar

Crie um token no GitHub e configure-o como variável de ambiente chamada `GITHUB_TOKEN`.

No Windows PowerShell:

```powershell
$env:GITHUB_TOKEN="seu_token_aqui"
```

## Limitações

- Sem token, a API permite 60 requisições por hora, e cada repositório diferente
gasta uma delas na busca de estrelas.
- Mostra só os eventos recentes que a API devolve (até 30).




