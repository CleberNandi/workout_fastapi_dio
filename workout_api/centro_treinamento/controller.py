"""
.
"""
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.centro_treinamento.schemas import CentroTreinamento, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel


router = APIRouter()

@router.post(
        '/',
        summary='Criar um novo centro de treinamento',
        status_code=status.HTTP_201_CREATED,
        response_model=CentroTreinamentoOut
)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamento = Body(...)
) -> CentroTreinamentoOut:
    """
    .
    """
    categoria_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    categoria_model = CentroTreinamentoModel(**categoria_out.model_dump())
    db_session.add(categoria_model)
    await db_session.commit()

    return categoria_out

@router.get(
        '/',
        summary='Constultar todas os centros de treinamento',
        status_code=status.HTTP_200_OK,
        response_model=list[CentroTreinamentoOut]
)
async def get_all(db_session: DatabaseDependency,) -> list[CentroTreinamentoOut]:
    """
    .
    """
    centro_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    
    return centro_treinamento

@router.get(
        '/{id}',
        summary='Constultar uma categoria pelo id',
        status_code=status.HTTP_200_OK,
        response_model=CentroTreinamentoOut
)
async def get(id: UUID4, db_session: DatabaseDependency,) -> CentroTreinamentoOut:
    """
    .
    """
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de treinamento com id {id} não encontrada'
        )
    
    return centro_treinamento