# Cashback

O objetivo dessa aplicação é fornecer uma API para gestão de cashback de revendedores GB

## Requisitos

- Python 3.12+
- sqlite - foi utilizado esse banco pela praticidade
- Docker (_opcional_)

## Como executar a aplicação

A aplicação pode ser executada localmente ou através do *docker-compose*.

Esse projeto utiliza [fastapi](https://fastapi.tiangolo.com/) que provê swagger com base nas rotas e schemas, e com a aplicação rodando acesse http://localhost:8000/docs.

#### Ambiente local

Para instalar as dependências é necessário que o [poetry](https://python-poetry.org/) esteja instalado.

```sh
poetry install
```

As configurações ficam em variáveis de ambiente e devem ser informadas no arquivo `.env`. O arquivo `.env-example` tem um exemplo de configuração.

Depois de instaladas as dependências, executar o comando:
```sh
task run
```

##### Como executar os testes

Com as dependências instaladas, execute os testes com o comando:
```sh
task test
```

#### Docker compose

Para executar a aplicação utilizando o _docker-compose_ executar:
```sh
docker-compose up
```

## Como funciona

A aplicação tem cinco rotas e algumas necessitam de autenticação
- Sem autenticação
  - POST **/resellers** - cadastro de revendedores
  - POST **/auth/token** - login com geração de _access-token_
- Necessário autenticação (_access-token_)
  - POST **/purchases** - cadastro de compras
  - GET **/purchases** - lista compras cadastradas
  - GET **/cashback** - retorna cashback acumulado





