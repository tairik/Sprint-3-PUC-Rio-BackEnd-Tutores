# Tutores API

Este pequeno projeto faz parte do MVP do curso de Pós-Gradução em **Engenharia de Software** 

Esta API serve como microserviço para o cadatro de Tutores. 

Esta API utiliza uma API externa para a validação de emails: https://www.abstractapi.com/

E seguinte Endpoint é utilizado: https://www.abstractapi.com/api/email-verification-validation-api

Preço licença: https://www.abstractapi.com/api/email-verification-validation-api#pricing

Para até 100 requests a API é gratuita. Para este MVP é o bastante.

Documentação da API, foi usado Swagger.
---
## Como executar 

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

## Docker

docker build --tag api-tutores-docker . 

docker run -d --name api-tutores-docker -p 6001:6000 api-tutores-docker  

## Execução local

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenpython -m venv .v.pypa.io/en/latest/).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API basta lançar o seguinte comando no terminal:

```
(env)$ flask run --host 0.0.0.0 --port 5001
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5001 --reload
```

Abra o [http://localhost:5001/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
