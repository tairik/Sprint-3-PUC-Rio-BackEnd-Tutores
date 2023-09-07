from pydantic import BaseModel
from typing import List
from model.tutor import Tutor

class TutorSchema(BaseModel):
    """ Define como um novo cão a ser inserido deve ser representado
    """
    nome: str = "José"
    sobre_nome = "Silva"
    email: str = "silva@tutor.com"

class TutorViewSchema(BaseModel):
    """ Define como um cão será retornado
    """
    id: int = 1
    nome: str = "Fluffy"
    sobre_nome = "Silva"
    email: str = "silva@tutor.com"

def apresenta_tutor(tutor: Tutor):
    """ Retorna uma representação do cão seguindo o schema definido em
        TutorViewSchema.
    """
    return {
        "id": tutor.id,
        "nome": tutor.nome,
        "sobre_nome": tutor.sobre_nome,
        "email": tutor.email,
    }

class ListagemTutoresSchema(BaseModel):
    """ Define como uma listagem de cães será retornada.
    """
    tutor:List[TutorSchema]

class TutorBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do tutor.
    """
    id: int = 1

class TutorDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: str

def apresenta_tutores(tutores: List[Tutor]):
    """ Retorna uma representação do cão seguindo o schema definido em
        TutorViewSchema.
    """
    result = []
    for tutor in tutores:
        result.append({
            "id": tutor.id,
            "nome": tutor.nome,
            "sobre_nome": tutor.sobre_nome,
            "email": tutor.email,
        })

    return {"tutores": result}