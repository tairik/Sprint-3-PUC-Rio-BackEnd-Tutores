from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime
from typing import Union
from model import Base

class Tutor(Base):

    __tablename__ = 'tutor'
    id = Column("pk_cat", Integer, primary_key=True)
    email = Column(String(140), unique=True)
    nome = Column(String(140), unique=False)
    sobre_nome = Column(String(140), unique=False)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome: str, sobre_nome: str, email: str,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um Tutor

        Arguments:
            nome: nome do animal.
            sobre_nome: sobre_nome
            email: email
        """
        self.nome = nome
        self.sobre_nome = sobre_nome
        self.email = email

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao