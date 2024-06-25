"""
.
"""
from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.atleta.schemas import AtletaSchema, AtletaSchemaOut, AtletaSchemaUpdate
from workout_api.atleta.models import AtletaModel


router = APIRouter()

@router.post(
        '/',
        summary='Criar um novo centro de treinamento',
        status_code=status.HTTP_201_CREATED,
        response_model=AtletaSchemaOut
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaSchema = Body(...)
) -> AtletaSchemaOut:
    """
    .
    """
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome =atleta_in.centro_treinamento.nome
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))).scalars().first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A Categoria '{categoria_nome}' não foi encontrata"
        )
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O Centro de treinamento '{centro_treinamento_nome}' não foi encontrato"
        )

    try:
        atleta_out = AtletaSchemaOut(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao inserir os dados no banco"
        )

    return atleta_out

@router.get(
        '/',
        summary='Constultar todas os atletas',
        status_code=status.HTTP_200_OK,
        response_model=list[AtletaSchemaOut]
)
async def get_all(db_session: DatabaseDependency,) -> list[AtletaSchemaOut]:
    """
    .
    """
    atletas: list[AtletaSchemaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    return [AtletaSchemaOut.model_validate(atleta) for atleta in atletas]

@router.get(
        '/{id}',
        summary='Constultar um atleta pelo id',
        status_code=status.HTTP_200_OK,
        response_model=AtletaSchemaOut
)
async def get(id: UUID4, db_session: DatabaseDependency,) -> AtletaSchemaOut:
    """
    .
    """
    atleta: AtletaSchemaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta com id {id} não encontrada'
        )
    
    return atleta

@router.patch(
    '/{id}', 
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaSchemaOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaSchemaUpdate = Body(...)) -> AtletaSchemaOut:
    atleta: AtletaSchemaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete(
    '/{id}', 
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaSchemaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    await db_session.delete(atleta)
    await db_session.commit()