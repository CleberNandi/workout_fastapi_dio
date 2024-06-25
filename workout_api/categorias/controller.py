"""
.
"""
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.categorias.schemas import Categoria, CategoriaOut
from workout_api.categorias.models import CategoriaModel


router = APIRouter()

@router.post(
        '/',
        summary='Criar nova categoria',
        status_code=status.HTTP_201_CREATED,
        response_model=CategoriaOut
)
async def post(
    db_session: DatabaseDependency,
    categoria_in: Categoria = Body(...)
) -> CategoriaOut:
    """
    .
    """
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    db_session.add(categoria_model)
    await db_session.commit()

    return categoria_out

@router.get(
        '/',
        summary='Constultar todas as categoria',
        status_code=status.HTTP_200_OK,
        response_model=list[CategoriaOut]
)
async def get_all(db_session: DatabaseDependency,) -> list[CategoriaOut]:
    """
    .
    """
    cateforias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    
    return cateforias

@router.get(
        '/{id}',
        summary='Constultar uma categoria pelo id',
        status_code=status.HTTP_200_OK,
        response_model=CategoriaOut
)
async def get(id: UUID4, db_session: DatabaseDependency,) -> CategoriaOut:
    """
    .
    """
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Categoria com id {id} não encontrada'
        )
    
    return categoria