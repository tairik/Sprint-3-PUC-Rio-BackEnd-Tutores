from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from sqlalchemy.exc import IntegrityError
from model import Session, Tutor
from logger import logger
from schemas import *
from flask_cors import CORS
import requests
from flask import request

info = Info(title="PetDiet Tutores API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tutor_tag = Tag(name="Tutor", description="Adição, visualização e remoção de Tutores à base")

# definindo base_url e key para API Abstract
abstract_api_base_url = 'https://emailvalidation.abstractapi.com/v1/'
abstract_api_key = '92dc213e968d42a38fff0ae5ee1f5b1a'

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

## Sistema PetDiet
##Rotas para os Tutores
@app.post('/tutor', tags=[tutor_tag],
          responses={"200": TutorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tutor(body: TutorSchema):
    """Adiciona um novo tutor à base de dados

    Retorna uma representação dos tutores.
    """
    data = request.json
    results = requests.get(abstract_api_base_url + '?api_key='+abstract_api_key+'&email=' + data.get('email')).json()
    is_valid_format = results["is_valid_format"]['value']
    #is_valid_format = False
    if is_valid_format == False:
        error_msg = "Email inválido"
        return {"message": error_msg}, 400

    tutor = Tutor(
        nome=data.get('nome'),
        sobre_nome=data.get('sobre_nome'),
        email = data.get('email'))
    logger.debug(f"Adicionando tutor de nome: '{tutor.nome}'")

    try:
        # criando conexão com a base
        session = Session()
        # adicionando tutor
        session.add(tutor)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado Tutor de nome: '{tutor.nome}'")
        return apresenta_tutor(tutor), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Tutor de mesmo email já salvo na base :/"
        logger.warning(f"Erro ao adicionar tutor '{tutor.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar tutor '{tutor.nome}', {error_msg}")
        return {"message": error_msg}, 400

@app.delete('/tutor', tags=[tutor_tag],
            responses={"200": TutorDelSchema, "404": ErrorSchema})
def del_tutor(query: TutorBuscaSchema):
    """Deleta um tutor a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    tutor_id = query.id
    logger.debug(f"Deletando dados sobre o tutor: #{tutor_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Tutor).filter(Tutor.id == tutor_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado o tutor: #{tutor_id}")
        return {"message": "Tutor deletado", "id": tutor_id}
    else:
        # se o tutor não foi encontrado
        error_msg = "Tutor não encontrado na base :/"
        logger.warning(f"Erro ao deletar o tutor: #'{tutor_id}', {error_msg}")
        return {"message": error_msg}, 404

@app.put('/tutor', tags=[tutor_tag],
            responses={"200": TutorDelSchema, "404": ErrorSchema})
def put_tutor(body: TutorViewSchema):
    """Atualiza um tutor a partir do id informado

    Retorna os dados do tutor atualizado.
    """
    tutor_id = body.id

    try:
        # criando conexão com a base
        session = Session()
        # adicionando tutor
        tutor = session.query(Tutor).filter(Tutor.id == tutor_id).first()
        tutor.nome = body.nome
        tutor.sobre_nome = body.sobre_nome
        tutor.email = body.email
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Alterando Tutor de nome: '{tutor.nome}'")
        return apresenta_tutor(tutor), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Tutor de mesmo email já salvo na base :/"
        logger.warning(f"Erro ao adicionar tutor '{tutor.email}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar tutor '{tutor.nome}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/tutores', tags=[tutor_tag],
             responses={"200": ListagemTutoresSchema, "404": ErrorSchema})
def get_tutores():
        """Faz a busca por todos os tutores cadastrados

        Retorna uma representação da listagem de tutores.
        """
        logger.debug(f"Coletando tutores ")

        # criando conexão com a base
        session = Session()
        # fazendo a busca
        tutores = session.query(Tutor).all()

        if not tutores:
            # se não há tutores cadastrados
            return {"tutores": []}, 200
        else:
            logger.debug(f"%d tutores econtrados" % len(tutores))
            # retorna a representação de tutores
            return apresenta_tutores(tutores), 200
