"""
.
"""
from typing import Annotated, Optional
from pydantic import Field, PositiveFloat

from workout_api.categorias.schemas import Categoria
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema
from workout_api.contrib.schemas import OutMixin


class AtletaSchema(BaseSchema):
    """
    .
    """
    nome: Annotated[str, Field(description='Nome do atleta', example='Cleber', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=40)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=90)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]
    categoria: Annotated[Categoria, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento')]

class AtletaSchemaOut(AtletaSchema, OutMixin):
    """
    .
    """
    pass


class AtletaSchemaUpdate(BaseSchema):
    """
    .
    """
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Cleber', max_length=50)]
    cpf: Annotated[Optional[str], Field(None,description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[Optional[int], Field(None,description='Idade do atleta', example=40)]
    peso: Annotated[Optional[PositiveFloat], Field(None,description='Peso do atleta', example=90)]
    altura: Annotated[Optional[PositiveFloat], Field(None,description='Altura do atleta', example=1.70)]
    sexo: Annotated[Optional[str], Field(None,description='Sexo do atleta', example='M', max_length=1)]
    categoria: Annotated[Optional[Categoria], Field(None,description='Categoria do atleta')]
    centro_treinamento: Annotated[Optional[CentroTreinamentoAtleta], Field(None, description='Centro de treinamento do atleta')]
