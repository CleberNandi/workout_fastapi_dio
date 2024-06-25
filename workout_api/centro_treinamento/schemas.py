from typing import Annotated

from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    """
    .
    """
    nome: Annotated[str, Field(description='Nome do centro de treinamentos', example='CT King', max_length=30)]
    endereco: Annotated[str, Field(description='Endereco do centro de treinamentos', example='Rua 15, quadra 14', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietario do centro de treinamentos', example='Marcos', max_length=30)]


class CentroTreinamentoAtleta(BaseSchema):
    """
    .
    """
    nome: Annotated[str, Field(description='Nome do centro de treinamentos', example='CT King', max_length=30)]


class CentroTreinamentoOut(CentroTreinamento):
    """
    .
    """
    id: Annotated[UUID4, Field(description='Identificador de centro de treinamento')]
